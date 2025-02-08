# Frequency response

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


class FrequencyResponseAnalyzer:
    def __init__(self, folder_path: str, reference_freq: float = 5.0):
        self.folder_path = folder_path
        self.reference_freq = reference_freq
        self.frequency_vrms = {}

        self.load_data()

    def load_data(self):
        for file_name in os.listdir(self.folder_path):
            if file_name.endswith('.csv'):
                frequency = float(file_name.split('_')[-1].replace('Hz.csv', '').replace(',', '.'))
                file_path = os.path.join(self.folder_path, file_name)

                data = pd.read_csv(file_path, header=None, sep='\t')
                data = data.apply(lambda col: col.str.replace(',', '.')).astype('float64')

                channel = data[1]
                mean_removed = channel - channel.mean()

                # Compute Vrms (standard deviation of the mean-removed data)
                self.frequency_vrms[frequency] = mean_removed.std()

    def compute_normalized_vrms(self):
        if self.reference_freq not in self.frequency_vrms:
            raise ValueError(f"Reference frequency {self.reference_freq}Hz not found in data.")

        sorted_frequencies = sorted(self.frequency_vrms.keys())
        reference_vrms = self.frequency_vrms[self.reference_freq]

        normalized_vrms = [self.frequency_vrms[freq] / reference_vrms * 100 for freq in sorted_frequencies]
        normalized_vrms_db = [20 * np.log10(vrms / 100) for vrms in normalized_vrms]

        return sorted_frequencies, normalized_vrms, normalized_vrms_db

    def plot_in_percent(self):
        sorted_frequencies, normalized_vrms, normalized_vrms_db = self.compute_normalized_vrms()

        # Normalized Vrms (%)
        plt.figure(figsize=(10, 6))
        plt.plot(sorted_frequencies, normalized_vrms, marker='o', linestyle='-', color='b')
        plt.xscale('log')
        plt.grid(which='both', linestyle='--', linewidth=0.5)
        plt.title('Frequency Response')
        plt.xlabel('Frequency (Hz)')
        plt.ylabel('Normalized Vrms (%)')
        plt.axhline(100, color='r', linestyle='--', label=f'Reference ({self.reference_freq}Hz)')

        for freq, norm_vrms in zip(sorted_frequencies, normalized_vrms):
            plt.text(freq, norm_vrms, f'{freq}Hz', fontsize=8, ha='right', va='bottom')

        plt.legend()
        plt.show()

    def plot(self):
        sorted_frequencies, normalized_vrms, normalized_vrms_db = self.compute_normalized_vrms()

        # Normalized Vrms in dB
        plt.figure(figsize=(10, 6))
        plt.plot(sorted_frequencies, normalized_vrms_db, marker='o', linestyle='-', color='b')
        plt.xscale('log')
        plt.grid(which='both', linestyle='--', linewidth=0.5)
        plt.title('Frequency Response (in dB)')
        plt.xlabel('Frequency (Hz)')
        plt.ylabel('Normalized Vrms (dB)')
        plt.axhline(0, color='r', linestyle='--', label=f'Reference ({self.reference_freq}Hz)')

        for freq, norm_vrms_db in zip(sorted_frequencies, normalized_vrms_db):
            plt.text(freq, norm_vrms_db, f'{freq}Hz', fontsize=8, ha='right', va='bottom')

        plt.legend()
        plt.show()


if __name__ == "__main__":
    # folder_path = '../data/frequency_response_ad7771'
    folder_path = '../data/frequency_response_ads131m08'

    analyzer = FrequencyResponseAnalyzer(folder_path)
    analyzer.plot()
