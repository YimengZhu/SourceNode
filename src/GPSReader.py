import urllib2
import os
import sys
import gps
import gpxpy
import gpxpy.gpx
import numpy as np
import paho.mqtt.publish as publish
import math
from Entity import Location	
from geojson import Point, Feature
import ConfigParser

session = gps.gps('localhost', '2947')
session.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)
currentPos = None


def getData():
    report = session.next()
    #wait for a 'TPV' report and exact the datata from it
    while report['class'] != 'TPV':
        report = session.next()
    try:
        longitude = report.__getitem__('lon')
        latitude = report.__getitem__('lat')
        result = (longitude, latitude)
        return result
    except KeyError:
        print 'No coordinate in TPV object, please try with next session.'
        
def synchRaspiTime():
    report = session.next()
    #wait for a 'TPV' report and exact the datata from it
    while report['class'] != 'TPV':
        report = session.next()
    time = report.__getitem__('time')
    #gpsd.utc is formatted like"2015-04-01T17:32:04.000Z", convert it to a form the date -u command will accept: "20140401 17:32:04"
    #gpsd.utc[0:4] is "2015", gpsd.utc[5:7] is "04", gpsd.utc[8:10] is "01"
    gpsutc = time[0:4] + time[5:7] + time[8:10] + ' ' + time[11:19]
    print(gpsutc)
    os.system('sudo date -u --set="%s"' % gpsutc)

#NEED TO BE TESTED!!!!!!!
def getGridNum():
    report = session.next()
    #wait for a 'TPV' report and extract the data from it
    while report['class'] != 'TPV':
        report = session.next()
    
    try:
        longtitude = report.__getitem__('lon')
        latitude = report.__getitem__('lat')
        gpsCoordinate = np.array([int(longtitude), int(latitude)])
        rotationMatrix = np.array([[30, 10], [-17.5, 173]]) 
        grid = rotationMatrix.dot(gpsCoordinate - np.array([8.8, 47.65]))
        np.rint(result).tolist()
        print grid
        publish.single('foi', grid, retain = True)
    except KeyError:
        print 'No coordinate in TPV object, please try with next session'

#Calculate the euler distance to last point 
def getDistance():
    coordinate = getData()
    global currentPos
    if currentPos == None:
        currentPos = coordinate
        return 0

    distance = math.sqrt(sum([(a - b) ** 2 for a, b in zip(coordinate, currentPos)]))
    print 'distance to last point is ' + str(distance)
    return distance

def updateLocation():
#    if get_distance() < 15:
#        return
    #consturct a new location entity based on current_pos     
    currentPos = getData()
    if currentPos == None: 
        return
    geoLocation = Feature(geometry = Point(getData()))

    config = ConfigParser.SafeConfigParser()
    config.read('../config.ini')
    
    serialNum = config.get('register', 'serialNum')

    location = Location('Location', 'Location coordinate of ' + serialNum, geoLocation)
    publish.single('v1.0/Things', location.jsonSerialize())
    return location


#regist the location
def registerLocation(location):
    data = location.jsonSerialize()
    print data
    config = ConfigParser.SafeConfigParser()
    config.read('../config.ini')
    thingId = config.get('register', 'thingid')
    serverPath = 'http://' + str(config.get('server','serverPath')) + '/SensorThingsServer-1.0/v1.0/Things(' + thingId + ')/Locations'
    print serverPath    
    req = urllib2.Request(serverPath, data, {'Content-Type' : 'application/json'})
    f = urllib2.urlopen(req)
    f.close
    
if __name__ == '__main__':
    synchRaspiTime()
    while True:
        getData()
        getDistance()
        location = updateLocation()
        if location != None:
            registerLocation(location)
#        getGridNum()
