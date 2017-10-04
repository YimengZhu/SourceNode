import time
import os
import paho.mqtt.publish as publish
import datetime
import ConfigParser
from Entity import Observation

#load the driver 
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

#define the file path of the output file
temp_sensor = '/sys/bus/w1/devices/28-03168c0303ff/w1_slave'


#function to read the output in the temp_sensor file
def temp_raw():
    f = open(temp_sensor, 'r')
    lines = f.readlines()
    f.close()
    return lines

#get the temperature data from the temp_sensor file
def read_temp():
    #find out the raw data with YES at the end of the first line
    lines = temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = temp_raw()
    #parse the number to celsius and fahrenheit
    temp_output = lines[1].find('t=')
    if temp_output != -1:
        temp_string = lines[1].strip()[temp_output + 2:]
        temp_c = float(temp_string) / 1000.0
        return temp_c

#publish the temperature as a observation to mqtt broker
def mqtt_send_data():
    
    result = read_temp()
    timestamp = datetime.datetime.now().isoformat()

    config = ConfigParser.SafeConfigParser()
    config.read('../config.ini')
    foiId = int(config.get('register', 'foi'))    
    datastreamId = int(config.get('datastreamid', 'Temperature'))
  
    observation = Observation(timestamp, result, timestamp, {"@iot.id" : datastreamId}, {"@iot.id" : foiId})
    print observation.jsonSerialize()
    publish.single('v1.0/Observations', observation.jsonSerialize())    

while True:
    mqtt_send_data()
    time.sleep(1)
