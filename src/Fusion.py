import paho.mqtt.client as mqtt 
import ConfigParser 
import json 
import paho.mqtt.publish as publish 
from Entity import Observation 
import datetime 

config = ConfigParser.SafeConfigParser() 
config.read('../config.ini')

datastreamids = {k:v for k, v in config.items('datastreamid')}

foi = config.get('register', 'foi')

measurements = {v: None for v in datastreamids.values()}

def on_connect(client, userdata, flags, rc):
    client.subscribe('v1.0/Observations', qos = 2)
    client.subscribe('v1.0/Locations', qos = 2)

def on_message(client, userdata, msg):
    if  msg.topic == 'v1.0/Observations':
        if msg.qos != 1: 
            handleObservation(msg.payload)
    elif msg.topic == 'v1.0/Locations':
        handleLocation();

def handleLocation():
    timestamp = datetime.datetime.now().isoformat()
    global measurements, foi
    for k, v in measurements.items():
        observation = Observation(timestamp, float(v), timestamp, {"@iot.id":int(k)}, {"@iot.id":foi})
        publish.single('v1.0/Observations', observation.jsonSerialize(), qos = 1)
    measurements = {v: None for v in datastreamids.values()}


def handleObservation(jsonString):
    observation = json.loads(jsonString)
    
    id = observation["Datastream"]["@iot.id"]
    result = observation["result"]
    
    if measurements[str(id)] == None:
        measurements[str(id)] = result
    else:
        measurements[str(id)] = (result + float(measurements[str(id)])) / 2
    
    observation["result"] = measurements[str(id)]
    
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost", 1883, 60)
client.loop_forever()    

