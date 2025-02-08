# Input Referred Noise (IRN)

import pandas as pd
import matplotlib.pyplot as plt


class IRNAnalyzer:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.data = None
        self.mean_removed = None
        self.irn_results = {}

        self.load_data()
        self.compute_irn()

    def load_data(self):
        self.data = pd.read_csv(self.file_path, header=None, sep='\t')
        self.data = self.data.drop(columns=[0, 9, 10, 11, 12])
        self.data = self.data.apply(lambda col: col.str.replace(',', '.')).astype('float64')
        self.mean_removed = self.data - self.data.mean()

    def compute_irn(self):
        """Calculate accurate and approximated Input-Referred Noise (IRN)."""
        for channel in self.mean_removed.columns:
            channel_data = self.mean_removed[channel]
            self.irn_results[channel] = {
                'accurate': channel_data.max() - channel_data.min(),  # Accurate IRN (peak-to-peak) calculation
                'std_approx': channel_data.std() * 6  # Approximation of IRN with standard deviation using ±3σ (99.73%)
            }

    def display_results(self):
        print("Input-Referred Noise (IRN) for each channel:")
        for channel, results in self.irn_results.items():
            print(f"Ch {channel}: Accurate = {results['accurate']:.6f} µV, "
                  f"STD ±3σ (99.73%) = {results['std_approx']:.6f} µV")

        max_irn = max(results['accurate'] for results in self.irn_results.values())
        max_irn_std = max(results['std_approx'] for results in self.irn_results.values())

        print(f"Maximum IRN (Accurate): {max_irn:.6f} µV")
        print(f"Maximum IRN (STD ±3σ): {max_irn_std:.6f} µV")

    def plot(self):
        n_channels = len(self.mean_removed.columns)
        ncols = 4
        nrows = (n_channels + 3) // ncols

        fig, axes = plt.subplots(nrows, ncols, figsize=(14, 6 * nrows))
        fig.suptitle('Input-Referred Noise (IRN) Histograms', fontsize=16)

        axes = axes.flatten()

        for i, (channel, ax) in enumerate(zip(self.mean_removed.columns, axes)):
            ax.hist(self.mean_removed[channel], bins=50, color='skyblue', edgecolor='black')
            ax.set_title(f"Histogram of Noise - Ch {channel}")
            ax.set_xlabel("Noise Amplitude (µV)")
            ax.set_ylabel("Frequency")
            ax.grid()

        for j in range(i + 1, len(axes)):
            axes[j].axis('off')

        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    # file_path = '../data/irn/streamer_2024_12_26_18_36_10_ads131m08_test_3_dgnd.csv'
    file_path = '../data/irn/streamer_2024_12_25_21_55_32_ad7771_test_2.csv'

    analyzer = IRNAnalyzer(file_path)

    analyzer.display_results()
    analyzer.plot()
