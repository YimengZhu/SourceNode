import datetime
import socket
import zlib
import pysmile
import json
import urllib2 
import binascii
from Entity import Observation

UDP_IP = "10.42.0.1"
UDP_PORT = 5005

def createObservation(observation):
	data = observation.jsonSerialize() 
	print data
	url = 'http://localhost:8080/SensorThingsServer-1.0/v1.0/Observations'
	req = urllib2.Request(url, data, {'Content-Type': 'application/json'})
	f = urllib2.urlopen(req)
	responseHeader = f.info().headers[0]
	f.close()
	return responseHeader


def decodeMessage(msg):
	hexString = binascii.hexlify(msg)
	
	timestample = datetime.datetime.fromtimestamp((int(hexString[0:8], 16))).isoformat()
	foi = int(hexString[8:10], 16)
	datastream = int(hexString[10:11], 16)
	value = int(hexString[11:], 16) / 100.00

	observation = Observation(timestample,
            value,
            timestample,
            {"@iot.id": datastream},
			{"@iot.id": foi})

	return observation

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

sock.bind((UDP_IP, UDP_PORT))

while True:
    data, addr = sock.recvfrom(1024)
    observation = decodeMessage(data)
    createObservation(observation)
    