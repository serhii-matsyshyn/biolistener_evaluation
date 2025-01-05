# BioListener - Evaluation

This repository contains code, programs, data records (for both, evaluation of main boards parameters and experimental setups for real-world evaluation) necessary for BioListener evaluation and demonstration.

Boards evaluated are based on:
- ADC AD7771 (Analog Devices)
- ADC ADS131M08 (Texas Instruments)

Parameters evaluated:
- Input Referred Noise (IRN)
- Frequency Response
- Signal to Noise Ratio (SNR)
- Common Mode Rejection Ratio (CMRR)
  - Balance test
  - Imbalance test

Experimental setups for real-world evaluation:
- EMG - Fist Clenching
- ECG - 1 Channel
- ECG - 5 Channel
- EEG, EMG - Alpha Brain Wave, Eye Blink


## Useful commands
```shell
sudo netstat -tulnap | grep 12345

sudo ./busy_sockets_clear.sh
```