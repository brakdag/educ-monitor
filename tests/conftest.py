import pytest
import os
import shutil

# Basic setup for tests
@pytest.fixture
def temp_db(tmp_path):
    # Use a temporary file for the database
    db_file = tmp_path / "test_llamados.db"
    return str(db_file)
