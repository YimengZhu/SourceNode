import test_pb2
import json
import paho.mqtt.client as mqtt
from subprocess import call

def on_connect(client, userdata, flags, rc):
    client.subscribe('v1.0/Observations', qos = 2)
    client.subscribe('v1.0/Locations', qos = 2)


def on_message(client, userdata, msg):
    if  msg.topic == 'v1.0/Observations':
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
    newPayload = test_pb2.ObservationWithGrid()
    newPayload.d = observation["Datastream"]["@iot.id"]
    newPayload.r = observation["result"]
    newPayload.g = observation["foi"]["iot.id"]
    newPayload.t = observation["resultTime"]

    call(["./periodic.out", newPayload.SerializeToString()])


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost", 1883, 60)
client.loop_forever()
