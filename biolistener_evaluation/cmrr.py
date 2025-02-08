# Common Mode Rejection Ratio (CMRR)

import os
from math import log10

import pandas as pd
import matplotlib.pyplot as plt


class CMRRAnalyzer:
    def __init__(self, folder_path: str, gen_voltage_vrms: float = 3.5):
        self.folder_path = folder_path
        self.reference_voltage = gen_voltage_vrms
        self.frequency_vrms = {}
        self.volts_to_microvolts = 1_000_000

        self.process_files()

    def process_files(self):
        for file_name in os.listdir(self.folder_path):
            if file_name.endswith('.csv'):
                frequency = self._extract_frequency(file_name)
                file_path = os.path.join(self.folder_path, file_name)
                self.frequency_vrms[frequency] = self._compute_vrms(file_path)

    def _extract_frequency(self, file_name: str) -> float:
        """Extract frequency value from the file name."""
        # streamer_2024_12_26_15_44_52_ad7771_5Hz.csv -> 5Hz
        return float(file_name.split('_')[-1].replace('Hz.csv', '').replace(',', '.'))

    def _compute_vrms(self, file_path: str) -> float:
        """Compute Vrms (standard deviation) of the mean-removed data."""
        data = pd.read_csv(file_path, header=None, sep='\t')
        data = data.apply(lambda col: col.str.replace(',', '.')).astype('float64')
        channel = data.drop(columns=[0, 9, 10, 11, 12])
        mean_removed = channel - channel.mean()
        return max(mean_removed.std())

    def compute_cmrr(self) -> dict:
        """Compute the CMRR in dB."""
        return {
            freq: 20 * log10((vrms * 2 * 2 ** 0.5) / (self.reference_voltage * self.volts_to_microvolts))
            for freq, vrms in self.frequency_vrms.items()
        }

    def plot(self):
        cmrr_db = self.compute_cmrr()
        sorted_frequencies = sorted(cmrr_db.keys())
        sorted_cmrr_db = [cmrr_db[freq] for freq in sorted_frequencies]

        plt.figure(figsize=(10, 6))
        plt.plot(sorted_frequencies, sorted_cmrr_db, marker='o', linestyle='-', color='b')
        plt.xscale('log')
        plt.grid(which='both', linestyle='--', linewidth=0.5)
        plt.title('CMRR vs Frequency')
        plt.xlabel('Frequency (Hz)')
        plt.ylabel('CMRR (dB)')

        for freq, cmrr in zip(sorted_frequencies, sorted_cmrr_db):
            plt.text(freq, cmrr, f'{freq}Hz', fontsize=8, ha='right', va='bottom')

        plt.show()


if __name__ == "__main__":
    folder_path = '../data/cmrr/cmrr_imbalance_ad7771'
    # folder_path = '../data/cmrr/cmrr_imbalance_ads131m08'

    analyzer = CMRRAnalyzer(folder_path)
    analyzer.plot()
