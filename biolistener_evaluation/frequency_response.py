# Frequency response

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

folder_path = '../data/frequency_response_ads131m08'

frequency_vrms = {}

for file_name in os.listdir(folder_path):
    if file_name.endswith('.csv'):
        # streamer_2024_12_26_15_44_52_ad7771_5Hz.csv -> 5Hz
        frequency = float(file_name.split('_')[-1].replace('Hz.csv', '').replace(',', '.'))

        file_path = os.path.join(folder_path, file_name)
        data = pd.read_csv(file_path, header=None, sep='\t')

        data = data.apply(lambda col: col.str.replace(',', '.')).astype('float64')

        channel = data[1]
        mean_removed = channel - channel.mean()

        # Compute Vrms (standard deviation of the mean-removed data)
        frequency_vrms[frequency] = mean_removed.std()

sorted_frequencies = sorted(frequency_vrms.keys())
sorted_vrms = [frequency_vrms[freq] for freq in sorted_frequencies]

# Normalize Vrms values relative to 5Hz (reference frequency)
reference_vrms = frequency_vrms[5.0]
normalized_vrms = [vrms / reference_vrms * 100 for vrms in sorted_vrms]

plt.figure(figsize=(10, 6))
plt.plot(sorted_frequencies, normalized_vrms, marker='o', linestyle='-', color='b')
plt.xscale('log')
plt.grid(which='both', linestyle='--', linewidth=0.5)
plt.title('Frequency Response')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Normalized Vrms (%)')
plt.axhline(100, color='r', linestyle='--', label='Reference (5Hz)')

for freq, norm_vrms in zip(sorted_frequencies, normalized_vrms):
    plt.text(freq, norm_vrms, f'{freq}Hz', fontsize=8, ha='right', va='bottom')

plt.legend()
plt.show()

# Convert normalized Vrms to dB taking 5Hz Vrms value as 0dB
normalized_vrms_db = [20 * np.log10(vrms / 100) for vrms in normalized_vrms]

plt.figure(figsize=(10, 6))
plt.plot(sorted_frequencies, normalized_vrms_db, marker='o', linestyle='-', color='b')
plt.xscale('log')
plt.grid(which='both', linestyle='--', linewidth=0.5)
plt.title('Frequency Response (in dB)')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Normalized Vrms (dB)')
plt.axhline(0, color='r', linestyle='--', label='Reference (5Hz)')

for freq, norm_vrms_db in zip(sorted_frequencies, normalized_vrms_db):
    plt.text(freq, norm_vrms_db, f'{freq}Hz', fontsize=8, ha='right', va='bottom')

plt.legend()
plt.show()
