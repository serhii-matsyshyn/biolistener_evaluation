# Signal to Noise Ratio (SNR)

import os

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.signal import find_peaks


def calculate_snr(signal, sampling_rate):
    n = len(signal)
    fft_result = np.fft.fft(signal)
    freqs = np.fft.fftfreq(n, d=1 / sampling_rate)
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

    snr_db = 10 * np.log10(signal_power / noise_power)

    return snr_db, signal_freq


folder_path = '../data/frequency_response_ad7771'

frequency_snr = {}

for file_name in os.listdir(folder_path):
    if file_name.endswith('.csv'):
        # streamer_2024_12_26_15_44_52_ad7771_5Hz.csv -> 5Hz
        frequency = float(file_name.split('_')[-1].replace('Hz.csv', '').replace(',', '.'))

        file_path = os.path.join(folder_path, file_name)
        data = pd.read_csv(file_path, header=None, sep='\t')

        data = data.apply(lambda col: col.str.replace(',', '.')).astype('float64')

        channel = data[1]
        mean_removed = channel - channel.mean()

        sampling_rate = 500  # Hz

        snr, freq = calculate_snr(mean_removed, sampling_rate)

        # print(f"Estimated SNR: {snr:.2f} dB")
        # print(f"Signal Frequency: {freq:.2f} Hz")

        frequency_snr[frequency] = snr

        # t = np.arange(len(mean_removed)) / sampling_rate
        # plt.figure(figsize=(12, 6))
        # plt.subplot(2, 1, 1)
        # plt.plot(t, mean_removed)
        # plt.title("Time-Domain Signal")
        # plt.xlabel("Time (s)")
        # plt.ylabel("Amplitude")
        #
        # plt.subplot(2, 1, 2)
        # fft_magnitude = np.abs(np.fft.fft(mean_removed)[:len(mean_removed)//2])
        # freqs = np.fft.fftfreq(len(mean_removed), d=1/sampling_rate)[:len(mean_removed)//2]
        # plt.plot(freqs, fft_magnitude)
        # plt.title("Frequency Spectrum")
        # plt.xlabel("Frequency (Hz)")
        # plt.ylabel("Magnitude")
        # plt.tight_layout()
        # plt.show()

sorted_frequencies = sorted(frequency_snr.keys())
sorted_snr = [frequency_snr[freq] for freq in sorted_frequencies]

plt.figure(figsize=(10, 6))
plt.plot(sorted_frequencies, sorted_snr, marker='o', linestyle='-', color='b')
plt.xscale('log')
plt.grid(which='both', linestyle='--', linewidth=0.5)
plt.title('SNR (in dB)')
plt.xlabel('Frequency (Hz)')
plt.ylabel('SNR (dB)')

for freq, norm_vrms_db in zip(sorted_frequencies, sorted_snr):
    plt.text(freq, norm_vrms_db, f'{freq}Hz', fontsize=8, ha='right', va='bottom')

plt.show()
