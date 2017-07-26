import json
import numpy as np
import urllib2


def regist(data):
	print(data)
	url = 'http://localhost:8080/SensorThingsServer-1.0/v1.0/FeaturesOfInterest'
	req = urllib2.Request(url, data, {'Content-Type': 'application/json'})
	f = urllib2.urlopen(req)
	responseHeader = f.info().headers[0]
	f.close()
	return responseHeader

def getGPSCoordinate(gridIndex):
	verCoordinate = gridIndex % 8
	horCoordinate = gridIndex / 8 + 1
	matrix = np.array([[30,10],[-17.5, 173]])
	invMatrix = np.linalg.inv(np.array([[30,10],[-17.5, 173]]))
	gpsLeftDown = invMatrix.dot(np.array([horCoordinate - 1, verCoordinate - 1])) + np.array([8.8, 47.65])
	gpsLeftUp = invMatrix.dot(np.array([horCoordinate - 1, verCoordinate])) + np.array([8.8, 47.65])
	gpsRightDown = invMatrix.dot(np.array([horCoordinate, verCoordinate - 1])) + np.array([8.8, 47.65])
	gpsRightUp = invMatrix.dot(np.array([horCoordinate, verCoordinate])) + np.array([8.8, 47.65])
	return [gpsLeftDown.tolist(), gpsLeftUp.tolist(), gpsRightDown.tolist(), gpsRightUp.tolist()]


for i in range(256):
	jsonString = {
		"name" : "Grid " + str(i),
		"description" : "This is the grid at (" + str((i / 8 + 1)) + ", " + str(i % 8) + ").",
		"encodingType" : "applicationvnd.geo+json",
		"feature" : {
			"type" : "Feature",
			"geometry" : {
				"type" : "Polygon",
				"coordinates" : getGPSCoordinate(i)
			}
		}
	}
	print('registering the ' + str(i) + ' foi.')	
	regist(json.dumps(jsonString))

print 'Register finished!'
