# Common Mode Rejection Ratio (CMRR)

import os
from math import log10

import pandas as pd
import matplotlib.pyplot as plt

folder_path = '../data/cmrr_imbalance_ad7771'
# folder_path = '../data/cmrr_imbalance_ads131m08'

frequency_vrms = {}

for file_name in os.listdir(folder_path):
    if file_name.endswith('.csv'):
        # streamer_2024_12_26_15_44_52_ad7771_5Hz.csv -> 5Hz
        frequency = float(file_name.split('_')[-1].replace('Hz.csv', '').replace(',', '.'))

        file_path = os.path.join(folder_path, file_name)
        data = pd.read_csv(file_path, header=None, sep='\t')

        data = data.apply(lambda col: col.str.replace(',', '.')).astype('float64')

        channel = data.drop(columns=[0, 9, 10, 11, 12])
        mean_removed = channel - channel.mean()

        # Compute Vrms (standard deviation of the mean-removed data)
        frequency_vrms[frequency] = max(mean_removed.std())

cmrr_db = {
    key: 20 * log10((value * 2 * 2 ** 0.5) / (1 * 1000000)) for key, value in frequency_vrms.items()
}

# for key, value in cmrr_db.items():
#     print(key, value)

sorted_frequencies = sorted(cmrr_db.keys())
sorted_cmrr_db = [cmrr_db[freq] for freq in sorted_frequencies]

plt.figure(figsize=(10, 6))
plt.plot(sorted_frequencies, sorted_cmrr_db, marker='o', linestyle='-', color='b')
plt.xscale('log')
plt.grid(which='both', linestyle='--', linewidth=0.5)
plt.title('CMRR vs Frequency')
plt.xlabel('Frequency (Hz)')
plt.ylabel('CMRR (dB)')
# plt.axhline(0, color='r', linestyle='--', label='Reference')

for freq, norm_vrms_db in zip(sorted_frequencies, sorted_cmrr_db):
    plt.text(freq, norm_vrms_db, f'{freq}Hz', fontsize=8, ha='right', va='bottom')

plt.show()
