from Entity import *
from GpsDataCollector import *
from geojson import Point, Feature
import urllib2

def regist(entity):
	data = entity.jsonSerialize()
	url = 'http://localhost:8080/SensorThingsServer-1.0/v1.0/' + entity.__class__.__name__ +'s'
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

thingRep = regist(thing)
thingID = getIOTid(thingRep)

sensorRep = regist(sensor)
sensorID = getIOTid(sensorRep)

locationRep = regist(location)
locationID = getIOTid(locationRep)

observedPropertyRep = regist(observedProperty)
observedPropertyID = getIOTid(observedPropertyRep)

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

print(dataStream.jsonSerialize())
regist(dataStream)
