![BioListener Logo](data/images/BioListener_Logo_1920х200.jpg "BioListener Logo")

# BioListener - Evaluation

This BioListener evaluation repository contains the necessary code, programs, data records, and experimental setups required for evaluating BioListener main board parameters and performing real-world demonstrations.

<p align="center">
  <img alt="BioListener V1.0 Boards 3D Printed Case Prototypes" src="data/images/BioListener_board_v1.0.jpg" width="600">
</p>

## Boards Evaluated

Boards evaluated are based on:
- ADC AD7771 (Analog Devices)
- ADC ADS131M08 (Texas Instruments)

### Parameters Evaluated

The evaluation covers key parameters:
- **Input Referred Noise (IRN)**
- **Frequency Response**
- **Signal to Noise Ratio (SNR)**
- **Common Mode Rejection Ratio (CMRR)**
  - Balance test
  - Imbalance test
- **Inputs impedance**

### Experimental Setups for Real-World Evaluation

- **Electromyography (EMG)**: Fist Clenching
- **Electrocardiography (ECG)**: 1 Lead
- **Electrocardiography (ECG)**: 5 Lead
- **Electroencephalography (EEG) and EMG**: Alpha Brain Wave and Eye Blink Detection

## Usage examples
Ensure the board is connected to the same WiFi network as the device running the BrainFlow server.  
**Default port**: `12345`  
The server listens on all interfaces by default.  


### Measure Data Frequency
To measure data frequency (in Hz) of data received from BioListener board:
```shell
python measure_brainflow_data_frequency.py
```

### Plot Data in Real-Time
To plot data in real time, with recording interface available:
```shell
python plot_real_time_with_recording.py
```

### OpenBCI GUI
To bind to OpenBCI GUI, use previous command. The streaming board is created at  
`streaming_board://225.1.1.1:6677`  
_Note_: Customized OpenBCI GUI is required. Future integration with the official GUI is planned.

## Boards evaluation
Evaluation scripts are located in `biolistener_evaluation` directory.  
See [biolistener_evaluation.ipynb](biolistener_evaluation.ipynb) for detailed evaluation results.

**Evaluation Data**: Located in the `data` directory.

> [!NOTE]
> Take note! The following Boards evaluation plots, descriptions, data is **Work In Progress** and will be moved in the future to the Jupiter Notebook and described fully. At the moment, only short descriptions are provided. Stay tuned!

| Equipment                                                      | Description and Images                                                                                                         |
|----------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------|
| Hantek DSO2C10 Digital Storage Oscilloscope                    | Has built-in signals generator (oscilloscope was updated to DSO2D15 firmware)                                                  |
| Hantek PP-150 100MHz 1:1 / 10:1 Oscilloscope Probes            |                                                                                                                                |
| Fnirsi P4100 100MHz 100:1 Oscilloscope Probes                  | High impedance probe                                                                                                           |
| Custom connectors, cables, and adapters                        |                                                                                                                                |
| Evaluation Helper PCB with soldered on test specific circuitry |                                                                                                                                |
| Golden Cup Passive Electrodes, ECG/EEG Gel                     | <img src="data/images/evaluation/equipment/golden_cup_passive_electrodes.jpg" alt="Golden Cup Passive Electrodes" width="250"> |
| Snap Patch Passive Electrodes                                  | <img src="data/images/evaluation/equipment/patch_electrodes.jpg" alt="Snap Patch Passive Electrodes" width="250">              |


### Evaluation setups
The following test setups were used for evaluation:
#### Input Referred Noise (IRN)
![Input Referred Noise (IRN) setup](data/images/evaluation/evaluation_setups/irn_setup.jpg)

All the input ADC channels were shorted together and with device ground.

#### Frequency Response
![Frequency Response setup](data/images/evaluation/evaluation_setups/frequency_response_setup.jpg)

<p align="center">
  <img alt="Frequency Response Schematic" src="data/images/evaluation/schematics/Frequency_Response_and_SNR.jpg" width="400">
</p>

#### Signal to Noise Ratio (SNR)
Calculated on data collected during Frequency Response test.

