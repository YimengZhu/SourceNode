import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish

message=""
newMessage=""

'''
def on_connectPub(publisher, userdata, flags, rc):
	(result, mid)=publisher.publish("Temperatur", "Publisher connected!", 2)
	print((result,mid))
	print("publisher connceted!")


publisher=mqtt.Client()
publisher.connect_async("localhost", 1884, 60)
publisher.on_connect=on_connectPub
'''


def on_connectSub(subscriber, userdata, flags, rc):
	subscriber.subscribe("Temperatur", 2)
	print("connected!")


def on_message(subscriber, userdata, msg):
	global newMessage
	newMessage=msg.payload
	publish.single("Temperatur", newMessage, hostname="localhost", port=1884, qos=2, client_id="1")
	print(newMessage)

subscriber = mqtt.Client(client_id="1", clean_session=False)

subscriber.on_connect=on_connectSub
subscriber.on_message=on_message

subscriber.connect_async("localhost", 1883, 60)

while 1:
	subscriber.loop_forever()
	'''
	subscriber.loop_start()
	if newMessage==message:
		print("no new message")
	else:
		publish.single("Temperatur", message, 2)
		#print((result, mid), message)
		message=newMessage
	subscriber.loop_stop()
'''
#	publisher.loop_start()

	

#	publisher.loop_stop()

subscriber.disconnect()

'''
class Receiver:
    def __init__(self, graph, timeout):
        self.graph = graph
        self.timeout = timeout

    def on_connect(self, mqttc, obj, flags, rc):
        print("Connected! - " + str(rc))

    def on_message(self, mqttc, obj, msg):
        print(msg.topic+" "+str(msg.qos)+" "+str(msg.payload))

    def on_publish(self, mqttc, obj, mid):
        print("Published! "+str(mid))

    def on_subscribe(self, mqttc, obj, mid, granted_qos):
        print("Subscribed! - "+str(mid)+" "+str(granted_qos))

    def on_log(self, mqttc, obj, level, string):
        print(string)

### MQTT Functions
def on_connect(mqttc, obj, flags, rc):
    print("Connected! - " + str(rc))

def on_message(mqttc, obj, msg):
    print(msg.topic+" "+str(msg.qos)+" "+str(msg.payload))

def on_publish(mqttc, obj, mid):
    print("Published! "+str(mid))

def on_subscribe(mqttc, obj, mid, granted_qos):
    print("Subscribed! - "+str(mid)+" "+str(granted_qos))

def on_log(mqttc, obj, level, string):
    print(string)

if __name__ == "__main__":
    # Handle args
       parser.add_argument('--topic', metavar='base/sub', type=str, nargs='?',)
    parser.add_argument('--host', metavar='url', type=str, nargs='?',
                        help='UQL of MQTT server.')
    parser.add_argument('--graph', metavar='True/False', type=bool, nargs='?')
    parser.add_argument('--timeout', metavar='sec', type=int, nargs='?')
    args = parser.parse_args()
    # MQTT
    mqttc = mqtt.Client()
    # mqttc.on_message = on_message
    mqttc.on_connect = on_connect
    mqttc.on_publish = on_publish
    mqttc.on_subscribe = on_subscribe
    # Uncomment to enable debug messages
    #mqttc.on_log = on_log
    mqttc.connect(args.host, 1883, 60)
    mqttc.subscribe(args.topic, 0)
    # Start to listen    
    while True:
        print mqttc.loop()


'''
