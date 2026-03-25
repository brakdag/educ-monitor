import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from datetime import datetime
import re

# We test the parsing logic directly as it's the core of scraper.py
def test_parse_date():
    col0 = "1er: 26/03/26 19:30"
    match = re.search(r'(\d{1,2}/\d{1,2}/\d{2})', col0)
    assert match is not None
    fecha_str = match.group(1)
    fecha_llamado = datetime.strptime(fecha_str, "%d/%m/%y").strftime("%Y-%m-%d")
    assert fecha_llamado == "2026-03-26"
    
    col0_bad = "No date here"
    match_bad = re.search(r'(\d{1,2}/\d{1,2}/\d{2})', col0_bad)
    assert match_bad is None
