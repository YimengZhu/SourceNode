from Entity import *
from GpsDataCollector import *
from geojson import Point, Feature
import urllib2

def regist(entity):
	print(1)
	data = entity.jsonSerialize()
	url = 'http://localhost:8080/SensorThingsServer-1.0/v1.0/' + entity.__class__.__name__ +'s'
	print(url)
	req = urllib2.Request(url, data, {'Content-Type': 'application/json'})
	f = urllib2.urlopen(req)
	for x in f:
		print(x)
	f.close()

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
delattr(geoLocation, 'properties')
location = Location(serialNum, locationDescripton, geoLocation)
print(location.jsonSerialize())



#Construct the Sensor entity
sensor = Sensor("Tem" + serialNum , "The temperature sensor on the Raspi " + serialNum)

#Construct the ObservedProperty entity
observedProperty = ObservedPropertie("Temperatur", "http://dbpedia.org/page/Dew_point", "Temperature")

#Construct the Thing entity
name = serialNum
thingDescription = "This is a sourcing node of Rapberry Pi with the serial number " + name + "."
thing = Thing(name, thingDescription, location)

regist(thing)
regist(sensor)
regist(location)
regist(observedProperty)
