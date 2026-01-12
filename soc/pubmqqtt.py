import paho.mqtt.client as paho
import time
import random

def on_publish(client, userdata, mid):
    print("published: "+str(mid))
    
# Define event callbacks
def on_connect(client, userdata, flags, rc):
    print("connected: " + str(rc))

def on_message(client, obj, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))

def on_publish(client, obj, mid):
    print("mid: " + str(mid))

def on_subscribe(client, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

def on_log(client, obj, level, string):
    print(string)
 
client = paho.Client(paho.CallbackAPIVersion.VERSION1)
client.on_publish = on_publish
client.on_message = on_message
client.on_connect = on_connect
client.on_subscribe = on_subscribe
client.username_pw_set("eswaraprasath_hello_world:Eswaraprasath", "CH3COONA")
client.connect('rabbitmq.selfmade.ninja', 1883)
client.loop_start()

while True:
    temperature = random.random() * 100
    (rc, mid) = client.publish('v1/temperature', str(temperature), qos=1)
    time.sleep(1)
