"""

.. include:: ./README.md

"""

# Module: boltwood.py
# Author: Adam Robichaud <arobichaud@diffractionlimited.com>
# License: MIT License
#
# Copyright 2024 Diffraction Limited
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of 
# this software and associated documentation files (the “Software”), to deal in 
# the Software without restriction, including without limitation the rights to use, 
# copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the 
# Software, and to permit persons to whom the Software is furnished to do so, 
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all 
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, 
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES 
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND 
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT 
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, 
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING 
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR 
# OTHER DEALINGS IN THE SOFTWARE.

import serial
import serial.tools.list_ports as serial_ports


class Interfaces:
    """
    A list of access keys used when accessing data via the `Boltwood.get()` and `Boltwood.put()` methods
    
    See Also
    --------
    Boltwood, ObservingConditions, SafetyMonitor, DeviceDescriptor, EngineeringData

    Examples
    --------
    >>> from boltwood import Boltwood, Interfaces, ObservingConditions, DeviceDescriptor
    >>> bcs = Boltwood("COM1")
    >>> bcs.open()
    >>> bcs.get(Interfaces.OC, ObservingConditions.TEMPERATURE)
    (True, "-10")

    >>> bcs.put(Interfaces.DD, DeviceDescriptor.STA_SSID, "MyWiFiSSID")
    (True, "")

    >>> bcs.put(Interfaces.OC, ObservingConditions.TEMPERATURE)
    (False, "Invalid Argument: property 'temperature' is read-only")
    """
    
    OC = 'oc'
    """Access key for Observing Conditions serial interface"""

    SM = 'sm'
    """Access key for Safety Monitor serial interface"""

    DD = 'dd'
    """Access key for Device Descriptors serial interface"""

    EN = 'en'
    """Access key for Engineering Data serial interface"""

class ObservingConditions:
    ALL = 'all'
    """Access key for a space-delimited list of all parameters in ObservingCondition (read-only)"""

    AVERAGE_PERIOD = 'averageperiod' 
    """Access key for the time period over which observations will be averaged in hours (read-only)"""
    
    CLOUD_COVER = 'cloudcover' 
    """Access key for an estimate of the sky's cloud coverage in % (read-only)"""
    
    DEWPOINT = 'dewpoint' 
    """Access key for the atmospheric dew point at the observatory in degrees Celcius (read-only)"""
    
    HUMIDITY = 'humidity' 
    """Access key for the relative humidity at the observatory in % (read-only)"""
    
    PRESSURE = 'pressure' 
    """Access key for the atmospheric pressure at the observatory in hPa (read-only)"""
    
    RAIN_RATE = 'rainrate' 
    """Access key for an estimate of the rain rate at the observatory in mm/hr (read-only)"""
    
    SKY_BRIGHTNESS = 'skybrightness' 
    """Access key for an estimate of the sky brightness at the observatory in Lux (read-only)"""
    
    SKY_QUALITY = 'skyquality' 
    """Access key for the ASCOM sky quality property. Not supported, reports as 'NA' (read-only)"""
    
    SKY_TEMPERATURE = 'skytemperature' 
    """Access key for the sky temperature at the observatory in degrees Celcius (read-only)"""
    
    STAR_FWHM = 'starfwhm' 
    """Access key for the ASCOM star FWHM property. Not supported, reports as 'NA' (read-only)"""
    
    TEMPERATURE = 'temperature' 
    """Access key for the ambient temperature at the observatory in degrees Celcius (read-only)"""
    
    WIND_DIRECTION = 'winddireciton' 
    """Access key for the ASCOM Wind Direction property. Not supported, reports as 'NA' (read-only)"""
    
    WIND_GUST = 'windgust' 
    """Access key for the ASCOM Wind Gust property. Not supported, reports as 'NA' (read-only)"""
    
    WIND_SPEED = 'windspeed' 
    """Returns the wind speed at the observatory in m/s (read-only)"""

    keys_all = [
        AVERAGE_PERIOD,
        CLOUD_COVER,
        DEWPOINT,
        HUMIDITY,
        PRESSURE,
        RAIN_RATE,
        SKY_BRIGHTNESS,
        SKY_QUALITY,
        SKY_TEMPERATURE,
        STAR_FWHM,
        TEMPERATURE,
        WIND_DIRECTION,
        WIND_GUST,
        WIND_SPEED,
    ]
    """List of all keys provided by the 'all' access key, in proper API order"""

    _values = {}

    def __init__(self, str):
        """
        ObservingConditions 'all' parser and list of ObservingConditions access keys

        Parameters
        ----------
        str : string
            Results of a call to `Boltwood.getOC('all')`

        Examples
        --------
        >>> from boltwood import Boltwood, ObservingConditions
        >>> bcs = Boltwood("COM1")
        >>> bcs.open()
        >>> rc, raw_values = bcs.getOCAll()
        >>> values = ObservingConditions(raw_values)
        >>> print(f'{values[ObservingConditions.WIND_SPEED]}')
        1.0
        """
        self._parse(str)

    def _parse(self, str):
        arr = str.split(' ')
        for i in range(0, len(self.keys_all)):
            self._values[self.keys_all[i]] = arr[i]

    def __getitem__(self, key):
        """
        Array accessor for parsed values, indexed by access keys listed above

        Parameters
        ----------
        key : string
            ObservingConditions access key to retrieve

        Returns
        -------
        value : string
            Stored value for provided access key 
        """
        return self._values[key]

