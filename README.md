# Sourcing Node for the Project **Crowd Sensing Bodensee online**

## Background and hardware requirements
To monitor and supervise the enviroment condition on the Lake Constance the Fraunhofer Institut ISOB has conducted the project _Crowd Sensing Bodensee online_. In this project, the approach of crowd sensing will be use to obtain the enviroment parameter on the Lake Constance. This repository contains the code for a sensing node prototyp which is implemented in a Raspberry Pi 3 Model B. In the prototyp only a limited kind of parameters will be collected, e.g: surface water temperatur, humunity, rainfall, air pressure, air temperature, wind speed, wind direction. The surface water temperature will be measured via a DS1820 sensor, other parameter will be collected through a wetterstation WS1080. Furthermore to get the location data a GPS modul of NEO 6M from blox will be appened on the RasPi. The DS1820 and Neo 6M will be connected to the Raspi via the GPIO and the WS1080 will be conncted to the node via USB port.

| GPS pin | Raspi Pin |
|---------|-----------|
|vcc|5V|
|vdd|ground|
|Rx|Tx|
|Tx|Rx|

## 
