import json


class Entity:
	def jsonSerialize(self):
		#dictFilter = dict((k, v) for k, v in self.__dict__.iteritems() if v is not None)
		#print(dictFilter)
		#return json.dumps(dictFilter)
		return json.dumps(self, default = lambda o:dict((k,v) for k,v in o.__dict__.iteritems() if v is not None))


class Thing(Entity):

	def __init__(self, name, description, properties = None,
		location = None, historical_location = None, dataStream = None):
		#init the properties
		self.name = name
		self.description = description
		self.properties = properties
		#init the relations
		self.locatons = [].append(location)
		self.historical_locations = [].append(historical_location)
		self.dataStream = [].append(dataStream)


class Location(Entity):

	def __init__(self, name, description, location,
		encodingType = "applicationvnd.geojson"):
		#init the properties
		self.name = name
		self.description = description
		self.encodingType = encodingType
		self.location = location



class HistoricalLocation(Entity):
	def __init__(self, time, location, thing):
		self.time = time
		self.thing = thing
		self.location = [location]


class Datastream(Entity):
	def __init__(self, name, description, unitOfMeasurement, observationType, 
		thing, sensor, observedProperty, observation = None,
		observatedArea = None, phenomenonTime = None, resultTime = None):
		#init the properties
		self.name = name
		self.description = description
		self.unitOfMeasurement = unitOfMeasurement
		self.observationType = observationType
		self.observatedArea = observatedArea
		self.phenomenonTime = phenomenonTime
		self.resultTime = resultTime
		#init the relations
		self.Thing = thing
		self.Sensor = sensor
		self.ObservedProperty = observedProperty
		self.Observation = observation





class Sensor(Entity):
	def __init__(self, name, description, encodingType = "application/pdf", metadata = " ", dataStream = None ):
		self.name = name
		self.description = description
		self.encodingType = encodingType
		self.metadata = metadata
		self.dataStream = dataStream

class ObservedPropertie(Entity):
	def __init__(self, name, definition, description, dataStream = None):
		self.name = name
		self.definition = definition
		self.description = description
		self.dataStream = dataStream

class Observation(Entity):
	def __init__(self, phenomenonTime, result, resultTime, 
		dataStream, featureOfInterest,
		resultQuality = None, validTime = None, parameters = None):
		#init the properties
		self.phenomenonTime = phenomenonTime
		self.result = result
		self.resultTime = resultTime
		self.resultQuality = resultQuality
		self.validTime = validTime
		self.parameters = parameters
		#init the relations
		self.Datastream = dataStream
		self.FeatureOfInterest = featureOfInterest



class FeaturesOfInterest(Entity):
	def __init__(self, name, description, encodingType, feature, observation = None):
		self.name = name
		self.description = description
		self.encodingType = encodingType
		self.feature = feature
		self.observation = [].append(observation)
