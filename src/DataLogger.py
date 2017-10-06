import sqlite3
import paho.mqtt.client as mqtt

dbconnect = sqlite3.connect('../sensorData.db')
cursor = dbconnect.cursor()

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
