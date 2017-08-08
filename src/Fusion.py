import paho.mqtt.client as mqtt
#from MqttWraper import Wrapper
from datetime import datetime
from GPSCollector import GPS
import sqlite3

dbconnect = sqlite3.connect("../sensorData.db")
cursor = dbconnect.cursor()
gps = GPS()

#The callback for when the client receives a CONNACK response rc from the server.
def on_connect(client, userdata, flags, rc):
	print("Connected with result code " + str(rc))

	#Subscribing in on_connect means that if the connection is losed,
	#the subscription will be renewd on reconnection.
	client.subscribe("Temperature")


def on_message(client, userdata, msg):
    #This callback do the following:
    #1. Listen on the mqtt broker to get the mesurement result.
    measurement = float(msg.payload)
    topic = msg.topic
        
    #2. get the value from the database based on the location and topic
    gridID = gps.getGridNum() 
    cursor.execute("SELECT value FROM sensorData WHERE gridID=? And topic=?", (gridID, topic))
    result = cursor.fetchall()
    if len(result) == 0:
        print 'No entry in for this FOI and topic in the database. Use current value as the initial value.'
        cursor.execute("INSERT INTO sensorData VALUES (?,?,?)", (gridID, topic,measurement))
    elif len(result) == 1:
        print result[0][0]
	newVal = ( result[0][0] + measurement ) / 2
	
        cursor.execute("UPDATE sensorData SET value = ? WHERE gridID = ? AND topic = ?", (newVal, gridID, topic))        
    else:
        raise 'More than one entry for this area and topic is inserted in the database!'
     

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message


client.connect("localhost", 1883, 60)	
client.loop_forever()
