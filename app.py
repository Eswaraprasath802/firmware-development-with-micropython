import network
from time import sleep as time
from umqttsimple import MQTTClient
from machine import Timer

def on_message(topic,msg):
    print(topic)
    print(msg)

def connect_mqtt():
    global mqtt_client_id,mqtt_username,mqtt_password,mqtt_server,mqtt_port
    client=MQTTClient(mqtt_client_id,mqtt_server,mqtt_port,mqtt_username,mqtt_password)
    client.set_callback(on_message)
    print(" i am here")
    client.connect()
    print("connected")
    client.subscribe('v1/temperature')
    print("connected and subscribe to Mqtt")
    return client

nic = network.WLAN(network.WLAN.IF_STA)
nic.active(True)
a=nic.scan()
for i in a:
    ssid,bssid,channel,RSSI,security,hidden=i
    if ssid.decode().strip()==ssid_hostname:
        nic.connect(ssid_hostname,password)
while(nic.status()==1):
    time(0.1)
    pass
print("Ready with network",nic.ifconfig())
h=connect_mqtt()
def read(t):
    h.check_msg()
tim=Timer(1)
tim.init(mode=Timer.PERIODIC, period=1000, callback=read)

