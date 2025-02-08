# Signal to Noise Ratio (SNR)

import os

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.signal import find_peaks


class SNRAnalyzer:
    def __init__(self, folder_path: str, sampling_rate: int = 500):
        self.folder_path = folder_path
        self.sampling_rate = sampling_rate
        self.frequency_snr = {}
        self.load_data()

    def _calculate_snr(self, signal):
        """Calculates SNR (in dB) from a given signal."""
        n = len(signal)
        fft_result = np.fft.fft(signal)
        freqs = np.fft.fftfreq(n, d=1 / self.sampling_rate)
        fft_magnitude = np.abs(fft_result[:n // 2])
        freqs = freqs[:n // 2]

        # Peak frequency
        peak_indices, _ = find_peaks(fft_magnitude, height=np.max(fft_magnitude) * 0.5)
        signal_freq_index = peak_indices[np.argmax(fft_magnitude[peak_indices])]
        signal_freq = freqs[signal_freq_index]

        power_spectrum = fft_magnitude ** 2

        # Signal power
        bandwidth = 1  # +-X Hz
        signal_band = (freqs > (signal_freq - bandwidth)) & (freqs < (signal_freq + bandwidth))
        signal_power = np.sum(power_spectrum[signal_band])

        total_power = np.sum(power_spectrum)
        noise_power = total_power - signal_power

        # Exclude harmonics if signal frequency > 1 Hz
        if signal_freq > 1:
            harmonics_power = 0
            harmonic_number = 2
            while True:
                harmonic_freq = harmonic_number * signal_freq
                if harmonic_freq >= freqs[-1]:
                    break
                harmonic_band = (freqs > (harmonic_freq - bandwidth)) & (freqs < (harmonic_freq + bandwidth))
                harmonics_power += np.sum(power_spectrum[harmonic_band])
                harmonic_number += 1

            noise_power -= harmonics_power  # Exclude harmonics

        # Compute SNR in dB
        snr_db = 10 * np.log10(signal_power / noise_power)

        return snr_db, signal_freq

    def load_data(self):
        for file_name in os.listdir(self.folder_path):
            if file_name.endswith('.csv'):
                frequency = float(file_name.split('_')[-1].replace('Hz.csv', '').replace(',', '.'))
                file_path = os.path.join(self.folder_path, file_name)

                data = pd.read_csv(file_path, header=None, sep='\t')
                data = data.apply(lambda col: col.str.replace(',', '.')).astype('float64')

                channel = data[1]
                mean_removed = channel - channel.mean()

                snr, freq = self._calculate_snr(mean_removed)
                if snr is not None:
                    self.frequency_snr[frequency] = snr

    def plot(self):
        sorted_frequencies = sorted(self.frequency_snr.keys())
        sorted_snr = [self.frequency_snr[freq] for freq in sorted_frequencies]

        plt.figure(figsize=(10, 6))
        plt.plot(sorted_frequencies, sorted_snr, marker='o', linestyle='-', color='b')
        plt.xscale('log')
        plt.grid(which='both', linestyle='--', linewidth=0.5)
        plt.title('SNR (in dB)')
        plt.xlabel('Frequency (Hz)')
        plt.ylabel('SNR (dB)')

        for freq, snr_value in zip(sorted_frequencies, sorted_snr):
            plt.text(freq, snr_value, f'{freq}Hz', fontsize=8, ha='right', va='bottom')

        plt.show()


if __name__ == "__main__":
    folder_path = '../data/frequency_response_ads131m08'
    # folder_path = '../data/frequency_response_ad7771'

    snr_analyzer = SNRAnalyzer(folder_path)
    snr_analyzer.plot()