class SafetyMonitor:
    """
    A list of access keys used when accessing data via `Boltwood.getSM()`

    Examples
    --------

    >>> from boltwood import Boltwood, SafetyMonitor
    >>> bcs = Boltwood("COM1")
    >>> bcs.open()
    >>> bcs.getSM(SafetyMonitor.IS_SAFE)
    (True, "1")
    """

    IS_SAFE = "isSafe"
    """
    Access key for the ASCOM Safety Monitor 'isSafe' property (read-only)
    
    1 is safe, 0 is unsafe
    """

class DeviceDescriptor:
    """
    A list of access keys when accessing data via `Boltwood.getDD()` or `Boltwood.putDD()`
    """

    SERIAL = 'serial'
    """Access key for the device's unique serial number (read-only)"""

    FW_REVISION = "fwrev"
    """Access key for the device's firmware revision number (read-only)"""

    STA_IP = "sta_ip"
    """Access key for the device's WiFi Station DHCP-assigned IP address (read-only)"""

    STA_SSID = "sta_ssid"
    """Access key for the device's WiFi Station SSID (network name)"""

    STA_PASS = "sta_pass"
    """Access key for the device's WiFi Station passphrase (write-only)"""

    AP_SSID = "ap_ssid"
    """Access key for the device's factory-assigned WiFi Access Point SSID (read-only)"""

