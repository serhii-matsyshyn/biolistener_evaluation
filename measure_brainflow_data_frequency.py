import time
from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds, BrainFlowPresets


def main():
    BoardShim.enable_dev_board_logger()

    params = BrainFlowInputParams()
    params.ip_port = 0
    params.ip_address = '0.0.0.0'

    board = BoardShim(BoardIds.BIOLISTENER_BOARD.value, params)
    board.prepare_session()
    board.config_board("""{"command": 1, "data_rate": 500}\n""")
    for i in range(8):
        board.config_board(f'{{"command": 3, "channel": {i}, "pga": 8}}\n')
    # board.config_board("""{"command": 2, "channel": 0, "enable": 0}\n""")

    board.start_stream()

    time_started = time.time()
    total_packages_received = 0
    while (time.time() - time_started) < 20:
        data = board.get_board_data(preset=BrainFlowPresets.DEFAULT_PRESET)
        if len(data[0]) == 0:
            time.sleep(0.1)
        else:
            total_packages_received += len(data[0])
            print(data)

    board.stop_stream()
    board.release_session()

    print("Data received: " + str(total_packages_received) + " packages")
    print("Hz: " + str(total_packages_received / 20))

    print(data)


if __name__ == "__main__":
    main()