#### Common Mode Rejection Ratio (CMRR) Balance
![Common Mode Rejection Ratio (CMRR) Balance setup](data/images/evaluation/evaluation_setups/cmrr_balance_setup.jpg)

<p align="center">
  <img alt="Common Mode Rejection Ratio (CMRR) Balance Schematic" src="data/images/evaluation/schematics/cmrr_balance.jpg" width="400">
</p>


#### Common Mode Rejection Ratio (CMRR) Imbalance
![Common Mode Rejection Ratio (CMRR) Imbalance setup](data/images/evaluation/evaluation_setups/cmrr_imbalance_setup.jpg)

<p align="center">
  <img alt="Common Mode Rejection Ratio (CMRR) Imbalance Schematic" src="data/images/evaluation/schematics/cmrr_imbalance.jpg" width="400">
</p>

#### Inputs impedance
![Inputs impedance setup](data/images/evaluation/evaluation_setups/inputs_impedance_setup.jpg)

<p align="center">
  <img alt="Inputs impedance Schematic" src="data/images/evaluation/schematics/Channel_Impedance_Test.jpg" width="400">
</p>

### Evaluation results
**See [biolistener_evaluation.ipynb](biolistener_evaluation.ipynb) for detailed evaluation results.**

### Real-world Evaluation setups

#### EMG - Fist Clenching
Channel 1 is used. All other channels are disabled. Preferable electrodes for this setup are Snap Patch Passive Electrodes (though Golden Cup Passive Electrodes can be used as well, and they were mainly used for this test setup).

![EMG - Fist Clenching](data/images/experimental_setup/BioListener_emg_fist_clenching.jpg)

#### ECG - 1 Lead
Standard ECG 1 lead setup.

#### ECG - 5 Lead
Standard ECG 5 lead setup.

#### EEG, EMG - Alpha Brain Wave, Eye Blink

![EEG, EMG - Alpha Brain Wave, Eye Blink](data/images/experimental_setup/BioListener_eeg_emg_alpha_brain_wave_eye_blink.jpg)


### ADC AD7771 (Analog Devices)

#### EMG - Fist Clenching
Channel 1 is used. All other channels are disabled.

![EMG - Fist Clenching Plot](data/images/ad7771/ad7771_emg_fist_clenching_plot.jpg)


#### ECG - 1 Lead

![ECG - 1 Lead Plot](data/images/ad7771/ad7771_ecg_1_lead_plot.jpg)

#### ECG - 5 Lead

![ECG - 5 Lead Plot](data/images/ad7771/ad7771_ecg_5_lead_plot.png)

#### EEG, EMG - Alpha Brain Wave, Eye Blink


![EEG, EMG - Alpha Brain Wave, Eye Blink Plot](data/images/ad7771/ad7771_eeg_emg_alpha_brain_wave_eye_blink_plot.jpg)

### ADC ADS131M08 (Texas Instruments)

#### EMG - Fist Clenching

![EMG - Fist Clenching Plot](data/images/ads131m08/ads131m08_emg_fist_clenching_plot.jpg)


#### ECG - 1 Lead

![ECG - 1 Lead Plot](data/images/ads131m08/ads131m08_ecg_1_lead_plot_32x.png)

#### ECG - 5 Lead

![ECG - 5 Lead Plot](data/images/ads131m08/ads131m08_ecg_5_lead_plot_32x.png)

#### EEG, EMG - Alpha Brain Wave, Eye Blink

![EEG, EMG - Alpha Brain Wave, Eye Blink Plot](data/images/ads131m08/ads131m08_eeg_emg_alpha_brain_wave_eye_blink_plot.jpg)


## Useful commands
To check active sockets on port **12345**:
```shell
sudo netstat -tulnap | grep 12345
```

To clear busy sockets:
```shell
sudo ./busy_sockets_clear.sh
```

## License

This repository uses the following licenses:

- **Code**: The code in this repository is licensed under the [GNU General Public License v3.0 (GPL-3.0)](https://www.gnu.org/licenses/gpl-3.0.html).
  
- **Experimental Data**: The experimental data (e.g., images, data records) is licensed under the [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/).
