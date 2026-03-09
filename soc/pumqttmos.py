import paho.mqtt.client as mqtt
import time
import random

PI_IP = "192.168.1.45"   # Raspberry Pi IP address 
# if the mosquito is installed in the publisher you can simply use localhost

client = mqtt.Client()

# connect to Mosquitto broker on Raspberry Pi
client.connect(PI_IP,1883)

client.loop_start()

while True:
    temperature = random.uniform(20,40)
    client.publish("v1/temperature", temperature)
    print("Published:", temperature)
    time.sleep(2)