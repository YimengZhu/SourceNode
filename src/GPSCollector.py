import os
import sys
import gps
import gpxpy
import gpxpy.gpx
import numpy as np

class GPS:
	'This class will build the connection to the gps and collect the data from it.'
	
	def __init__(self, ip = 'localhost', port = '2947'):
		self.ip = ip
		self.port = port
		self.session = gps.gps(ip, port)
		self.session.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)

	def getData(self):
		#report = self.session.next()
		##wait for a 'TPV' report and exact the datata from it
		#while report['class'] != 'TPV':
		#    report = self.session.next()
		
		#longitude = report.__getitem__('lon')
		#latitude = report.__getitem__('lat')
		#result = [int(longitude), int(latitude)]
		return [1,1]


	def synchRaspiTime(self):
		report = self.session.next()
		#wait for a 'TPV' report and exact the datata from it
		while report['class'] != 'TPV':
		    report = self.session.next()
		time = report.__getitem__('time')
		#gpsd.utc is formatted like"2015-04-01T17:32:04.000Z"
    		#convert it to a form the date -u command will accept: "20140401 17:32:04"
		#use python slice notation [start:end] (where end desired end char + 1)
		#gpsd.utc[0:4] is "2015"
		#gpsd.utc[5:7] is "04"
         	#gpsd.utc[8:10] is "01"
    		gpsutc = time[0:4] + time[5:7] + time[8:10] + ' ' + time[11:19]
		print(gpsutc)
		os.system('sudo date -u --set="%s"' % gpsutc)


	#NEED TO BE TESTED!!!!!!!
	def getGridNum(self):
#		rotationMatrix = np.array([30, 10], [-17.5, 173])
#		gpsKoordinate = self.getData()
#		result = rotationMatrix.dot(gpsKoordinate - np.array[8.8, 47.65])
#		np.rint(result).tolist()
		return 2589

#gps = GPS()
#gps.synchRaspiTime()
#while True:
#    print gps.getData()
