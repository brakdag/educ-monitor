import pytest
from unittest.mock import MagicMock, patch
from src.educ_monitor.notifier import format_notification, connect_mqtt, publish_mqtt

def test_format_notification_json_structure():
    """Tests that the notification payload is correctly filtered."""
    raw_data = {
        "lugar_trabajo": "1234 - Escuela Test",
        "materia": "Matemática",
        "articulo": "Cargo",
        "fecha_llamado_1": "05/04/26 10:00",
        "fecha_llamado_2": None,
        "fecha_llamado_3": "06/04/26 10:00",
        "extra_field": "ignore_me"
    }
    
    result = format_notification(raw_data)
    
    assert result["escuela"] == "1234"
    assert result["materia"] == "Matemática"
    assert "fecha_llamado_1" in result
    assert "fecha_llamado_2" not in result
    assert "extra_field" not in result

@patch('paho.mqtt.client.Client')
def test_connect_mqtt_success(mock_client_class):
    """Tests successful MQTT connection."""
    mock_client = mock_client_class.return_value
    
    # Ensure we are not in test mode for this test
    with patch('src.educ_monitor.config.config.test_mode', False):
        client = connect_mqtt()
        assert client is not None
        mock_client.connect.assert_called_once()
        mock_client.loop_start.assert_called_once()

@patch('src.educ_monitor.config.config.test_mode', True)
def test_connect_mqtt_test_mode():
    """Tests that MQTT connection is skipped in test mode."""
    client = connect_mqtt()
    assert client is None

@patch('src.educ_monitor.config.config.test_mode', False)
def test_publish_mqtt_success():
    """Tests that publish_mqtt calls the client publish method."""
    mock_client = MagicMock()
    llamado = {"lugar_trabajo": "123 - Esc", "materia": "Math"}
    
    publish_mqtt(mock_client, llamado)
    
    assert mock_client.publish.called
    # Verify that the payload is a JSON string
    args, kwargs = mock_client.publish.call_args
    assert isinstance(args[1], str)
    assert "123" in args[1]