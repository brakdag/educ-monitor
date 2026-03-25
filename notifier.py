from config import config
import paho.mqtt.client as mqtt
import json
import time
import os

def notify_home_assistant(llamado):
    # Retrieve MQTT settings from config
    broker = config.MQTT_BROKER
    port = config.MQTT_PORT
    topic = config.MQTT_TOPIC
    user = os.getenv("MQTT_USER")
    password = os.getenv("MQTT_PASSWORD")

    # Create client
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    
    if user and password:
        client.username_pw_set(user, password)
    
    try:
        client.connect(broker, port, 60)
        client.loop_start()
        
        # Publish message
        payload = json.dumps(llamado)
        client.publish(topic, payload, retain=True)
        
        time.sleep(1) # Ensure message is sent
        client.loop_stop()
        client.disconnect()
        print(f"Notification sent to MQTT topic: {topic}")
    except Exception as e:
        print(f"Error sending MQTT notification: {e}")
