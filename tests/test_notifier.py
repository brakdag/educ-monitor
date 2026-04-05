import pytest
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

# Add src to path
sys.path.append(str(Path("src")))

from educ_monitor.notifier import format_notification

def test_format_notification_json_structure():
    # Mock input data
    raw_data = {
        "lugar_trabajo": "1234 - Escuela Test",
        "materia": "Matemática",
        "articulo": "Cargo",
        "fecha_llamado_1": "05/04/26 10:00",
        "fecha_llamado_2": None,
        "fecha_llamado_3": "06/04/26 10:00",
        "extra_field": "ignore_me"
    }
    
    # Run function
    result = format_notification(raw_data)
    
    # Assert structure
    assert result["escuela"] == "1234"
    assert result["materia"] == "Matemática"
    assert result["articulo"] == "Cargo"
    assert "fecha_llamado_1" in result
    assert result["fecha_llamado_1"] == "05/04/26 10:00"
    assert "fecha_llamado_2" not in result # Should not be in result if None
    assert "fecha_llamado_3" in result
    assert "extra_field" not in result # Should ignore fields not in filtering logic
