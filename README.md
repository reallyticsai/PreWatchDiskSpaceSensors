# Pre-Watch

A python service for making predictions based on historical sensor data from Oversight

## Getting Started

### Dependencies

* Python > 3.6
* pip

### Installing

```shell
pip install -r requirements.txt
```

### Executing program (locally)

```
python -m app.py
```

### Executing program (production)

```
docker-compose up -d
```

## Developing a new Predictive signal

### Step 1: Create a new script file in resources/plugins
```bash
touch resources/plugins/helloprediction.py
```

### Step 2: Create the standard plugin class
Note: You can find the boilerplate code in resources/plugins/boilerplate.py

1. The class name should be "Plugin"
```python
class Plugin:
```
2. There should be an __init__ constructor
```python
def __init__(self, dbservicefactory):
        self.dbservice = dbservicefactory.get_db_service()
        # you may add any other code here
```
3. There should be a "get_name" method. This method should return the name of your signal that you want to appear on Oversight UI.
```python
def get_name(self):
        return "Mongo Example Prediction"
```

4. There should be a "get_interval" method that return interval (in seconds) that this particular predicitve sensor must be executed
```python
def get_interval(self):
        return 60 #runs every ten seconds
```

5. There should be a "process" method that runs the main logic of your sensor. This method must return a tuple of (level,payload)
```python
def process(self):
    #do some magic here
    payload = {}
    return Levels.NORMAL,payload
```

### Step 3: Register the sensor in resources/active_plugins.py
Add the new plugin to the array
```python
plugins = [
    "something-something",
    "helloprediction"
]
```

## Creating an External plugin
An External plugin is practically created in the same way as a standard plugin but is intended to be deployed in a running instance (in production) of this service.

To create an external plugin follow these steps:
### Step 1: Create a new script file on the target machine at /etc/oversight/prewatch/externalplugins
```bash
touch /etc/oversight/prewatch/externalplugins/helloprediction.py
```

### Step 2: Follow Step 2 as in the above section

### Step 3: Add the file name to the environment variable (PW_EXTERNAL_PLUGINS) in the docker-compose file as a comma-separated list
```
environment:
      - PW_OV_VERSION=1
      - PW_EXTERNAL_PLUGINS=something,helloprediction
```

### Step 4: Rebuild the service
```
docker-compose up -d --build
```



## Authors
Syed Muhammad Haris  
muhammad.haris@afiniti.com

## Version History

* 1.0.0
    * Initial release