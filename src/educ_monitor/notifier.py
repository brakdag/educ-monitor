from educ_monitor.config import config
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

def connect_mqtt():
    if config.TEST_MODE:
        return None
    broker = config.MQTT_BROKER
    port = config.MQTT_PORT
    user = os.getenv("MQTT_USER")
    password = os.getenv("MQTT_PASSWORD")
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    if user and password:
        client.username_pw_set(user, password)
    try:
        client.connect(broker, port, 60)
        client.loop_start()
        return client
    except Exception as e:
        print(f"Error connecting to MQTT: {e}")
        return None

def publish_mqtt(client, llamado):
    payload_data = format_notification(llamado)
    if config.TEST_MODE:
        print(f"--- [TEST MODE] Notification to MQTT ---")
        print(f"Topic: {config.MQTT_TOPIC}")
        print(f"Payload: {json.dumps(payload_data, indent=2)}")
        print(f"----------------------------------------")
        return
    if client:
        try:
            payload = json.dumps(payload_data)
            client.publish(config.MQTT_TOPIC, payload, retain=True)
            time.sleep(0.5)
        except Exception as e:
            print(f"Error publishing to MQTT: {e}")

def disconnect_mqtt(client):
    if client:
        client.loop_stop()
        client.disconnect()