class EngineeringData:
    WIND_COLD       = 'windColdSensor' 
    """Access key for EngineeringData Windspeed sensor cold stock temperature measurement (read-only)"""

    WIND_HOT        = 'windHotSensor'  
    """Access key for EngineeringData Windspeed sensor hot stock temperature measurement (read-only)"""

    WINDSPEED       = 'windSpeed'      
    """Access key for EngineeringData Windspeed sensor measurement (read-only)"""

    PRESSURE        = 'pressure'       
    """Access key for EngineeringData Pressure sensor measurement (read-only)"""

    PRESSURE_TEMP   = 'pressureTemp'   
    """Access key for EngineeringData Pressure sensor temperature measurement (read-only)"""

    AMBIENT_TEMP    = 'ambientTemp'
    """Access key for EngineeringData Ambient Temperature sensor temperature measurement (read-only)"""

    VOLTAGE         = 'voltage'        
    """Access key for EngineeringData Power Supply Voltage sensor measurement (read-only)"""

    DAYLIGHT        = 'daylightSensor' 
    """Access key for EngineeringData Daylight sensor measurement (read-only)"""

    SKY_AMBIENT     = 'skyAmbientTemp' 
    """Access key for EngineeringData Sky Temperature minus Ambient Temperature measurement (read-only)"""

    SKY_TEMP        = 'skyTemp'        
    """Access key for EngineeringData Sky Temperature sensor measurement (read-only)"""

    CASE_TEMP       = 'caseTemp'       
    """Access key for EngineeringData Case Temperature sensor measurement (read-only)"""

    RAIN_RAW        = 'rainRaw'        
    """Access key for EngineeringData Rain sensor's instantaneous raw drop sample (read-only)"""

    RAIN_DPM        = 'rainDpm'        
    """Access key for EngineeringData Rain sensor drops/minute measurement (read-only)"""

    HUMIDITY        = 'humidity'       
    """Access key for EngineeringData Humidity sensor measurement (read-only)"""

    HUMIDITY_TEMP   = 'humidityTemp'   
    """Access key for EngineeringData Humidity sensor onboard temperature measurement (read-only)"""

    DEWPOINT        = 'dewpoint'      
    """Access key for EngineeringData Dewpoint sensor calculated value (read-only)"""

    COND_OVERCAST   = 'condOvercast'
    """Access key for EngineeringData Overcast condition state (read-only)"""

    COND_WIND       = 'condWind'
    """Access key for EngineeringData Windy condition state (read-only)"""

    COND_BRIGHTNESS = 'condBrightness'
    """Access key for EngineeringData Brightness condition state (read-only)"""

    COND_PRECIP     = 'condPrecipitation'
    """Access key for EngineeringData Precipitation condition state (read-only)"""

    COND_WEATHER    = 'condWeather'
    """Access key for EngineeringData Overall Weather condition state (read-only)"""

    COND_HUMIDITY   = 'condHumidity'
    """Access key for EngineeringData Humidity condition state (read-only)"""

    COND_PRESSURE   = 'condPressure'
    """Access key for EngineeringData Pressure condition state (read-only)"""

    COND_VOLTAGE    = 'condVoltage'
    """Access key for EngineeringData Voltage condition state (read-only)"""

    def _format_lmh(self, val):
        """
        Convenience function for formatting low/medium/high condition values
        """
        if val == '0': return "low"
        if val == '1': return "med"
        if val == '2': return "high"
        return "???"

    def _format_overcast(self):
        """
        Convenience function for formatting overcast condition values
        """
        val = self.values[self.COND_OVERCAST]
        if val == '0': return 'clear'
        if val == '1': return 'cloudy'
        if val == '2': return 'vcloudy'
        return '???'

    def _format_wind(self):
        """
        Convenience function for formatting windy condition values
        """
        val = self.values[self.COND_WIND]
        if val == '0': return 'calm'
        if val == '1': return 'windy'
        if val == '2': return 'vwindy'
        return '???'

    def _format_bright(self):
        """
        Convenience function for formatting brightness condition values
        """
        val = self.values[self.COND_BRIGHTNESS]
        if val == '0': return 'dark'
        if val == '1': return 'light'
        if val == '2': return 'vlight'
        return '???'

    def _format_precip(self):
        """
        Convenience function for formatting precipitation condition values
        """
        val = self.values[self.COND_PRECIP]
        temp = float(self.values[self.AMBIENT_TEMP])
        if val == '0': return 'dry'
        if val == '1': return 'raining' if temp > 0 else 'snowing'
        if val == '2': return 'snowing'
        return '???'

    def _format_weather(self):
        """
        Convenience function for formatting overall weather condition values
        """
        val = self.values[self.COND_WEATHER]
        if val == '0': return 'unsafe'
        if val == '1': return 'safe'
        return '???'
    
    def _format_humidity(self):
        """
        Convenience function for formatting humidity condition values
        """
        val = self.values[self.COND_HUMIDITY]
        return self._format_lmh(val)  

    def _format_pressure(self):
        """
        Convenience function for formatting pressure condition values
        """
        val = self.values[self.COND_PRESSURE]
        return self._format_lmh(val)  

    def _format_voltage(self):
        """
        Convenience function for formatting voltage condition values
        """
        val = self.values[self.COND_VOLTAGE]
        return self._format_lmh(val)  

    def get_cond(self, key):
        """
        Convenience function for formatting condition values into human-readable strings

        Parameters
        ----------
        key : string
            EngineeringData condition Access key to format. e.g. `EngineeringData.COND_OVERCAST`

        Returns
        -------
        formatted_value : string
            Human readable interpretation of the condition enumerations

        Examples
        --------
        When `EngineeringData[COND_OVERCAST] == 0`

        >>> from boltwood import Boltwood, EngineeringData
        >>> bcs = Boltwood("COM1")
        >>> bcs.open()
        >>> rc, vals = bcs.getENAll()
        >>> ed = EngineeringData(vals)
        >>> ed.get_cond(EngineeringData.COND_OVERCAST)
        'clear'

        When `EngineeringData[COND_OVERCAST] == 1`
        
        >>> ed.get_cond(EngineeringData.COND_OVERCAST)
        'cloudy'
        
        When `EngineeringData[COND_OVERCAST] == 2`

        >>> ed.get_cond(EngineeringData.COND_OVERCAST)
        'vcloudy'

        

        """
        match key:
            case self.COND_OVERCAST:
                return self._format_overcast()
            case self.COND_WIND:
                return self._format_wind()
            case self.COND_BRIGHTNESS:
                return self._format_bright()
            case self.COND_PRECIP:  
                return self._format_precip()
            case self.COND_WEATHER: 
                return self._format_weather()
            case self.COND_HUMIDITY: 
                return self._format_humidity()
            case self.COND_PRESSURE:  
                return self._format_pressure()
            case self.COND_VOLTAGE:          
                return self._format_voltage()
        return "???"    
    
    keys_cond = [        
        COND_OVERCAST,
        COND_WIND,
        COND_BRIGHTNESS,
        COND_PRECIP,
        COND_WEATHER,
        COND_HUMIDITY,
        COND_PRESSURE,
        COND_VOLTAGE
    ]
    """List of EngineeringData condition keys"""

    keys = [
        WIND_HOT,
        WIND_COLD,
        WINDSPEED,
        PRESSURE,
        PRESSURE_TEMP,
        AMBIENT_TEMP,
        VOLTAGE,
        DAYLIGHT,
        SKY_AMBIENT,
        SKY_TEMP,
        CASE_TEMP,
        RAIN_RAW,
        RAIN_DPM,
        HUMIDITY,
        HUMIDITY_TEMP,
        DEWPOINT
    ]
    """List of EngineeringData parameter keys"""

    values = {}
    """
        Storage array for parsed values. 
        
        We advise you use array access on the storage class instance to access (see examples).

        Parameters
        ----------
        key : string
            Either an accessor key provided above (e.g. boltwood.EngineeringData.WIND_HOT or boltwood.EngineeringData.COND_OVERCAST)
            or the raw string that key represents

        Returns
        -------
        value : string
            The value of the requested key

        See Also
        --------
        Boltwood.getENAll()

        Examples
        --------
        >>> from boltwood import Boltwood, EngineeringData
        >>> bcs = Boltwood("COM1")
        >>> bcs.open()
        >>> rc, raw_values = bcs.getENAll()
        >>> values = EngineeringData(raw_values)
        >>> values[EngineeringData.WIND_HOT]
        20
        
        >>> values[EngineeringData.COND_OVERCAST]
        0
        """

    def __init__(self, str):
        """
        Engineering Data string decoder
        
        Parameters
        ----------
        str : string
            Value portion of a `Boltwood.getENAll()` call

        Examples
        --------
        >>> from boltwood import Boltwood, EngineeringData
        >>> bcs = Boltwood("COM1")
        >>> bcs.open()
        >>> rc, raw_values = bcs.getOCAll()
        >>> values = EngineeringData(raw_values)
        >>> print(f'{values[EngineeringData.HUMIDITY]}')
        ( 50.0, 1 )
        """
        self._parse(str)

    def _parse(self, str):
        """
        Enineering Data decoder

        Decodes the passed string from a space-delimited list of engineering data values and saves them
        in boltwood.EngineeringData.values

        Parameters
        ----------
        str : string
            Value portion of a Boltwood.getENAll() call
        """
        arr = str.split(' ')
        for i in range(0, len(self.keys)):
            self.values[self.keys[i]] = arr[i]
        for i in range(0, len(self.keys_cond)):
            self.values[self.keys_cond[i]] = arr[i+len(self.keys)]      

    def __getitem__(self, key):
        return self.values[key]
    
