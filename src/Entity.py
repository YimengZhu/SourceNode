import datetime

pathBase = ""

def setPathBase(path)
	pathBase = path

class Entity:
	
	_id = 0

	def __init__(self):
		self.id = _id
		_id += 1
		selfLink = pathBase + '/' + __name__

class Thing(Entity):

	def __init__(self, name, description, properties = None,
		location = None, historical_location = None, ):
		super().__init__()
		#init the properties
		self.name = name
		self.description = description
		self.properties = properties
		#init the relations
		self.locatons = [].append(locaton)
		self.historical_locations = [].append(historical_location)
		self.dataStreams = [].append(dataStream)

	# def locate(self, location):
	# 	if location.__name__ != 'Location':
	# 		raise "The parameter passed in is not a Location entity."
	# 	elif self.location != location:
	# 		self.historical_location.append(HistoricalLocation(datetime.datetime.now().isoformat(), self))
	# 		self.location = location

	# def locate_historical(self, historical_location):
	# 	if historical_location.__name__ = 'HistoricalLocation':
	# 		self.historical_location.append(historical_location)
	# 	else:
	# 		raise "The parameter passed in is not a HistoricalLocation Entity."
	
	# def dataStream(self, dataStream):
	# 	if dataStream.__name__ = 'DataStream':
	# 		self.dataStream.append(dataStream)
	# 	else:
	# 		raise "The parameter passed in is not a Datastream Entity"

class Location(Entity):

	def __init__(self, name, description, 
		thing = None, historical_location = None,
		encodingType = "application/vnd.geo+json"):
		super().__init__()
		#init the properties
		self.name = name
		self.description = description
		self.encodingType = encodingType
		self.historical_location = []
		#init the relations
		self.things = [].append(thing)
		self.historical_location = [].append(historical_location)

	def locate_historical(self, historical_location):
		self.historical_location.append(historical_location)


class HistoricalLocation(Entity):
	def __init__(self, time, location, thing):
		super().__init__()
		self.time = time
		self.thing = thing
		self.location = [location]


class Datastream(Entity):
	def __init__(self, name, description, unitOfMeasurement, observationType, 
		thing, sensor, observedProperty, observation
		observatedArea = None, phenomenonTime = None, resultTime = None):
		super.__init__()
		#init the properties
		self.name = name
		self.description = description
		self.unitOfMeasurement = unitOfMeasurement
		self.observatedType = observationType
		self.observatedArea = observatedArea
		self.phenomenonTime = phenomenonTime
		self.resultTime = resultTime
		#init the relations
		self.thing = thing
		self.sensor = sensor
		self.observedProperty = observedProperty
		self.observation = observation





class Sensor(Entity):
	def __init__(self, name, description, encodingType, metadata, dataStream ):
		super.__init__()
		self.name = name
		self.description = description
		self.encodingType = encodingType
		self.metadata = metadata
		self.dataStream = dataStream

class ObservedProperty(Entity):
	def __init__(self, name, definition, description, dataStream):
		super.__init__()
		self.name = name
		self.definition = definition
		self.description = description
		self.dataStream = dataStream

class Observation(Entity):
	def __init__(self, phenomenonTime, result, resultTime, 
		dataStream, featureOfInterest,
		resultQuality = None, validTime = None, parameters = None):
		super().__init__()
		#init the properties
		self.phenomenonTime = phenomenonTime
		self.result = result
		self.resultTime = resultTime
		self.resultQuality = resultQuality
		self.validTime = validTime
		self.parameters = parameters
		#init the relations
		self.dataStream = dataStream
		self.featureOfInterest = featureOfInterest



class FeatureOfInterest(Entity):
	def __init__(self, name, description, encodingType, feature, observation):
		self.name = name
		self.description = description
		self.encodingType = encodingType
		self.feature = feature
		self.observation = observation
