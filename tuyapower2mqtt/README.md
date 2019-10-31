# TuyaPower2MQTT - PyPi Module
Author: Phill Healey
https://github.com/jasonacox/tuyapower

# Description
Python module to pull power and state data from Tuya / Smart Life / Jinvoo WiFi smart socket/switch devices.  _Tested on RaspberryPi, Linux, Windows 10 and MacOS._ 

Compatible with Home Assistant.

# Preparation
All python dependencies for TuyaPower2MQTT will be automatically installed. However, you may need to install ```python-crypto``` via apt/yum/etc. If this is your first pip package then you may also need to install ```python-pip```.

```bash
 sudo apt-get install python-crypto python-pip		
```

# Functions
* deviceInfo - Poll device and return on, w, mA, V and err data.
    ```python
   	tuyapower.deviceInfo(PLUGID, PLUGIP, PLUGKEY, PLUGVERS)
    ```

# Usage
Gathers full power stats / data from Tuya sockets &amp; switches and reports results as JSON via MQTT

Full details coming soon.