class Thresholds:
    CLEAR_CLOUDY     = 'clearCloudy'
    """Threshold/Safety Trigger accessor key for reporting cloudy when (sky temp - ambient temp) > threshold in degrees Celcius"""

    CLOUDY_VCLOUDY   = 'cloudyVeryCloudy'
    """Threshold/Safety Trigger accessor key for reporting vcloudy when (sky temp - ambient temp) > threshold in degrees Celcius"""

    CALM_WINDY       = 'calmWindy'
    """Threshold/Safety Trigger accessor key for reporting windy when windspeed > threshold in km/h"""

    WINDY_VWINDY     = 'windyVeryWindy'
    """Threshold/Safety Trigger accessor key for reporting vwindy when windspeed > threshold in km/h"""

    DARK_LIGHT       = 'darkLight'
    """Threshold/Safety Trigger accessor key for reporting light when brightness > threshold in %"""

    LIGHT_VLIGHT     = 'lightVeryLight'
    """Threshold/Safety Trigger accessor key for reporting vlight when brightness > threshold in %"""

    RAIN_SENSITIVITY = 'rainSensitivity'
    """Threshold/Safety Trigger accessor key for reporting rain hit when rain sensor duty cycle > threshold in microseconds"""

    RAIN_DPM         = 'rainDpmThreshold'
    """Threshold/Safety Trigger accessor key for reporting raining/snowing when dpm > threshold in drops/minute"""

    HUMIDITY_LOW     = 'humidityLow'
    """Threshold/Safety Trigger accessor key for reporting low humidity when humidity < threshold in %"""

    HUMIDITY_HIGH    = 'humidityHigh'
    """Threshold/Safety Trigger accessor key for reporting high humidity when humidity > threshold in %"""

    PRESSURE_LOW     = 'pressureLow'
    """Threshold/Safety Trigger accessor key for reporting low pressure when pressure < threshold in mBar"""

    PRESSURE_HIGH    = 'pressureHigh'
    """Threshold/Safety Trigger accessor key for reporting high pressure when pressure > threshold in mBar"""

    VOLTAGE_LOW      = 'voltageLow'
    """Threshold/Safety Trigger accessor key for reporting low voltage when voltage < threshold in V"""

    VOLTAGE_HIGH     = 'voltageHigh'
    """Threshold/Safety Trigger accessor key for reporting high voltage when voltage > threshold in V"""

    keys = [
        CLEAR_CLOUDY,     
        CLOUDY_VCLOUDY,      
        CALM_WINDY,       
        WINDY_VWINDY,        
        DARK_LIGHT,       
        LIGHT_VLIGHT,    
        RAIN_SENSITIVITY,
        RAIN_DPM,       
        HUMIDITY_LOW,      
        HUMIDITY_HIGH, 
        PRESSURE_LOW,      
        PRESSURE_HIGH,      
        VOLTAGE_LOW,       
        VOLTAGE_HIGH
    ]
    """List of Threshold/Safety Trigger accessor keys"""

    threshValue = {}
    """List of Threshold values indexed by Threshold/Safety Trigger accessor keys"""

    roofTrig = {}
    """List of Safety Trigger values indexed by Threshold/Safety Trigger accessor keys"""
    
    def __init__(self, str=''):
        """
        Threshold/Safety Trigger decoder class 

        Parameters
        ----------
        str : string
            The value result of a call to `boltwood.Boltwood.getOCThresholds()`

        See Also
        --------
        Boltwood.getOCThresholds()

        Examples
        --------
        >>> from boltwood import Boltwood, Thresholds
        >>> bcs = Boltwood("COM1")
        >>> bcs.open()
        >>> rc, raw_values = bcs.getOCThresholds()
        >>> values = Thresholds(raw_values)
        >>> values.threshValue[Thresholds.CLEAR_CLOUDY] # Threshold value
        -10
        >>> values.roofTrig[Thresholds.CLEAR_CLOUDY] # Active as safety trigger
        0
        >>> values[Thresholds.CLEAR_CLOUDY] # Tuple of threshold value & safety trigger
        ("-10", 0)
        """
        self._parse(str)

    def _parse(self, str):
        if not str: return
        arr = str.split(" ")
        for i in range(0, len(self.keys)):
            self.threshValue[self.keys[i]] = arr[i]
            self.roofTrig[self.keys[i]] = arr[i + len(self.keys)]
                               
    def to_string(self):
        """
        Encodes values stored in this class instance into a string for transmission via boltwood.Boltwood.setOCThresholds()

        Examples
        --------
        >>> from boltwood import Boltwood, Thresholds
        >>> bcs = Boltwood("COM1") 
        >>> bcs.open()
        >>> # Fetch existing thresholds first
        >>> rc, raw_thresholds = bcs.getOCThresholds() 
        >>> # Parse the result
        >>> thresholds = Thresholds(raw_thresholds) 
        >>> # Add Thresholds.CLEAR_CLOUDY to list of active safety triggers
        >>> thresholds.roofTrig[Thresholds.CLEAR_CLOUDY] = 1 
        >>> # Send updated threshold structure to Boltwood, expect: (True, "")
        >>> bcs.setOCThresholds(thresholds.to_string())
        (True, "")

        Returns
        -------
        encoded_str : string
            The Threshold/Safety Trigger values stored in proper order for transmission to a BCSIII device over a serial connection
        """
        tmp = []
        for key in self.keys:
            tmp.append("{}".format(self.threshValue[key]))
        for key in self.keys:
            tmp.append("{}".format(self.roofTrig[key]))
        return ' '.join(tmp)
    
    def __getitem__(self, key):
        """
        Accessor for Thresholds/Safety Trigger entries

        Looks up a stored Threshold/Safety Trigger value by access key and returns it as a tuple

        Parameters
        ----------
        key : string
            Thresholds/Safety Trigger ccess key, or raw string representing the threshold to be accessed

        Returns
        -------
        threshold : string
            string-encoded value of the Thresholds

        safety_trigger : string
            string-encoded value of whether the Safety Trigger is active for the provided key ('1' for active, '0' for inactive)    
        """
        return (self.threshValue[key], self.roofTrig[key])
        
