# pyboltwood 

A [Boltwood Cloud Sensor III](https://diffractionlimited.com/cloud-sensor/) Serial API wrapper for Python

Copyright 2024 Diffraction Limited

# Requirements

- Python 3.10 or above
- PySerial 3.5 or above

# Getting Started
## Installing dependencies
> **NOTE:** This guide assumes you have Python 3.10 or greater installed on your system with the installation added to your PATH environment variable, and are familiar with basic Python toolchain tools like PyPI. You can verify this by executing:

```
>> python --version
Python 3.11.8 (tags/v3.11.8:db85d51, Feb  6 2024, 22:03:32) [MSC v.1937 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
```

Begin by downloading the latest Boltwood Python package PyPI:

```
pip install pyboltwood
``` 

You can then import the library into your code using:

```python
from pyboltwood import *
```

## Determining the Boltwood's serial port
In order to communicate with your Boltwood, you need to discover which port the device is connected to. Unfortunately, every operating system has a different way of presenting serial port access, so you'll need to familiarize yourself with the process for your environment.

### Windows
Windows list connected serial devices in the Device Manager under "Ports (COM & LPT)". Boltwood devices list as "USB Serial Port (COM#)", where "COM#" will be something like "COM3". That value is the port you'll be addressing when you create the `Boltwood` class instance.

### Ubuntu 22.04 LTS
Linux drivers list their serial devices in the `/dev` folder. Our serial converters will typically list as `/dev/ttyUSB#` where "ttyUSB#" will be something like "ttyUSB0". This file needs to be given read/write privileges. This can be achieved with the following command:

```bash
$ sudo usermod -a -G dialout $USER
```

where you replace `$USER` with your user account name.

## The serial API
The boltwood package attempts to reflect the Boltwood serial API as closely as possible. The API is designed to operate similarly to a thinned down HTTP protocol where requests have a verb (e.g. "G" for Get) followed by an interface endpoint (e.g. "DD" for Device Descriptor) followed by a property (e.g. "serial" for Serial Number) and optionally a value. Responses will always have a status code and optionally a return value or error message in the event the message is a failure.

Messages are case insensitive and must be terminated by a linefeed character (`\n`). 

### Requests
Requests have the following structure:

```verb interface parameter [value]\n```

Where `verb` can be:

- `G` for "Get", used for retrieving readable properties on a supplied interface
- `P` for "Put", used for updating writable properties on a supplied interface

`interface` can be:

- `OC` for "Observing Conditions", reflecting the ASCOM Observing Conditions interface
- `SM` for "Safety Monitor", reflecting the ASCOM Safety Monitor interface
- `DD` for "Device Descriptor", used for identifying information and user device settings
- `EN` for "Engineering Data", used to access raw sampling and condition data

`parameter` is interface dependent. Properties for the various interfaces are documented in the `ObservingConditions`, `SafetyMonitor`, `DeviceDescriptor`, and `EngineeringData` classes below.

`value` is an optional parameter (required for Put requests) that supplies the value to pass to the Boltwood.

### Responses
Responses have the following structure:

```status_code [value|error_message]\n```

Where `status_code` can be:

- `0` for Success
- `1` for Client Error (the command supplied was invalid)
- `2` for Server Error (the device was unable to comply with the command)

`value` is provided on `status_code` success for Get requests, and is the value obtained from the Boltwood.

`error_message` is a human-readable error message returned when `status_code` is non-zero describing the encountered error in detail.

### Examples
Retrieving a serial number

```
>> G DD SERIAL
0 BCS3S24010203\n
```

Setting up your wireless connection
```
>> P DD STA_SSID MyObservatorySSID\n
0

>> P DD STA_PASS MySuperSecurePassword\n
0
```

Retrieving all Engineering Data properties at once
```
>> G EN ALL\n
0 20 0 ...
```

Attempting to set a read-only property (worth a shot)
```
>> P OC TEMPERATURE 21\n
1 Invalid Argument: property 'temperature' is read-only.
```


## Python wrappers
The Python wrapper `Boltwood` class acts as a controller that executes your verbs: "Get" via `Boltwood.get()` and "Put" via `Boltwood.put()`. You can then access the various interfaces and properties via access keys supplied as parameters to those functions. Interface access keys are defined as class variables in the `Interfaces` class, while Property access keys are defined as class variables in the `ObseringConditions`, `SafetyMonitor`, `DeviceDescriptor`, and `EngineeringData` classes.

These wrapper functions return a tuple where the first entry is `True` or `False` depending on whether the command succeeded, and the second entry is either the value retrieved (if a value was requested/retrieved) or an error message (if the command failed).

### Examples

Retrieving a serial number
```python
>>> bcs = Boltwood("COM1")
>>> bcs.open()
>>> bcs.get(Interfaces.DD, DeviceDescriptor.SERIAL)
(True, "BCS3S24010203") # Success
```

Setting up your wireless connection
```python
>>> bcs = Boltwood("COM1")
>>> bcs.open()
>>> bcs.put(Interfaces.DD, DeviceDescriptor.STA_SSID, "MyObservatorySSID")
(True, "") # Success
>>> bcs.put(Interfaces.DD, DeviceDescriptor.STA_PASS, "MySuperSecurePassword")
(True, "") # Success
```

Attempting to set a read-only property (a man can dream...)
```python
>>> bcs = Boltwood("COM1")
>>> bcs.open()
>>> bcs.put(Interfaces.OC, ObservingConditions.TEMPERATURE, 21)
(False, "Invalid argument: property 'temperature' is read-only.") # Error: Invalid argument
```

### Convenience Accessors
We've also wrapped the interface accessors into their own functions:

- `Boltwood.getOC()` 
- `Boltwood.putOC()`
- `Boltwood.getSM()`
- `Boltwood.getDD()`
- `Boltwood.putDD()`
- `Boltwood.getEN()`

Where you can pass an interface access key as a parameter to the function to retrieve/set properties depending on their permissions.

```python
# Interface accessor wrappers
>>> from pyboltwood import Boltwood, EngineeringData

>>> bcs = Boltwood("COM1")
>>> bcs.open()
>>> bcs.getDD(DeviceDescriptor.SERIAL)
(True, 'BCS3S24010203') # Success
```

### Amalgamation Accessors
We've provided convenience accessors for interface amalgamators that return the entire interface property listings:

- `Boltwood.getOCAll()`
- `Boltwood.getENAll()`

These functions can be used in conjunction with their respective access key wrapper classes to parse the output safely:

```python
# Parsing Engineering Data amalgamator
>>> rc, data = bcs.getENAll()
>>> if rc == True: 
>>>    print(f'Failed to retrieve Engineering Data: {data}')
>>>    exit(1)
>>> ed = EngineeringData(data)
>>> ed[EngineeringData.AMBIENT_TEMP]
"-10"

# Parsing the Observing Conditions amalgamator
>>> rc, data = bcs.getOCAll()
>>> if rc == True: 
>>>     print(f'Failed to retrieve Observing Conditions: {data}')
>>>     exit(1)

>>> oc = ObservingConditions(data)
"-10"
```

## Your first program
Once you've installed boltwood.py's dependencies and determined the port your Boltwood is connected to, you can write your first application. Create a new directory and place "boltwood.py" in it. Then create a new file, named "example.py" and paste the following code into it:

```python
# example.py
from pyboltwood import Boltwood, DeviceDescriptor

# Sets up a Boltwood instance on Windows COM port `"COM1"` 
# and open the connection. Always wrap your code in a try-except
# block to prevent abnormal program termination
try:
    bcs = Boltwood("COM1")
    bcs.open()

    # Attempt to retrieve Device Descriptor's Serial property, handle any errors
    rc, value = bcs.get(Interface.DD, DeviceDescriptor.SERIAL)
    if not rc:
        # Print the supplied error message to screen
        print(f'There was an error retrieving your device\'s serial number: {value}')
        exit(1)

    # Print the device's returned serial number
    print(f'Success! {value}')
except:
    print("Failed to connect to Boltwood CSIII")

```

Be sure to update `"COM1"` with whatever serial port identifier your environment requires to communicate with your device.

## Accessing Thresholds & Safety Triggers

Thresholds and Safety Triggers are programmable via the serial API. These values represent transitions between two conditions (e.g. `Thresholds.CLEAR_CLOUDY` is the value of Sky-Ambient where the cloud sensor transitions from "Clear" to "Cloudy"), and whether they are used to determine the safe/unsafe condition and trigger the roof close signal. You can access them via the Observing Conditions interface, and we've provided a reflection class that parses the response string from the Boltwood CSIII into a dictionary of threshold and safety trigger values. You can use the `Thresholds.threshValue` class variable to look-up what value will trigger a given condition (e.g. `Thresholds.CLEAR_CLOUDY`) and use `Thresholds.roofTrig` to check whether that condition is actively used as a safety trigger.

Retrieving device thresholds/safety triggers:

```python
# Load Boltwood library and connect to device
>>> from pyboltwood import Boltwood, Thresholds
>>> bcs = Boltwood("COM1")
>>> bcs.open()

# Obtain thresholds from the device and parse them using our Thresholds reflection class 
>>> rc, raw_values = bcs.getOCThresholds()
>>> values = Thresholds(raw_values)

# Access the parsed values by transition access key
>>> values.threshValue[Thresholds.CLEAR_CLOUDY] # Access threshold's value
-10
>>> values.roofTrig[Thresholds.CLEAR_CLOUDY] # Access whether transition is active as safety trigger
0
>>> values[Thresholds.CLEAR_CLOUDY] # Access tuple of threshold value & safety trigger
(-10, 0)
```

Updating a threshold/safety trigger:

```python
# Load Boltwood library and connect to device
>>> from pyboltwood import Boltwood, Thresholds
>>> bcs = Boltwood("COM1")
>>> bcs.open()

# Obtain thresholds from the device and parse them using our Thresholds reflection class 
>>> rc, raw_values = bcs.getOCThresholds()
>>> values = Thresholds(raw_values)

# Update the desired threshold from -10 degrees Celcius to -15, and set it as an active safety trigger
>>> values.threshValue[Thresholds.CLEAR_CLOUDY] = -15
>>> values.roofTrig[Thresholds.CLEAR_CLOUDY] = 1

# Submit changes to Boltwood
>>> bcs.putOCThresholds(values.to_string())
(True, "") # Success
```

# License
This software is licensed under the MIT License.

```text
Copyright 2024 Diffraction Limited

Permission is hereby granted, free of charge, to any person obtaining a copy of 
this software and associated documentation files (the “Software”), to deal in 
the Software without restriction, including without limitation the rights to use,
copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the 
Software, and to permit persons to whom the Software is furnished to do so, 
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all 
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, 
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES 
OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND 
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT 
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, 
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING 
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR 
OTHER DEALINGS IN THE SOFTWARE.
```
