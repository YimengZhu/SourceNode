import pywws.WeatherStation as WeatherStation
import paho.mqtt.publish as publish
import time
from Entity import Observation
import datetime
import ConfigParser

weather_station = WeatherStation.weather_station()
current_pos = None

#Get the current data of the weather station. 
#The return value is a dict object with parameter and its value if there is new updated value.
def read_data():
    #The weather station store the data in a ring buffer. 
    #To get the current data, we should firstly get the current postion of the ring buffer.
    new_pos = weather_station.current_pos()
    global current_pos
    if new_pos != current_pos:
        current_pos = new_pos
        new_data = weather_station.get_data(new_pos)
    else:
        new_data = None
    return new_data

def mqtt_send_data():
    new_data = read_data()
    if new_data == None:
        return;
    

    config = ConfigParser.SafeConfigParser()
    config.read('../config.ini')
    foiId = int(config.get('register', 'foi'))

    timestamp = datetime.datetime.now().isoformat()
    print new_data
    for key, value in new_data.items():
        if value != None:
            try:
                datastreamId = int(config.get('datastreamid', key))
            except ConfigParser.NoOptionError:  
                continue
            observation = Observation(timestamp, value, timestamp, {"@iot.id" : datastreamId}, {"@iot.id" : foiId})
            print observation.jsonSerialize()
            publish.single('v1.0/Observations', observation.jsonSerialize())

while True:
    mqtt_send_data()
    time.sleep(2)
