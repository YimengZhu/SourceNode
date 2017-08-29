import pywws.WeatherStation as WeatherStation
import paho.mqtt.publish as publish
import time

class WS:
    #This class is a proxy class for the weather station WH1080, 
    #which read the live data in every minute and publish them to fusion

    def __init__(self):
        self.weather_station = WeatherStation.weather_station()

    def updateData(self):
        new_pos = self.weather_station.current_pos()
        new_data = self.weather_station.get_data(new_pos)

        for key, value in new_data.items():
            publish.single(key, str(value))
            print(key, value)

testWS = WS()
while True:
    testWS.updateData()
    time.sleep(2)
