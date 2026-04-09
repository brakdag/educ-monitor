import pytest
from src.educ_monitor.utils import parse_date

@pytest.mark.parametrize("input_date, expected", [
    ("15/04/24", "2024-04-15"),            # Formato estándar YY
    ("15/04/2024", "2024-04-15"),         # Formato estándar YYYY
    ("15-04-24", "2024-04-15"),            # Formato con guion YY
    ("15-04-2024", "2024-04-15"),         # Formato con guion YYYY
    ("2024-04-15", "2024-04-15"),         # Formato ISO
    ("15/04/24 10:30", "2024-04-15"),     # Fecha con hora
    ("  15/04/24  ", "2024-04-15"),       # Fecha con espacios
    (None, None),                            # Valor nulo
    ("", None),                             # String vacío
    ("invalid-date", None),                 # Formato inválido
    ("32/01/24", None),                     # Fecha inexistente
])
def test_parse_date_variants(input_date, expected):
    """Tests that parse_date handles various formats and edge cases correctly."""
    assert parse_date(input_date) == expected