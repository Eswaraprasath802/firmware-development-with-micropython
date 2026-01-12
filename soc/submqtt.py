import paho.mqtt.client as paho

def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed: "+str(mid)+" "+str(granted_qos))

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.qos)+" "+str(msg.payload))    

client = paho.Client(paho.CallbackAPIVersion.VERSION1)
client.on_subscribe = on_subscribe
client.on_message = on_message
client.username_pw_set("eswaraprasath_hello_world:Eswaraprasath", "CH3COONA")
client.connect('rabbitmq.selfmade.ninja', 1883)
client.subscribe('v1/temperature', qos=1)

client.loop_forever()
