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
        try:
            return int(os.getenv("MQTT_PORT", 1883))
        except ValueError:
            return 1883

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

    @property
    def USER_AGENT(self):
        return os.getenv("USER_AGENT", "Mozilla/5.0 (iPhone; CPU iPhone OS 18_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.5 Mobile/15E148 Safari/604.1")

    @property
    def DEFAULT_HEADERS(self):
        return {
            "Host": "educacionales.mendoza.edu.ar",
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Language": "es-US,es;q=0.9,en-US;q=0.8,en;q=0.7,es-419;q=0.6",
            "Referer": "https://educacionales.mendoza.edu.ar/",
            "X-Requested-With": "XMLHttpRequest",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "Priority": "u=1, i"
        }

    def validate(self):
        """Validates critical configuration settings."""
        errors = []
        
        if not self.DB_PATH:
            errors.append("DB_PATH is not defined")
        
        if not self.MQTT_BROKER:
            errors.append("MQTT_BROKER is not defined")
            
        if not self.MQTT_TOPIC:
            errors.append("MQTT_TOPIC is not defined")
            
        if errors:
            raise ValueError(f"Configuration Error: {'; '.join(errors)}")
        
        return True

    def update_setting(self, key, value):
        """Update a setting in the .env file."""
        set_key(ENV_FILE, key, str(value))
        # Force reload of the environment
        load_dotenv(ENV_FILE, override=True)

config = Config()