class Boltwood:
    _ser = serial.Serial()
    """Serial connection manager [Internal only]"""

    port = '/dev/ttyUSB0'
    """Serial port name, must be set before calling Boltwood.open()"""

    _dbg = False
    """Internal use only"""

    def __init__(self, port):
        """
        Class constructor for the Boltwood Cloud Sensor III python serial API

        Parameters
        ----------
        port : string
            Valid serial port hosting a Boltwood Cloud Sensor III
        """
        self.port = port

    def debug(self, val):
        """
        Reserved for factory use
        """
        self._dbg = val
    
    def __del__(self):
        if self._ser.is_open:
            self._ser.close()

    def open(self):
        """
        Opens a connection to the serial port provided in Boltwood class constructor.

        e.g.

        ```python
        from boltwood import Boltwood

        bcs = Boltwood("COM1")                          # for Windows machines
        bcs = Boltwood("/dev/ttyUSB0")                  # for Linux machines
        bcs = Boltwood("/dev/tty.usbserial-FTG6RCEJ")   # for MacOS machines

        bcs.open()

        # ... Do stuff with bcs ...
        ```
        """
        if self._ser.is_open:
            return

        if self._dbg: print("Connecting to BCSIII")            
        self._ser.port = self.port
        self._ser.baudrate = 9600
        self._ser.bytesize = serial.EIGHTBITS
        self._ser.parity = serial.PARITY_NONE
        self._ser.stopbits = serial.STOPBITS_ONE
        self._ser.timeout = 2
        self._ser.rtscts = False

        self._ser.rts = False
        self._ser.dtr = True
        self._ser.open()
        self._ser.rts = False

        if not self._dbg:
            return

    def close(self):
        """
        Closes an open serial connection. Executed automatically by Boltwood class destructor.
        """
        self._ser.close()
    
    def scan():
        """
        Lists all available serial ports on the host OS

        Returns
        -------
        ports : list
            An array of serial port designators

        Examples
        --------
        Windows

        >>> from boltwood import Boltwood
        >>> Boltwood.scan()
        [ "COM1", "COM3" ]
        
        Linux
        
        >>> Boltwood.scan()
        [ "/dev/ttyUSB0" ]

        MacOS

        >>> Boltwood.scan()
        [ "/dev/tty.usbserial-FT123456" ]

        """
        ports = serial_ports.comports()
        results = []
        for port in ports:
            results.append(port[0])
        return results

    def _exec(self, verb, key, param, val=''):
        if not self._ser.is_open:
            self.open()

        self._ser.reset_output_buffer()
        self._ser.reset_input_buffer()

        # construct the command
        dout = "{} {} {}".format(verb, key, param)
        if (val):
            dout = "{} {}".format(dout, val)
        dout = dout + '\n'

        if self._dbg: print('out: {}'.format(dout[0:-1]))        
        self._ser.write(dout.encode())
        din = self._ser.readline().decode()
        if self._dbg: print('in : {}'.format(din[0:-1]))
        if din[0] != '1' and din[0] != '0' and din[0] != '2':
            raise RuntimeError('Invalid response from BCSIII')
                  
        return din[0] == '0', din[2:-1]

    def get(self, key, param):
        """
        General-use interface accessor for readable properties      

        Parameters
        ----------
        key : string
            An interface shorthand key to access. e.g. "dd" for Device Descriptors
            
        param : string
            Parameter key to retrieve. e.g. "sta_ssid"

        Returns
        -------
        rc : bool
            False if successful, True otherwise
        
        val : string
            string-encoded requested value if successful, error message otherwise

        See Also
        --------
        Interfaces
        ObservingConditions
        SafetyMonitor
        DeviceDescriptor
        EngineeringData

        Examples
        --------
        >>> from boltwood import Boltwood, Interfaces, ObservingConditions
        >>> bcs = Boltwood("COM1")
        >>> bcs.get(Interfaces.OC, ObservingConditions.TEMPERATURE)
        (True, "-12.0")
        """
        return self._exec('g', key, param)

    def getOC(self, param):
        """
        Retrieve readable Observing Conditions interface values and threshold/safety trigger structure 

        Parameters
        ----------
        param : string
            Observing Conditions access key to read. e.g. ObservingConditions.TEMPERATURE

        Returns
        -------
        rc : bool
            True if successful, False otherwise

        status : string
            Device's current Observing Conditions interface readings

        See Also
        --------
        ObservingConditions
        """
        return self.get('oc', param)

    def getSM(self, param):
        """
        Retrieve readable Safety Monitor interface values 
        
        Parameters
        ----------
        param : string
            Safety Monitor access key to retrieve. e.g. SafetyMonitor.IS_SAFE

        Returns
        -------
        rc : bool
            True if successful, False otherwise

        status : string
            Device's current Safety Monitor interface readings
        
        See Also
        --------
        SafetyMonitor
        """
        return self.get('sm', param)

    def getDD(self, param):
        """
        Retrieve readable Device Descriptor interface values

        Parameters
        ----------
        self : Boltwood
            Reference to a connected Boltwood object
        
        param : string
            Device Descriptor access key to set. e.g. DeviceDescriptor.STA_SSID

        val : string
            Value to set. e.g. "MyWiFiSSID"

        Returns
        -------
        rc : bool
            0 if successful, 1 otherwise
        
        val : string
            empty if successful, error message otherwise

        See Also
        --------
        DeviceDescriptor
        """
        return self.get('dd', param)

    def getEN(self, param='all'):
        """
        Retrieve readable Enineering Data interface properties

        Parameters
        ----------
        self : Boltwood
            Reference to a connected Boltwood object
        
        param : string
            EngineeringData access key to set. e.g. EngineeringData.STA_SSID

        val : string
            Value to set

        Returns
        -------
        rc : bool
            0 if successful, 1 otherwise
        
        val : string
            empty if successful, error message otherwise

        See Also
        --------
        EngineeringData
        """
        return self.get('en', param)

    def put(self, key, param, val):
        """
        General-use interface accessor for writable properties

        Parameters
        ----------
        key : string
            An interface shorthand key to access. e.g. "dd" for Device Descriptors
            
        param : string
            Parameter key to set. e.g. "sta_ssid"

        val : string
            Value to set

        Returns
        -------
        rc : bool
            0 if successful, 1 otherwise
        
        val : string
            empty if successful, error message otherwise

        See Also
        --------
        Interfaces
        ObservingConditions
        SafetyMonitor
        DeviceDescriptor
        EngineeringData

        Examples
        --------
        >>> from boltwood import Boltwood, Interfaces, ObservingConditions
        >>> bcs = Boltwood("COM1")
        >>> bcs.open()
        >>> bcs.put(Interfaces.DD, DeviceDescriptor.STA_SSID, "MyWiFiSSID")
        (True, "")
        >>> bcs.put(Interfaces.OC, ObservingConditions.TEMPERATURE, 23)
        (False, "Invalid argument: property 'temperature' is read-only")
        """
        return self._exec('p', key, param, val)

    def putDD(self, param, val):
        """
        Set writable Device Descriptor values

        This method can be used to set writable device descriptor values such as:
        - sta_ssid
        - sta_pass

        Parameters
        ----------
        self : Boltwood
            Reference to a connected Boltwood object
        
        param : string
            Parameter key to set. e.g. "sta_ssid"

        val : string
            Value to set

        Returns
        -------
        rc : bool
            0 if successful, 1 otherwise
        
        val : string
            empty if successful, error message otherwise
        """
        return self.put('dd', param, val)

    def putOC(self, param, val):
        """
        Set writable Observing Conditions values

        This method can be used to set writable observing condition values such as:
        - refresh
        - thresholds (see also: Boltwood.setOCThresholds())

        Parameters
        ----------
        self : Boltwood
            Reference to a connected Boltwood object
        
        param : string
            Parameter key to set. e.g. "thresholds"

        val : string
            Value to set

        Returns
        -------
        rc : bool
            0 if successful, 1 otherwise
        
        val : string
            empty if successful, error message otherwise
        """
        return self.put('oc', param, val)

    def getSerial(self):
        """
        Retrieve Serial Number

        Fetches the device's factory-programmed serial number.

        Returns
        -------
        rc : bool
            True if successful, False otherwise

        serial : string
            Device's factory programmed serial number. e.g. "BCS3S24010203"
        """                       
        return self.getDD('serial')

    def getFWRev(self):
        """
        Retrieve Firmware Revision Number

        Fetches the device's firmware revision number. Requires firmware revision 12 or greater.

        Returns
        -------
        rc : bool
            True if successful, False otherwise

        revision : string
            Device's firmware revision number. e.g. "rev12"
        """
        return self.getDD('fwrev')

    def getSTAIP(self):
        """
        Retrieve DHCP-assigned WiFi Station IP Address

        Fetches the device's DHCP-assigned IP if connected to the programmed WiFi Station.

        Returns
        -------
        rc : bool
            True if successful, False otherwise

        ip : string
            Device's DHCP-assigned Station IP if the device is connected to a WiFi station, empty string if not.
        """
        return self.getDD('sta_ip')

    def getSTASSID(self):
        """
        Retrieve Wireless Station SSID

        Fetches the device's programmed user-submitted wireless Station SSID.

        Returns
        -------
        rc : bool
            True if successful, False otherwise

        ssid : string
            Device's programmed WiFi Station SSID if rc is True, garbage otherwise
        """
        return self.getDD('sta_ssid')

    def getAPSSID(self):
        """
        Retrieve Wireless Access Point SSID

        Fetches the device's unique wireless Accesss Point SSID.

        Returns
        -------
        rc : bool
            True if successful, False otherwise

        ssid : string
            Device's factory-set Access Point SSID if rc is True, garbage otherwise
        """
        return self.getDD('ap_ssid')
    
    def getOCAll(self):
        """
        Retrieve Observing Conditions amalgamator 

        Shorthand for `Boltwood.getOC('all')`

        Returns
        -------
        rc : bool
            True if successful, False otherwise

        status : string
            Device's current Observing Conditions interface readings

        See Also
        --------
        ObservingConditions
        Boltwood.getOC()
        """
        return self.getOC('all')

    def getSMAll(self):
        """
        Retrieve Safety Monitor amalgamator 

        Fetches all Safety Monitor interface parameters:
        A string-delimited list of all supported parameters as defined in the ASCOM Safety Monitor device interface.
        Currently:
         
        isSafe: 
            1 if device detects no configured safety condition failures. 0 otherwise.

        Returns
        -------
        rc : bool
            True if successful, False otherwise

        status : string
            Device's current Safety Monitor interface readings

        See Also
        --------
        SafetyMonitor
        Boltwood.getSM()
        """
        return self.getSM('all')

    def getENAll(self):
        """
        Retrieve Engineering Data amalgamator.

        Shorthand for `Boltwood.getEN('all')`.
        
        Returns
        -------
        rc : bool
            True if successful, False otherwise

        status : string
            Device's current Engineering Data interface readings

        See Also
        --------
        EngineeringData
        Boltwood.getEN()
        """
        return self.getEN('all')
    
    def getOCThresholds(self):
        """
        Retrieve user-programmed safety thresholds and trigger structure

        Shorthand for `Boltwood.getOC('thresholds')`

        Fetches a space-delimited list of internal safety thresholds and whether they're used in the roof trigger.
        The thesholds are listed in the following order as floats, then again as booleans (0 for off, 1 for on) 
        when those thresholds are used to denote a safety exception.

        See Also
        --------
        Thresholds
        Boltwood.getOC()
        """
        return self.getOC('thresholds')

    def setOCThresholds(self, val):
        """
        Set user-programmed safety thresholds and trigger structure
        
        Sets a space-delimited list of internal safety thresholds and whether they're used in the roof trigger.
        The thesholds are listed in the following order as floats, then again as booleans (0 for off, 1 for on) 
        when those thresholds are used to denote a safety exception.

        boltwood.Thresholds has been provided as a convenience wrapper to encode and decode this list in a programmatic way:

        See Also
        --------
        Thresholds
        Boltwood.putOC()
        """
        return self.putOC('thresholds', val)

Boltwood.scan = staticmethod(Boltwood.scan)
