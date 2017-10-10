import sqlite3
import paho.mqtt.client as mqtt
import csv
import datetime

dbconnect = sqlite3.connect('../sensorData.db')
cursor = dbconnect.cursor()

#store the data from last time into a csv and clean them
data = cursor.execute("SELECT * FROM rawdata")
csvFile = str(datetime.datetime.now())
with open('../' + csvFile + '.csv', 'wb') as f:
    writer = csv.writer(f)
    writer.writerows(data)

cursor.execute("DELETE FROM rawdata")


counter = 1

def on_connect(client, userdata, flags, rc):
    print 'starting to log data.'

    client.subscribe("v1.0/Observations")
    client.subscribe("v1.0/Locations")

def on_message(client, userdata, msg):
    payload = msg.payload
    topic = msg.topic

    global counter
    cursor.execute("INSERT INTO rawdata VALUES (?,?,?)", (counter, topic, payload))
    counter += 1
    dbconnect.commit()
    
    print 'logged data with topic: ' + topic + ', ' + payload

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect('localhost', 1883, 60)
client.loop_forever()
