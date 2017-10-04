import struct
import paho.mqtt.client as mqtt 
from datetime import datetime 
from GPSCollector import GPS 
import sqlite3 
from Wrapper import Wrapper
from Entity import Observation
import socket
import json
import time
import ConfigParser
import observation_pb2

dbconnect = sqlite3.connect("../sensorData.db")
cursor = dbconnect.cursor()
gps = GPS()
counter = 0

foi = gps.getGridNum()

measurements = {'Temperature':None, 
		'temp_in':None, 
		'abs_pressure':None, 
		'hum_in':None, 
		'temp_out':None,
		'wind_dir':None,
		'hum_out':None,
		'wind_gust':None,
		'wind_ave':None,
		'rain':None
		 }


#The callback for when the client receives a CONNACK response rc from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    #Subscribing in on_connect means that if the connection is losed,
    #the subscription will be renewd on reconnection.
    client.subscribe("Temperature")
    client.subscribe("temp_in")
    client.subscribe("abs_pressure")
    client.subscribe("hum_in")
    client.subscribe("temp_out")
    client.subscribe("wind_dir")
    client.subscribe("hum_out")
    client.subscribe("wind_gust")
    client.subscribe("wind_ave")
    client.subscribe("rain")


def on_message(client, userdata, msg):

    #This callback do the following:
    #1. check wether the sensor is in a new foi. If yes, create a new dictionay for the measurements.
    global foi, gps, measurements
    if foi != gps.getGridNum():
        for key, value in measurements:
            value = None
    
    #2. get the mesurement message from the mqtt broker.
    measurement = float(msg.payload)
    topic = msg.topic
    timestamp = datetime.now()
    
    #3. make the fusion of the measurement. If the sensor in the new FOI, use the current one.
    if measurements[topic] != None:
        measurements[topic] = (measurements[topic] + measurement) / 2
    else: 
        measurements[topic] = measurement

    #4. get the meta data for this measurement  
    datastreamID = getDatastreamID(topic)
    foiID = gps.getGridNum()
    timestamp = int(round(time.time() * 1000))

    message = getByteArray(measurements[topic], datastreamID, 2589, timestamp)
    print 'Length of of the message to be transfered: ' + str(len(message))
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(message, ("10.42.0.1", 5005))
    del sock
    
    #5. log the raw data to the sqlite database
    global counter
    cursor.execute("INSERT INTO observation VALUES (?,?)", (counter, message))
    counter += 1
    dbconnect.commit()
    
def getDatastreamID(observedType):
    config = ConfigParser.SafeConfigParser()
    config.read('../observation.ini')
    dataStreamID = int(config.get('datastreamid', observedType))
    return dataStreamID


def getByteArray(measurement, datastreamID, foiID, timestamp):
    observation = observation_pb2.Observation()
    observation.r = measurement
    observation.d = datastreamID
    observation.f = foiID
    observation.t = timestamp
    return observation.SerializeToString()   

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message


client.connect("localhost", 1883, 60)	
client.loop_forever()
