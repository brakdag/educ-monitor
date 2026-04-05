import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from educ_monitor import config
from educ_monitor.config import Config
import pytest

def test_config_defaults():
    # We can create a fresh Config instance
    c = Config()
    # Check against environment
    import os
    assert c.MQTT_BROKER == os.getenv("MQTT_BROKER", "localhost")
    assert c.MQTT_PORT == int(os.getenv("MQTT_PORT", 1883))

def test_update_config(tmp_path, monkeypatch):
    # Set up a fake .env file
    env_file = tmp_path / ".env"
    env_file.write_text("MQTT_BROKER=192.168.1.1\n")
    
    # We need to change the global setting in the module
    monkeypatch.setattr(config, 'ENV_FILE', str(env_file))
    
    # Reload environment variables for this instance
    from dotenv import load_dotenv
    load_dotenv(str(env_file), override=True)
    
    c = Config()
    assert c.MQTT_BROKER == "192.168.1.1"
    
    c.update_setting("MQTT_BROKER", "10.0.0.1")
    assert c.MQTT_BROKER == "10.0.0.1"
