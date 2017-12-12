# Sourcing Node for the Project **Crowd Sensing Bodensee online**

## Background
To monitor and supervise the enviroment condition on the Lake Constance the Fraunhofer Institut ISOB has conducted the project _Crowd Sensing Bodensee online_. In this project, the approach of crowd sensing will be use to obtain the enviroment parameter on the Lake Constance. This repository contains the code for a sensing node prototyp which is implemented in a Raspberry Pi 3 Model B. In the prototyp only a limited kind of parameters will be collected, e.g: surface water temperatur, humunity, rainfall, air pressure, air temperature, wind speed, wind direction. All the sensor data will be packed as a _Observation_defined in the SensorThings API and published to a Mosquitto MQTT Broker in the sensing knoten. 

## Hardware requisite
The surface water temperature will be measured via a DS1820 sensor, other parameter will be collected through a wetterstation WS1080. Furthermore to get the location data a GPS modul of NEO 6M from blox will be appened on the RasPi. The DS1820 and Neo 6M will be connected to the Raspi via the GPIO and the WS1080 will be conncted to the node via USB port. The connection is described in the following table:

|GPS Connection|DS1820 Connection|
|--|--|
|<table> <tr><th>GPS Pins</th><th>Raspi Pins</th></tr><tr><td>vcc</td><td>GPIO 2</td></tr> <tr><td>vdd</td><td>GPIO 6</td></tr> <tr><td>Rx</td><td>GPIO 8</td></tr> <tr><td>Tx</td><td>GPIO 10</td></tr> </table>| <table> <tr><th>DS1820 Wire</th><th>Raspi Pins</th></tr><tr><td>red</td><td>GPIO 1</td></tr> <tr><td>yellow</td><td>GPIO 7</td></tr><tr><td>black</td><td>GPIO 9</td></tr></table>

## Usage of this repository
On this stage, it is assumed that you have raspbian jessie on your raspberry pi 3 model b and you have installed git.

Although the code in this repository is for ds1820, ws1080 and gps, you can run the corresponding python script independently. That means, if you don't have any of the sensor mentioned above, you can still use the python code in this repo to gather sensor data from the one you have. To achive this, first go to home directory.

`cd ~`

Then clone the repository with git

`git clone https://github.com/YimengZhu/SourceNode.git`

Then go to the project repository
`cd SourceNode`

Run install.sh
`./install.sh`

Now you should have installed the necessary dependencies and python libraries for the scripts. At next step, you should register the raspberry pi by the SensorThingsAPI, The ip address and port number of the SensorThingsAPI should be recorded in the config.ini. If you configured it successfully, run the ServerRegister.py
`python ServerRegister.py`

Now the corresponding iot.id of the sensing node such like thing id, sensor id, datastream ids and so on should be recorded in config.ini. Go to src/ folder and choose the script you want to run to gather sensor data.
`cd src`

To collect data from DS1820, run
`python Temperature.py`

To collect data from WS1080, run
`python WetterStation.py`

To collect data from gps, run
`python GPSReader.py`



##TO DO:
Add link to sensor things api
Thank pywws
Write a seperate shell script to add the startup python script 
Write the other wifi transfer mannual
Puffer all the data in sd card and send only few of them periodlly. Period should be set up.
