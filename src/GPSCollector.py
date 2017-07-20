from sys import argv
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
		try:
			report = self.sessoin.next()
			#wait for a 'TPV' report and exact the datata from it
			if report['class'] == 'TPV':
				longitude = report.__getitem__('lon')
				latitude = report.__getitem__('lat')
			return [int(longitude), int(latitude)]
		except :
			#return "GPS data currently not available."
			return [23,22]

	#NEED TO BE TESTED!!!!!!!
	def synchRaspiTime(self):
		try:
			report = self.sessoin.next()
			#wait for a 'TPV' report and exact the datata from it
			if report['class'] == 'TPV':
				time = report.__getitem__('time')
			#gpsd.utc is formatted like"2015-04-01T17:32:04.000Z"
    		#convert it to a form the date -u command will accept: "20140401 17:32:04"
    		#use python slice notation [start:end] (where end desired end char + 1)
    		#gpsd.utc[0:4] is "2015"
    		#gpsd.utc[5:7] is "04"
    		#gpsd.utc[8:10] is "01"
    		gpsutc = time[0:4] + time.utc[5:7] + time[8:10] + ' ' + gps[1d1:19]
			os.system('sudo date -u --set="%s"' % gpsutc)
		except :
			#return "GPS data currently not available."
			print 'Synchonization with GPS time failed!'


	#NEED TO BE TESTED!!!!!!!
	def getGridNum(self):
		rotationMatrix = np.array([30, 10], [-17.5, 173])
		gpsKoordinate = self.getData()
		result = rotationMatrix.dot(gpsKoordinate - np.array[8.8, 47.65])
		np.rint(result).tolist()
		return result