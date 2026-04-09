import os
from dotenv import load_dotenv, set_key

# Load environment variables
ENV_FILE = ".env"
load_dotenv(ENV_FILE)

class Config:
    """
    Handles application configuration by loading environment variables from a .env file.
    
    Provides properties for database paths, MQTT settings, and scraper identity.
    """

    @property
    def db_path(self) -> str:
        """Path to the SQLite database file."""
        return os.getenv("DB_PATH", "data/llamados.db")

    @property
    def mqtt_broker(self) -> str:
        """IP or hostname of the MQTT broker."""
        return os.getenv("MQTT_BROKER", "localhost")

    @property
    def mqtt_port(self) -> int:
        """Port of the MQTT broker."""
        try:
            return int(os.getenv("MQTT_PORT", 1883))
        except ValueError:
            return 1883

    @property
    def mqtt_topic(self) -> str:
        """MQTT topic for publishing notifications."""
        return os.getenv("MQTT_TOPIC", "educacionales/llamados")

    @property
    def school_filter(self) -> list[str] | None:
        """List of school IDs to filter notifications. Returns None if no filter is set."""
        val = os.getenv("SCHOOL_FILTER")
        if not val:
            return None
        return [s.strip() for s in val.split(",")]

    @property
    def test_mode(self) -> bool:
        """Whether the application is running in test mode (disables real MQTT publishing)."""
        return os.getenv("TEST_MODE", "false").lower() == "true"

    @property
    def user_agent(self) -> str:
        """User-Agent string used by the scraper to mimic a mobile device."""
        return os.getenv("USER_AGENT", "Mozilla/5.0 (iPhone; CPU iPhone OS 18_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.5 Mobile/15E148 Safari/604.1")

    @property
    def default_headers(self) -> dict[str, str]:
        """Standard HTTP headers required by the DGE Mendoza API."""
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

    def validate(self) -> bool:
        """
        Validates that critical configuration settings are present.
        
        Raises:
            ValueError: If any critical setting is missing.
            
        Returns:
            bool: True if configuration is valid.
        """
        errors = []
        if not self.db_path: errors.append("DB_PATH is not defined")
        if not self.mqtt_broker: errors.append("MQTT_BROKER is not defined")
        if not self.mqtt_topic: errors.append("MQTT_TOPIC is not defined")
            
        if errors:
            raise ValueError(f"Configuration Error: {'; '.join(errors)}")
        return True

    def update_setting(self, key: str, value: any) -> None:
        """
        Updates a setting in the .env file and reloads the environment.
        
        Args:
            key (str): The environment variable name.
            value (any): The value to set.
        """
        set_key(ENV_FILE, key, str(value))
        load_dotenv(ENV_FILE, override=True)

config = Config()