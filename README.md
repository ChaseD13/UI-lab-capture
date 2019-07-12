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
cd (File path where repo was cloned or downloaded)\UI-lab-capture\Additional docs
```

3. Create the Anaconda Environment:
```
# Replace environmentName with the name you want for the environment

conda env create -f LabCaptureEnvironment.yml -n environmentName
```

4. Activate the environment:
```
# Replace environmentName with the name from the last step

conda activate environmentName
```

#### Install the Labjack API-

1. Change directories:
```
cd (current directory)\LabJackPython-2.0.0\LabJackPython-2.0.0
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
# For my env, version cp37-cp37m was used

cd (current directory)\Latest Python Spinnaker\Latest Python Spinnaker\spinnaker_python-1.23.0.27-cpxx-cpxxm-win_amd64
```
  
2. Install PySpin to your associated python version:
```
python -m pip install spinnaker_python-1.23.0.27-cpxx-cpxxm-win_amd64.whl
```

3. Return to main directory UI-lab-capture:
```
cd ..\..\..\..
```

## Running the tests

Explain how to run the automated tests for this system

### Break down into end to end tests

Explain what these tests test and why

```
Give an example
```

### And coding style tests

Explain what these tests test and why

```
Give an example
```

## Deployment

Add additional notes about how to deploy this on a live system

## Built With

* [Dropwizard](http://www.dropwizard.io/1.0.2/docs/) - The web framework used
* [Maven](https://maven.apache.org/) - Dependency Management
* [ROME](https://rometools.github.io/rome/) - Used to generate RSS Feeds


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
