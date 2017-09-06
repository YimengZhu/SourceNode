import json
import numpy as np
import urllib2
import re

def getIDfromResponse(res):
	lastPart = res.split('/')[-1]
	idInResponse = int(re.search(r'\d+', lastPart).group())
	return idInResponse

def regist(data, urltail):
	print(data)
	url = 'http://localhost:8080/SensorThingsServer-1.0/v1.0/' + urltail
	print url
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


print 'Starting to register the FeatureOfInterest.'
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
	res = regist(json.dumps(jsonString), 'FeaturesOfInterest')
	print getIDfromResponse(res)

print 'Starting to register the ObservedProperties.'
properties = ['Temperature', 'temp_in', 'abs_pressure', 'hum_in', 'temp_out', 'wind_dir', 'hum_out', 'wind_gust', 'wind_ave', 'rain']
definitions = ['', '', '', '', '', '', '', '', '', '']
descriptions = ['', '', '', '', '', '', '', '', '', '']
observedPropertiesID = []
for i in range(10):
	jsonString = {
		"name" : properties[i],
		"definition" : definitions[i],
		"description" : descriptions[i],
	}
	print('registering the ' + str(i) + 'observed properties.')
	res = regist(json.dumps(jsonString), 'ObservedProperties')
	observedPropertiesID.append(getIDfromResponse(res))

print 'Starting to register the datastreams.'
unitOfMeasurements = [
	{"name" : "degree Celsius",
	 "symbol" : "C",
	 "definition" : "http://unitsofmeasure.org/ucum.html#para-30"
	},
	{"name" : "degree Celsius",
	 "symbol" : "C",
	 "definition" : "http://unitsofmeasure.org/ucum.html#para-30"
	},
	{"name" : "Pasca",
	 "symbol" : "Pa",
	 "definition" : "http://unitsofmeasure.org/ucum.html#para-30"
	},
	{"name" : "Percent",
	 "symbol" : "%",
	 "definition" : "http://unitsofmeasure.org/ucum.html#para-30"
	},
	{"name" : "degree Celsius",
	 "symbol" : "C",
	 "definition" : "http://unitsofmeasure.org/ucum.html#para-30"
	},
	{"name" : "grade",
	 "symbol" : "grade",
	 "definition" : "http://unitsofmeasure.org/ucum.html#para-30"
	},
	{"name" : "Percent",
	 "symbol" : "%",
	 "definition" : "http://unitsofmeasure.org/ucum.html#para-30"
	},
	{"name" : "kilometer pro hour",
	 "symbol" : "km/h",
	 "definition" : "http://unitsofmeasure.org/ucum.html#para-30"
	},
	{"name" : "kilometer pro hour",
	 "symbol" : "km/h",
	 "definition" : "http://unitsofmeasure.org/ucum.html#para-30"
	},
	{"name" : "minimeter",
	 "symbol" : "mm",
	 "definition" : "http://unitsofmeasure.org/ucum.html#para-30"
	},
]
for i in range(10):
	jsonString = {
		"name" : "Datastream for " + properties[i],
		"description" : "The datastram for the measurement of " + properties[i],
		"unitOfMeasurement" : unitOfMeasurements[i],
		"observationType" : "http://www.opengis.net/def/observationType/OGC-OM/2.0/OM_Measurement",
		"Thing" : { "@iot.id" : 1},
		"Sensor" : { "@iot.id" : 1},
		"ObservedProperty" : {"@iot.id" : observedPropertiesID[i]}
	}
	print('registering the ' + str(i) + ' datastream.')
	res = regist(json.dumps(jsonString), 'Datastreams')
	print res

print 'Register finished!'
