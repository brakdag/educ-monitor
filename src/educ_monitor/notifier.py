from config import config
import paho.mqtt.client as mqtt
import json
import time
import os

def format_notification(raw_data):
    """Filters the payload for MQTT notification."""
    
    # Extract ID
    escuela_info = raw_data.get("lugar_trabajo", "")
    escuela_id = escuela_info.split(' - ')[0] if ' - ' in escuela_info else escuela_info
    
    # Basic info
    filtered_data = {
        "escuela": escuela_id,
        "materia": raw_data.get("materia"),
        "articulo": raw_data.get("articulo")
    }
    
    # Conditional Date fields
    for i in range(1, 5):
        key = f"fecha_llamado_{i}"
        val = raw_data.get(key)
        if val is not None:
            filtered_data[key] = val
            
    return filtered_data

def notify_home_assistant(llamado):
    # Filter the payload
    payload_data = format_notification(llamado)
    
    # Retrieve MQTT settings from config
    if config.TEST_MODE:
        print(f"--- [TEST MODE] Notification to MQTT ---")
        print(f"Topic: {config.MQTT_TOPIC}")
        print(f"Payload: {json.dumps(payload_data, indent=2)}")
        print(f"----------------------------------------")
        return

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
        print(f"DEBUG: Attempting to connect to {broker}:{port}")
        client.connect(broker, port, 60)
        client.loop_start()
        
        # Publish message
        payload = json.dumps(payload_data)
        client.publish(topic, payload, retain=True)
        
        time.sleep(1) # Ensure message is sent
        client.loop_stop()
        client.disconnect()
        print(f"Notification sent to MQTT topic: {topic}")
    except Exception as e:
        print(f"Error sending MQTT notification: {e}")

