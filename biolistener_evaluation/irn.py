# Input Referred Noise (IRN)

import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv(
    '../data/irn/streamer_2024_12_26_18_36_10_ads131m08_test_3_dgnd.csv',
    # '../data/irn/streamer_2024_12_25_21_55_32_ad7771_test_2.csv',
    header=None, sep='\t'
)

channels = data.drop(columns=[0, 9, 10, 11, 12]).apply(lambda col: col.str.replace(',', '.')).astype('float64')

mean_removed = channels - channels.mean()

irn_results = {}

for channel in mean_removed.columns:
    channel_data = mean_removed[channel]

    irn_results[channel] = {
        'accurate': channel_data.max() - channel_data.min(),  # Accurate IRN (peak-to-peak) calculation
        'std_approx': channel_data.std() * 6  # Approximation using standard deviation
    }

print("Input-Referred Noise (IRN) for each channel:")
for channel, results in irn_results.items():
    print(f"{channel}: Accurate = {results['accurate']:.6f} µV, STD ±3σ (99.73%) = {results['std_approx']:.6f} µV")

# # FIXME: Vrms without removing the mean - wrong, dc offset not taken in account
# vrms_with_mean = (channels ** 2).mean() ** 0.5
# print(f"Vrms for each channel (including mean): {vrms_with_mean}")

# Vrms with mean removed - way to fix
vrms_mean_removed = mean_removed.std()
print(f"Vrms for each channel (mean removed): {vrms_mean_removed}")

n_channels = len(mean_removed.columns)
ncols = 4
nrows = (n_channels + 3) // ncols

fig, axes = plt.subplots(nrows, ncols, figsize=(14, 6 * nrows))

fig.suptitle('Input-Referred Noise (IRN) Histograms', fontsize=16)

axes = axes.flatten()

for i, (channel, ax) in enumerate(zip(mean_removed.columns, axes)):
    ax.hist(mean_removed[channel], bins=50, color='skyblue', edgecolor='black')
    ax.set_title(f"Histogram of Noise - Ch {channel}")
    ax.set_xlabel("Noise Amplitude (µV)")
    ax.set_ylabel("Frequency")
    ax.grid()

for j in range(i + 1, len(axes)):
    axes[j].axis('off')

plt.tight_layout()
plt.show()
