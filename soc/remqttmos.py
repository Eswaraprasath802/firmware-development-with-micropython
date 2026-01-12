import paho.mqtt.client as mqtt
from pymongo import MongoClient
from datetime import datetime
import sys

# --- CONFIGURATION ---
PI_IP = "10.54.199.96" 
MONGO_URI = "mongodb://localhost:27017/" 

# --- STEP 1: SET UP MONGODB ---
try:
    mongo_client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=2000)
    db = mongo_client["Eswaraprasath_Iot"] 
    collection = db["UltrasonicReadings"]
    
    # Trigger a call to verify connection
    mongo_client.server_info() 
    print("✅ Connected to MongoDB successfully!")
except Exception as e:
    print(f"❌ MongoDB Connection Error: {e}")
    sys.exit(1)

# --- STEP 2: MQTT LOGIC ---
# Fix: Ensure the parameters match Paho MQTT V2 requirements
def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print(f"✅ Connected to Pi! Subscribing to 'sensor/distance'...")
        client.subscribe("sensor/distance")
    else:
        print(f"❌ Connection failed with code {rc}")

def on_message(client, userdata, msg):
    try:
        # Decode the payloady

        raw_payload = msg.payload.decode()
        val = float(raw_payload)
        
        # Prepare the Data Document
        document = {
            "distance_cm": val,
            "timestamp": datetime.now(), 
            "device": "Raspberry Pi Zero"
        }
        
        # Insert into MongoDB
        result = collection.insert_one(document)
        print(f"💾 [{datetime.now().strftime('%H:%M:%S')}] Stored: {val} cm")
        
    except ValueError:
        print(f"⚠️ Warning: Received non-numeric data: {msg.payload.decode()}")
    except Exception as e:
        print(f"❌ Error saving to DB: {e}")

# --- STEP 3: START THE BRIDGE ---
# Using CallbackAPIVersion.VERSION2 as you correctly specified
client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message

print(f"Connecting to Pi at {PI_IP}...")

try:
    client.connect(PI_IP, 1883, 60)
    # This keeps the script running and listening
    client.loop_forever()
except KeyboardInterrupt:
    print("\nStopping the receiver...")
    sys.exit(0)
except Exception as e:
    print(f"❌ Could not connect to MQTT Broker: {e}")
