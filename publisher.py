import time
import paho.mqtt.client as mqtt


mqttc = mqtt.Client()
mqttc.connect("localhost", 1883, 60)

mqttc.loop_start()

a = 0
def gernerateNum():
    global a
    a += 1
    print(a)
    return a

while 1:
    t = gernerateNum()
    (result,mid)=mqttc.publish("Temperatur", t, 2)
    time.sleep(2)

mqtt.loop_stop()
mqttc.disconnect()
