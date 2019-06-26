# UI-lab-capture

An interface designed to make a scientists job easier by providing a  simple, yet effective way of setting up two USB3 BlackFly S cameras and starting their data collection from a Labjack U3-LV.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

What things you need to install the software and how to install them

- Spinnaker SDK

- LabJackPython

- Python 3

- Anaconda

### Installing

#### Setting up the Anaconda environment-

1. Open the Anaconda prompt

2. Change directories:
  - **cd (File path where repo was cloned or downloaded)\UI-lab-capture\Additional docs**

3. Create the Anaconda Environment:
  - **conda env create -f LabCaptureEnvironment.yml -n environmentName**
    - _Replace environmentName with the name you want for the environment_

4. Activate the environment:
  - **conda activate environmentName**
    - _Replace environmentName with the name from the last step_

#### Install the Labjack API-

1. Change directories:
  - **cd (current directory)\LabJackPython-2.0.0\LabJackPython-2.0.0**
  
2. Run the setup script
  - **python setup.py install**
  
3. Return to additional docs:
  - **cd ..\..**

#### Install the Spinnaker(PySpin) API-

1. Change directories:
  - **cd (current directory)\Latest Python Spinnaker\Latest Python Spinnaker\spinnaker_python-1.23.0.27-cpxx-cpxxm-win_amd64**
    - _For my env, version cp37-cp37m was used_
  
2. Install PySpin to your associated python version:
  - **python -m pip install spinnaker_python-1.23.0.27-cpxx-cpxxm-win_amd64.whl**

3. Return to main directory UI-lab-capture:
  - **cd ..\..\..\..**

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

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 

## Authors

* **Billie Thompson** - *Initial work* - [PurpleBooth](https://github.com/PurpleBooth)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration
* etc
