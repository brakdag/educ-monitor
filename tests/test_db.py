import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import sqlite3
import pytest
import db

def test_db_operations(tmp_path, monkeypatch):
    db_file = tmp_path / "llamados.db"
    
    # Store original
    original_connect = sqlite3.connect
    
    # Mocking
    def mock_connect(path):
        return original_connect(str(db_file))
    
    monkeypatch.setattr(db.sqlite3, 'connect', mock_connect)
    
    db.init_db()
    
    unique_id = "test_123"
    assert db.is_new_llamado(unique_id) == True
    
    db.add_llamado(unique_id, "content", "2026-03-25", "1er", "2026-03-26")
    
    assert db.is_new_llamado(unique_id) == False
