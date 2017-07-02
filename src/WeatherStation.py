import pywws.WeatherStation as WeatherStation
import MqttWraper as Wraper

class Sensor:
	def __init__(self, topic):
		self.topic = topic


class WS(Sensor):
	'This class is a proxy for the weather station WH1080, which read the live data in every 5 minute and publish them as a mqtt messages'

	current_data = {
		'status': None,
		'hum_out': None,
		'wind_gust': None, 
		'wind_ave': None, 
		'rain': None, 
		'temp_in': None, 
		'delay': None, 
		'abs_pressure': None, 
		'hum_in': None, 
		'temp_out': None, 
		'wind_dir': None
	}

	def __init__(self):
		self.weather_station = WeatherStation.weather_station()

	def updateData(self):
		new_pos = self.weather_station.current_pos()
		new_data = self.weather_station.get_data(new_pos)
		for topic, value in new_data.items():
			if WS.current_data[topic] != value:
				WS.current_data[topic] = value
				mqttWrapper = Wraper.Wrapper(value, topic)
				mqttWrapper.mqtt_send_data()
				del mqttWrapper


testWS = WS()
testWS.updateData()
