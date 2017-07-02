import paho.mqtt.publish as publisher

class MqttConfig:
    'A class to configure the mqtt connection'
    def __init__(self, hostname = 'localhost', port = 1883, qos = 2):
        self.hostname = hostname
        self.port = port
        self.qos = qos
        self.client_id = None

class Wrapper:
    'A generic wrapper class to capsulte all the sensor value to be ready for publishing to mqtt broker.'
   
    def __init__(self, value, topic, mqttConfig = MqttConfig()):
        self.value = value
        self.topic = topic
        self.mqttConfig = mqttConfig
        self.mqttConfig.client_id = topic


    def mqtt_send_data(self):
        msg = self.formatMsg();
        publisher.single(self.topic, msg, hostname=self.mqttConfig.hostname, port=self.mqttConfig.port, qos=self.mqttConfig.qos, client_id=self.mqttConfig.client_id)

    def formatMsg(self):
        result = "{topic: " + self.topic + ", value: " + str(self.value) + " }"
        return result

