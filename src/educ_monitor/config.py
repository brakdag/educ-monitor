import os
from dotenv import load_dotenv, set_key

# Load environment variables
ENV_FILE = ".env"
load_dotenv(ENV_FILE)

class Config:
    @property
    def DB_PATH(self):
        return os.getenv("DB_PATH", "data/llamados.db")

    @property
    def MQTT_BROKER(self):
        return os.getenv("MQTT_BROKER", "localhost")

    @property
    def MQTT_PORT(self):
        return int(os.getenv("MQTT_PORT", 1883))

    @property
    def MQTT_TOPIC(self):
        return os.getenv("MQTT_TOPIC", "educacionales/llamados")

    @property
    def SCHOOL_FILTER(self):
        val = os.getenv("SCHOOL_FILTER")
        if not val:
            return None
        return [s.strip() for s in val.split(",")]

    @property
    def TEST_MODE(self):
        return os.getenv("TEST_MODE", "false").lower() == "true"

    def update_setting(self, key, value):
        """Update a setting in the .env file."""
        set_key(ENV_FILE, key, str(value))
        # Force reload of the environment
        load_dotenv(ENV_FILE, override=True)

config = Config()
