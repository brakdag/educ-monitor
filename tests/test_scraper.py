import pytest
from unittest.mock import patch, MagicMock
from requests.exceptions import HTTPError, Timeout
from src.educ_monitor.scraper import get_llamados

@patch('requests.Session.get')
def test_get_llamados_success(mock_get):
    """Tests that get_llamados correctly parses a successful API response."""
    # Mock response object
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "datos": [
            {
                "id": 123,
                "lugar_trabajo": "4117 - Escuela A",
                "tipo_llamado": "1er Llamado",
                "fecha_llamado_1": "15/04/24 10:00",
                "materia": "Matemática",
                "articulo": "Cargo"
            }
        ]
    }
    mock_response.raise_for_status = MagicMock()
    mock_get.return_value = mock_response

    result = get_llamados()
    
    assert len(result) == 1
    assert result[0]['unique_id'] == "123"
    assert result[0]['escuela_id'] == "4117"
    assert result[0]['fecha_llamado'] == "2024-04-15"

@patch('requests.Session.get')
def test_get_llamados_http_error(mock_get):
    """Tests that get_llamados handles HTTP errors gracefully."""
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = HTTPError("404 Not Found")
    mock_get.return_value = mock_response

    result = get_llamados()
    assert result == []

@patch('requests.Session.get')
def test_get_llamados_malformed_json(mock_get):
    """Tests that get_llamados handles invalid JSON responses."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.side_effect = ValueError("No JSON object could be decoded")
    mock_get.return_value = mock_response

    result = get_llamados()
    assert result == []

@patch('requests.Session.get')
def test_get_llamados_timeout(mock_get):
    """Tests that get_llamados handles request timeouts."""
    mock_get.side_effect = Timeout("Request timed out")

    result = get_llamados()
    assert result == []