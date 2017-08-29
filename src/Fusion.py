import paho.mqtt.client as mqtt 
from datetime import datetime 
from GPSCollector import GPS 
import sqlite3 
from Wrapper import Wrapper

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
        print result[0][0]
	newVal = ( result[0][0] + measurement ) / 2
	measurement = newVal
        cursor.execute("UPDATE sensorData SET value = ? , updateTime = ? WHERE gridID = ? AND topic = ?", (newVal, timestamp, gridID, topic))        
    else:
        raise 'More than one entry for this area and topic is inserted in the database!'
    
    wrapper = Wrapper(measurement)
    wrapper.mqtt_send_data()
    del wrapper

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message


client.connect("localhost", 1883, 60)	
client.loop_forever()
