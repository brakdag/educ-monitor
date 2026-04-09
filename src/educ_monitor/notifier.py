import json
import time
import os
import paho.mqtt.client as mqtt
from .config import config
from .logger import get_logger

logger = get_logger("notifier")

def format_notification(raw_data: dict) -> dict:
    """
    Filters and formats the raw API data for MQTT notification.
    """
    escuela_info = raw_data.get("lugar_trabajo", "")
    escuela_id = escuela_info.split(' - ')[0] if ' - ' in escuela_info else escuela_info
    
    notification = {
        "escuela": escuela_id,
        "materia": raw_data.get("materia"),
        "articulo": raw_data.get("articulo")
    }
    
    for i in range(1, 5):
        key = f"fecha_llamado_{i}"
        val = raw_data.get(key)
        if val:
            notification[key] = val
            
    return notification

def connect_mqtt() -> mqtt.Client | None:
    """
    Establishes a connection to the MQTT broker.
    """
    if config.test_mode:
        logger.info("MQTT connection skipped: TEST_MODE is enabled.")
        return None

    user = os.getenv("MQTT_USER")
    password = os.getenv("MQTT_PASSWORD")
    
    try:
        client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        if user and password:
            client.username_pw_set(user, password)
            
        client.connect(config.mqtt_broker, config.mqtt_port, 60)
        client.loop_start()
        logger.info(f"Connected to MQTT broker at {config.mqtt_broker}:{config.mqtt_port}")
        return client
    except (mqtt.MQTTException, OSError) as e:
        logger.error(f"Failed to connect to MQTT broker: {e}")
        return None

def publish_mqtt(client: mqtt.Client | None, llamado: dict) -> None:
    """
    Publishes a formatted call notification to the MQTT broker.
    """
    payload_data = format_notification(llamado)
    
    if config.test_mode:
        logger.info(f"[TEST MODE] MQTT Payload: {json.dumps(payload_data)}")
        return

    if client:
        try:
            payload = json.dumps(payload_data)
            client.publish(config.mqtt_topic, payload, retain=True)
            time.sleep(0.5)
        except (mqtt.MQTTException, TypeError) as e:
            logger.error(f"Error publishing to MQTT: {e}")

def disconnect_mqtt(client: mqtt.Client | None) -> None:
    """
    Gracefully disconnects the MQTT client.
    """
    if client:
        try:
            client.loop_stop()
            client.disconnect()
            logger.info("Disconnected from MQTT broker.")
        except mqtt.MQTTException as e:
            logger.error(f"Error during MQTT disconnect: {e}")