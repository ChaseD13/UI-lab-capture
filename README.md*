# UI-lab-capture

An interface designed to make a scientists job easier by providing a  simple, yet effective way of setting up two USB3 BlackFly S cameras and starting their data collection from a Labjack U3-LV.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites
Run in a windows 10 environment using Anaconda 4.7.5 and python 3.7.3

- Spinnaker SDK
  - _Included in Additional docs_

- LabJackPython
  - _Included in Additional docs_

- Python 3
  - [Download](https://www.python.org/downloads/)

- Anaconda
  - [Download](https://www.anaconda.com/distribution/)

### Installing

#### Setting up the Anaconda environment-

1. Open the Anaconda prompt

2. Change directories:
```
cd (File path where repo was cloned or downloaded)\UI-lab-capture\Additional docs\Environments

For DONALDSON LAB:
cd Documents\UI-lab-capture\Additional Docs\Environments
```

3. Create the Anaconda Environment:
```
# IMPORTANT: Replace environmentName with the name you want for the environment

conda env create -f LabCaptureEnv.yml -n environmentName
```

4. Activate the environment:
```
# IMPORTANT: Replace environmentName with the name from the last step

conda activate environmentName
```

#### Install the Labjack API-

1. Change directories:
```
cd ..\LabJackPython-2.0.0\LabJackPython-2.0.0
```
  
2. Run the setup script
```
python setup.py install
```
  
3. Return to additional docs:
```
cd ..\..
```

#### Install the Spinnaker(PySpin) API-

1. Change directories:
```
# NOTE: For my env, version cp37-cp37m was used

cd Latest Python Spinnaker\Latest Python Spinnaker\spinnaker_python-1.23.0.27-cpxx-cpxxm-win_amd64
```
  
2. Install PySpin to your associated python version:
```
python -m pip install spinnaker_python-1.23.0.27-cpxx-cpxxm-win_amd64.whl
```

3. Return to main directory UI-lab-capture:
```
cd ..\..\..\..
```

## Running the GUI

Once back to the main diretory, type
```
cd Scripts
```
Then, to launch application type
```
python Master.py
```
The settings window will appear. The following explains each entry in the window.
```
Working Direcotry - EDITABLE Takes desired file path where experiment files will be saved.
                    ex. "C://Users/Protter/Documents/UI-lab-capture/Experiments/Experiment_1_60fps"
                    
Base File Name - EDITABLE Takes desired file name for the data file being outputed to by the GUI
                 ex. "Labjack_data"
                 
Active Directory - READ-ONLY Displays where the data output file will be saved. Used as a way to verify that the infomation inputed looks correct

Primary Camera Serial Number - EDITABLE Takes the serial number for the 'primary' Blackfly S Camera
```
Hit Submit once all of the entries have been filled in. The settings window will close and the main GUI will display. The following explains each entry in the window.
```
Labjack Scan Rate - EDITABLE Determines the scan frequency for the Labjack U3-LV

BlackFly FPS - READ-ONLY Determines the FPS for the video recording
```
Once you are ready to start the experiment, hit the start button towards the bottom of the window.

To stop the experiment, hit the stop button towards the bottom of the window. This will redirect you to the settings window. Here you can either start another experiment by repeating these steps or quit to desktop by closing the settings window.  

## Deployment

Additional notes about how to deploy this on a live system
```
Python 3.7.3
conda 4.7.5
```

## Built With

* [Anaconda](https://www.anaconda.com/) - Platform
* [Visual Studio](https://visualstudio.microsoft.com/) - IDE
* [Python](https://www.python.org/) - Code Language 
* [PySpin](https://www.flir.com/products/spinnaker-sdk/) - API for **USB3 Blackfly S Camera**
* [Labjack](https://labjack.com/support/software/api) - API for **Labjack U3-LV**


## Versioning

We use species for versioning. For the versions available, see the [tags on this repository](https://github.com/donaldsonlab/UI-lab-capture/tags). 

## Authors

* **Chase Dudas** - *GUI/Scripts* - [Personal GitHub](https://github.com/ChaseD13)
* Dave Protter - *Torubleshooting* - [Git](https://github.com/dprotter)

## License

This project is not licensed

## Acknowledgments

* Big thanks to **Kevin Chen** @ FLIR for helping troubleshoot issues with the Blackfly S cameras
* David Protter w/ Donaldson Lab
  * It’ll be running like a toyota carolla, FOREVER and basically flawlessly
