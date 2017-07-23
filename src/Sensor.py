from datetime import datetime
import paho.mqtt.client as mqtt
from MqttWraper import Wrapper


currentVal = 0
counter = 0


#The callback for when the client receives a CONNACK response rc from the server.
def on_connect(client, userdata, flags, rc):
	print("Connected with result code " + str(rc))

	#Subscribing in on_connect means that if the connection is losed,
	#the subscription will be renewd on reconnection.
	client.subscribe("temperature")


def on_message(client, userdata, msg):
	#This callback do the following:
	#1. Listen on the mqtt broker to get the mesurement result.
	#2. Compute the mean of the current value and the recieving result.
	measurment = int(msg.payload)
	global currentVal
	currentVal = (currentVal * counter + measurment) / (counter + 1)
	counter += 1
	wrapper = Wrapper(currentVal)
	wrapper.mqtt_send_data()
	del wrapper

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message


client.connect("localhost", 1883, 60)	
client.loop_forever()