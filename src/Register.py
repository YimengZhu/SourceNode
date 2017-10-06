
from Entity import *
import GPSReader
from geojson import Point, Feature
import urllib2
import os
import ConfigParser
import sys
import re


def regist(data, serverPath, urltail):
    print data
    url = serverPath + '/SensorThingsServer-1.0/v1.0/' + urltail
    print url
    req = urllib2.Request(url, data, {'Content-Type': 'application/json'})
    f = urllib2.urlopen(req)
    responseHeader = f.info().headers[0]
    f.close()
    return responseHeader

def getIOTid(response):
    print response
    lastPart = response.split('/')[-1]
    idInResponse = int(re.search(r'\d+', lastPart).group())
    return idInResponse

def getserial():
    # Extract serial from cpuinfo file
    cpuserial = "dummy"
    try:
      f = open('/proc/cpuinfo','r')
      for line in f:
        if line[0:6]=='Serial':
          cpuserial = line[10:26]
      f.close()
    except:
      cpuserial = "ERROR000000000"

    return cpuserial


#Set the path variable based on a config file.
config = ConfigParser.SafeConfigParser()
config.read('../config.ini')
serverPath = 'http://' + str(config.get('server', 'serverPath'))
print 'registering to ther server at ' + serverPath

#The following create a serie of entities. The identifier on each Raspi is the serial number
serialNum = getserial()

#Construct a new location based on the gps data
locationDescripton = "The start point of the sourcing node: " + serialNum + "."
gpsCoordinate = GPSReader.getData()
geoLocation = Feature(geometry = Point(gpsCoordinate))
location = Location(serialNum, locationDescripton, geoLocation)

#register the thing
thing = Thing(serialNum, "Sensing node on the raspi with serial number " + serialNum, location)
thingRes = regist(thing.jsonSerialize(), serverPath, 'Things')
thingID = getIOTid(thingRes)

#register the sensor
sensor = Sensor("Temperatur Sensor " + serialNum , "The temperature sensor on the Raspi " + serialNum)
sensorRes = regist(sensor.jsonSerialize(), serverPath, 'Sensors')
sensorID = getIOTid(sensorRes)

#register the location
locationRes = regist(location.jsonSerialize(), serverPath, 'Locations')
locationID = getIOTid(locationRes)

#register the ObservedProperties
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
    print('registering the ' + str(i) + ' observed properties.')
    res = regist(json.dumps(jsonString), serverPath, 'ObservedProperties')
    observedPropertiesID.append(getIOTid(res))

print 'Starting to register the datastreams.'
datastreamID = {}
unitOfMeasurements = [
    {
        "name" : "degree Celsius",
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
    res = regist(json.dumps(jsonString), serverPath, 'Datastreams')
    iotId = getIOTid(res)
    datastreamID.update({properties[i]:iotId})

#Register the feature of interest
foiFeature = {
    "type" : "Feature",
    "geometry" : {
            "type" : "Point",
            "coordinates" : [0, 0]
        }
    }
foi = FeaturesOfInterest(serialNum, 'The boat with Raspi ' + serialNum, 'application.geo+json', foiFeature)
foiRes = regist(foi.jsonSerialize(), serverPath, 'FeaturesOfInterest')
foiId = getIOTid(foiRes)
print foiId

################################################################
#set up the config file
parser = ConfigParser.SafeConfigParser()
parser.read('../config.ini')

parser.set('register', 'sensorID', str(sensorID))
parser.set('register', 'thingID', str(thingID))
parser.set('register', 'startLocationID', str(locationID))
parser.set('register', 'foi', str(foiId))
parser.set('register', 'registered', 'true')
parser.set('register', 'serialNum',serialNum)
for key,value in datastreamID.items():
    parser.set('datastreamid', key, str(value))

with open('../config.ini', 'w') as configfile:
    parser.write(configfile)

 
