import sys
from pathlib import Path
from unittest.mock import MagicMock, patch
import os

# Set environment variable to force TEST_MODE
os.environ["TEST_MODE"] = "true"

from educ_monitor.notifier import notify_home_assistant

def test_mqtt_output():
    # Setup test data
    llamado = {
        "lugar_trabajo": "1234 - Escuela de Prueba",
        "materia": "Informática",
        "articulo": "Cargo",
        "fecha_llamado_1": "06/04/26 08:00"
    }

    print("--- Testing MQTT Notification (TEST_MODE via ENV) ---")
    notify_home_assistant(llamado)

if __name__ == "__main__":
    test_mqtt_output()

if __name__ == "__main__":
    test_mqtt_output()
