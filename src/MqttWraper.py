import paho.mqtt.publish as publisher
from GPSCollector import *
from Entity import Observation
import datetime
import ConfigParser

class MqttConfig:
    'A class to configure the mqtt connection'
    def __init__(self, hostname = 'localhost', port = 1883, qos = 2):
        self.hostname = hostname
        self.port = port
        self.qos = qos
        self.client_id = None

class Wrapper:
    'A generic wrapper class to capsulte all the sensor value to be ready for publishing to mqtt broker.'
   
    def __init__(self, value, topic = 'v1.0/Observations', mqttConfig = MqttConfig()):
        config = ConfigParser.SafeConfigParser()
        config.read('../observation.ini')
        dataStreamID = int(config.get('entities', 'datastreamid'))

        self.observation = Observation(datetime.datetime.now().isoformat(),
            value,
            datetime.datetime.now().isoformat(),
            {"@iot.id": dataStreamID},
            {"@iot.id": self.getFeatureOfInterest()})

        self.topic = topic
        self.mqttConfig = mqttConfig
        self.mqttConfig.client_id = topic


    def mqtt_send_data(self):
        msg = self.observation.jsonSerialize();
        publisher.single(self.topic, msg, hostname=self.mqttConfig.hostname, port=self.mqttConfig.port, qos=self.mqttConfig.qos, client_id=self.mqttConfig.client_id)

    def formatMsg(self):
        result = "{topic: " + self.topic + ", value: " + str(self.value) + " }"
        return result



    #TODO: Implement!!!!! Calculate the grid id based on the gps coordinate
    def getFeatureOfInterest(self):
        return 1


wrapper = Wrapper(2).mqtt_send_data()