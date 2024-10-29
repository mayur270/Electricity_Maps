# SmartestEnergy

- PYTHON_VERSION: 3.11
- IDE: PyCharm

## Problem Statement
Calculate the known carbon intensity (in gCO2eq/kWh) of electricity consumed in the UK 
using the Electricity Maps API for the last 24 hours.

This information can be retrieved from https://docs.electricitymaps.com/#recent-carbon-intensity-history 
and will be displayed in a csv file.

## Structure of application
```
SmartestEnergyTask/
│  
├── models/
│   ├── __init__.py
│   └── carbon_intensity_history_model.py       # Pydantic models for data validation
│
├── results/
│   └── carbon_intensity_20241028_120304.csv    # CSV File
│
├── tests/                                      # Unit tests and test cases
│   ├── __init__.py
│   ├── test_carbon_intensity_history.py        # Tests for carbon_intensity_history_view.py
│   └── test_util.py                            # Tests for util.py
│
├── utils/             
│   ├── __init__.py
│   ├── api_client.py                           # Get request class
│   └── util.py                                 # All other utils
│ 
├── views/                          
│   ├── __init__.py
│   ├── abstract_base.py                        # Abstract base models
│   └── carbon_intensity_history_view.py        # Calculates total carbon intensity 24h
│
├── config.py                                   # Env variable settings
├── endpoints.py                                # All endpoints of application
├── exceptions.py                               # Custom exceptions
├── log.py                                      # Logging configuration
├── main.py                                     # Entrypoint to application
├── README.md                                   # Project documentation
└── requirements.txt                            # Dependencies required for the project
```

## Run Application
1. Create Virtual Environment ```python3.11 -m venv venv```. 
2. Then activate venv: ```source venv/bin/activate```
3. Install all the dependencies ```pip install -r requirements.txt```
4. Create '.env' file in root folder and add env variables e.g. 
    ```
    LOGGING_LEVEL=<currently_set_to_DEBUG>
    ```
5. Run the application```python main.py```
6. Check the 'results' folder where .csv file is stored with date and time.

## Test Application
1. Run ```pytest``` in CLI
