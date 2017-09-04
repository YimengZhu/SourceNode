import struct
import paho.mqtt.client as mqtt 
from datetime import datetime 
from GPSCollector import GPS 
import sqlite3 
from Wrapper import Wrapper
from Entity import Observation
import socket
import zlib
import pysmile
import json
import time

dbconnect = sqlite3.connect("../sensorData.db")
cursor = dbconnect.cursor()
gps = GPS()

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
    #1. Listen on the mqtt broker to get the mesurement result.
    measurement = float(msg.payload)
    topic = msg.topic
    timestamp = datetime.now()
        
    #2. get the value from the database based on the location and topic
    gridID = gps.getGridNum() 
    cursor.execute("SELECT value FROM sensorData WHERE gridID=? And topic=?", (gridID, topic))
    result = cursor.fetchall()
    if len(result) == 0:
        print 'No entry in for this FOI and topic in the database. Use current value as the initial value.'
        cursor.execute("INSERT INTO sensorData VALUES (?,?,?,?)", (gridID, topic, measurement, timestamp))
    elif len(result) == 1:
	newVal = ( result[0][0] + measurement ) / 2
	measurement = newVal
        cursor.execute("UPDATE sensorData SET value = ? , updateTime = ? WHERE gridID = ? AND topic = ?", (newVal, timestamp, gridID, topic))        
    else:
        raise 'More than one entry for this area and topic is inserted in the database!'
    
    #3. get the datastream Id based on the observed type
    #datastreamID = getDatastreamID(topic)
    observation = Observation(datetime.now().isoformat(),
            measurement,
            datetime.now().isoformat(),
            {"@iot.id": 1},
            {"@iot.id": 1})
    
    message = getByteArray(measurement, 1, 1)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(message, ("10.42.0.1", 5005))
    del sock

def getDatastreamID(observedType):
    config = ConfigParser.SafeConfigParser()
    config.read('../observation.ini')
    dataStreamID = int(config.get('register', 'datastreamid'))


def getByteArray(measurement, datastreamID, foiID):
    #This funciton generate a byte array like following:
    #8 Bytes timestampe + 
    timeHex = hex(int(time.mktime(datetime.now().timetuple())) - time.timezone)[2:].zfill(8)
    datastreamHex = hex(datastreamID)[2:]
    foiHex = hex(foiID).zfill(2)[2:].zfill(2)
    valHex = hex(int(measurement * 100))[2:].zfill(3)
    stringSum = timeHex + foiHex + datastreamHex + valHex
    retVal = bytearray.fromhex(stringSum)
    print len(retVal)
    return retVal

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message


client.connect("localhost", 1883, 60)	
client.loop_forever()
