from Entity import *
from GPSCollector import *
from geojson import Point, Feature
import urllib2
import os
from ConfigParser import SafeConfigParser
import sys



def regist(entity, path = 'http://localhost:8080'):
	data = entity.jsonSerialize()
	url = path + '/SensorThingsServer-1.0/v1.0/' + entity.__class__.__name__ +'s'
	if(isinstance(entity, FeaturesOfInterest)):
		url = 'http://localhost:8080/SensorThingsServer-1.0/v1.0/FeaturesOfInterest'
	req = urllib2.Request(url, data, {'Content-Type': 'application/json'})
	f = urllib2.urlopen(req)
	responseHeader = f.info().headers[0]
	f.close()
	return responseHeader

def getIOTid(response):
	location = str(response)
	idInString = location[location.find("(")+1:location.find(")")]
	return int(idInString)


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


#Set the path variable by the system argument
path = sys.argv[1]


#The following create a serie of entities. The identifier on each Raspi is the serial number
serialNum = getserial()

#Construct a new location based on the gps data
locationDescripton = "The start point of the sourcing node: " + serialNum + "."
gpsCoordinate = GPS().getData()
geoLocation = Feature(geometry = Point(gpsCoordinate))
location = Location(serialNum, locationDescripton, geoLocation)


#Construct the Sensor entity
sensor = Sensor("Temperatur Sensor " + serialNum , "The temperature sensor on the Raspi " + serialNum)

#Construct the ObservedProperty entity
observedProperty = ObservedPropertie("Temperatur", "http://dbpedia.org/page/Dew_point", "Temperature")

#Construct the Thing entity
thingName = serialNum
thingDescription = "This is a sourcing node of Rapberry Pi with the serial number " + thingName + "."
thing = Thing(thingName, thingDescription, location)

thingRes = regist(thing, path)
thingID = getIOTid(thingRes)

sensorRes = regist(sensor, path)
sensorID = getIOTid(sensorRes)

locationRes = regist(location, path)
locationID = getIOTid(locationRes)

observedPropertyRes = regist(observedProperty, path)
observedPropertyID = getIOTid(observedPropertyRes)

#Construct the Datastream entity
unitOfMeaturement =  {
      "name":
  "degree Celsius",
      "symbol":
  "C",
      "definition":
  "http://unitsofmeasure.org/ucum.html#para-30"
    }

dataStream = Datastream("Datastream " + serialNum, 
	"The datastream measured by the Raspi " + serialNum, 
	unitOfMeaturement,
	"http://www.opengis.net/def/observationType/OGC-OM/2.0/OM_Measurement",
	{"@iot.id": thingID}, {"@iot.id": sensorID}, {"@iot.id": observedPropertyID})

dataStreamRes = regist(dataStream, path)
dataStreamID = getIOTid(dataStreamRes)


################################################################
#Create a FeatureOfInterest
foI = FeaturesOfInterest("testFOI", "tesi FOI", "applicationvnd.geojson", geoLocation)
regist(foI)


################################################################
#set up the config file
parser = SafeConfigParser()
parser.read('../observation.ini')
parser.set('register', 'dataStreamID', dataStreamID)
parser.set('register', 'sensorID', sensorID)
parser.set('register', 'thingID', thingID)
parser.set('register', 'startLocationID', startLocationID)
parser.set('register', 'registered', true)

with open('../observation.ini', 'w') as configfile:
    parser.write(configfile)
 