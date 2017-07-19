from sys import argv
import gps
import gpxpy
import gpxpy.gpx

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
				self.longitude = report.__getitem__('lon')
				self.latitude = report.__getitem__('lat')
			return [self.longitude, self,latitude]
		except :
			#return "GPS data currently not available."
			return [23,22]
