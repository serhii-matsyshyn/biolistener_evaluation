# Original example source: https://brainflow.org/2021-07-05-real-time-example/

import argparse
import logging

import pyqtgraph as pg
from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds, BrainFlowPresets
from brainflow.data_filter import DataFilter, FilterTypes, WindowOperations, DetrendOperations
from pyqtgraph.Qt import QtGui, QtCore


class Graph:
    def __init__(self, board_shim):
        pg.setConfigOption('background', 'w')
        pg.setConfigOption('foreground', 'k')

        self.board_id = board_shim.get_board_id()
        self.board_shim = board_shim
        self.exg_channels = BoardShim.get_exg_channels(self.board_id)
        self.sampling_rate = BoardShim.get_sampling_rate(self.board_id)

        self.battery_voltage_channel = BoardShim.get_battery_channel(
            self.board_id,
            BrainFlowPresets.AUXILIARY_PRESET.value
        )
        self.update_speed_ms = 50
        self.window_size = 4
        self.num_points = self.window_size * self.sampling_rate

        self.app = QtGui.QApplication([])
        self.win = pg.GraphicsLayoutWidget(title='BrainFlow Plot', size=(800, 600))

        self.battery_voltage_label = pg.LabelItem(justify='right')
        self.win.addItem(self.battery_voltage_label, row=10, col=1)

        self._init_pens()
        self._init_timeseries()
        self._init_psd()
        self._init_band_plot()

        timer = QtCore.QTimer()
        timer.timeout.connect(self.update)
        timer.start(self.update_speed_ms)
        self.win.show()
        QtGui.QApplication.instance().exec_()

    def _init_pens(self):
        self.pens = list()
        self.brushes = list()
        colors = ['#A54E4E', '#A473B6', '#5B45A4', '#2079D2', '#32B798', '#2FA537', '#9DA52F', '#A57E2F', '#A53B2F']
        for i in range(len(colors)):
            pen = pg.mkPen({'color': colors[i], 'width': 2})
            self.pens.append(pen)
            brush = pg.mkBrush(colors[i])
            self.brushes.append(brush)

    def _init_timeseries(self):
        self.plots = list()
        self.curves = list()
        for i in range(len(self.exg_channels)):
            p = self.win.addPlot(row=i, col=0)
            p.showAxis('left', False)
            p.setMenuEnabled('left', False)
            p.showAxis('bottom', False)
            p.setMenuEnabled('bottom', False)
            if i == 0:
                p.setTitle('TimeSeries Plot')
            self.plots.append(p)
            curve = p.plot(pen=self.pens[i % len(self.pens)])
            # curve.setDownsampling(auto=True, method='mean', ds=3)
            self.curves.append(curve)

    def _init_psd(self):
        self.psd_plot = self.win.addPlot(row=0, col=1, rowspan=len(self.exg_channels) // 2)
        self.psd_plot.showAxis('left', False)
        self.psd_plot.setMenuEnabled('left', False)
        self.psd_plot.setTitle('PSD Plot')
        self.psd_plot.setLogMode(False, True)
        self.psd_curves = list()
        self.psd_size = DataFilter.get_nearest_power_of_two(self.sampling_rate)
        for i in range(len(self.exg_channels)):
            psd_curve = self.psd_plot.plot(pen=self.pens[i % len(self.pens)])
            psd_curve.setDownsampling(auto=True, method='mean', ds=3)
            self.psd_curves.append(psd_curve)

    def _init_band_plot(self):
        self.band_plot = self.win.addPlot(row=len(self.exg_channels) // 2, col=1, rowspan=len(self.exg_channels) // 2)
        self.band_plot.showAxis('left', False)
        self.band_plot.setMenuEnabled('left', False)
        self.band_plot.showAxis('bottom', False)
        self.band_plot.setMenuEnabled('bottom', False)
        self.band_plot.setTitle('BandPower Plot')
        y = [0, 0, 0, 0, 0]
        x = [1, 2, 3, 4, 5]
        self.band_bar = pg.BarGraphItem(x=x, height=y, width=0.8, pen=self.pens[0], brush=self.brushes[0])
        self.band_plot.addItem(self.band_bar)

    def update(self):
        data = self.board_shim.get_current_board_data(self.num_points)
        data_auxilary = self.board_shim.get_current_board_data(self.num_points, BrainFlowPresets.AUXILIARY_PRESET.value)

        if len(data_auxilary[self.battery_voltage_channel]) > 0:
            battery_voltage = data_auxilary[self.battery_voltage_channel][-1]
            self.battery_voltage_label.setText(f'Battery Voltage: {battery_voltage:.2f} V')

        avg_bands = [0, 0, 0, 0, 0]
        for count, channel in enumerate(self.exg_channels):
            # plot timeseries
            DataFilter.detrend(data[channel], DetrendOperations.CONSTANT.value)
            DataFilter.perform_bandpass(data[channel], self.sampling_rate, 3.0, 45.0, 2,
                                        FilterTypes.BUTTERWORTH_ZERO_PHASE, 0)
            DataFilter.perform_bandstop(data[channel], self.sampling_rate, 48.0, 52.0, 2,
                                        FilterTypes.BUTTERWORTH_ZERO_PHASE, 0)
            DataFilter.perform_bandstop(data[channel], self.sampling_rate, 58.0, 62.0, 2,
                                        FilterTypes.BUTTERWORTH_ZERO_PHASE, 0)
            self.curves[count].setData(data[channel].tolist())
            if data.shape[1] > self.psd_size:
                # plot psd
                psd_data = DataFilter.get_psd_welch(data[channel], self.psd_size, self.psd_size // 2,
                                                    self.sampling_rate,
                                                    WindowOperations.BLACKMAN_HARRIS.value)
                lim = min(70, len(psd_data[0]))
                self.psd_curves[count].setData(psd_data[1][0:lim].tolist(), psd_data[0][0:lim].tolist())
                # plot bands
                avg_bands[0] = avg_bands[0] + DataFilter.get_band_power(psd_data, 2.0, 4.0)
                avg_bands[1] = avg_bands[1] + DataFilter.get_band_power(psd_data, 4.0, 8.0)
                avg_bands[2] = avg_bands[2] + DataFilter.get_band_power(psd_data, 8.0, 13.0)
                avg_bands[3] = avg_bands[3] + DataFilter.get_band_power(psd_data, 13.0, 30.0)
                avg_bands[4] = avg_bands[4] + DataFilter.get_band_power(psd_data, 30.0, 50.0)

        avg_bands = [int(x * 100 / len(self.exg_channels)) for x in avg_bands]
        self.band_bar.setOpts(height=avg_bands)

        self.app.processEvents()


def main():
    # BoardShim.enable_dev_board_logger()
    logging.basicConfig(level=logging.DEBUG)

    parser = argparse.ArgumentParser()
    # use docs to check which parameters are required for specific board, e.g. for Cyton - set serial port
    parser.add_argument('--timeout', type=int, help='timeout for device discovery or connection', required=False,
                        default=0)
    parser.add_argument('--ip-port', type=int, help='ip port', required=False, default=12345)
    parser.add_argument('--ip-protocol', type=int, help='ip protocol, check IpProtocolType enum', required=False,
                        default=0)
    parser.add_argument('--ip-address', type=str, help='ip address', required=False, default='0.0.0.0')
    parser.add_argument('--serial-port', type=str, help='serial port', required=False, default='')
    parser.add_argument('--mac-address', type=str, help='mac address', required=False, default='')
    parser.add_argument('--other-info', type=str, help='other info', required=False, default='')
    parser.add_argument('--streamer-params', type=str, help='streamer params', required=False, default='')
    parser.add_argument('--serial-number', type=str, help='serial number', required=False, default='')
    parser.add_argument('--board-id', type=int, help='board id, check docs to get a list of supported boards',
                        required=False, default=BoardIds.BIOLISTENER_BOARD.value)
    parser.add_argument('--file', type=str, help='file', required=False, default='')
    parser.add_argument('--master-board', type=int, help='master board id for streaming and playback boards',
                        required=False, default=BoardIds.NO_BOARD)
    args = parser.parse_args()

    params = BrainFlowInputParams()
    params.ip_port = args.ip_port
    params.serial_port = args.serial_port
    params.mac_address = args.mac_address
    params.other_info = args.other_info
    params.serial_number = args.serial_number
    params.ip_address = args.ip_address
    params.ip_protocol = args.ip_protocol
    params.timeout = args.timeout
    params.file = args.file
    params.master_board = args.master_board

    board_shim = BoardShim(args.board_id, params)
    try:
        board_shim.prepare_session()
        board_shim.config_board("""{"command": 1, "data_rate": 500}\n""")
        for i in range(8):
            board_shim.config_board(f'{{"command": 3, "channel": {i}, "pga": 8}}\n')

        board_shim.start_stream(450000, args.streamer_params)
        Graph(board_shim)
    except BaseException:
        logging.warning('Exception', exc_info=True)
    finally:
        if board_shim.is_prepared():
            logging.info('Releasing session')
            board_shim.release_session()


if __name__ == '__main__':
    main()
