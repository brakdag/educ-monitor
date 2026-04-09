import sqlite3
import logging
from .config import config

logger = logging.getLogger("educ_monitor.database")

def init_db() -> None:
    """
    Initializes the database schema if it doesn't exist.
    
    Raises:
        sqlite3.Error: If the table creation fails.
    """
    try:
        with sqlite3.connect(config.db_path) as conn:
            c = conn.cursor()
            c.execute('''CREATE TABLE IF NOT EXISTS llamados
                     (id TEXT PRIMARY KEY, contenido TEXT, fecha_publicacion TEXT, tipo_llamado TEXT, fecha_llamado DATE)''')
            conn.commit()
    except sqlite3.Error as e:
        logger.error(f"Database initialization failed: {e}", exc_info=True)
        raise

def is_new_llamado(unique_id: str) -> bool:
    """
    Checks if a specific call ID already exists in the database.
    
    Args:
        unique_id (str): The unique identifier of the call.
        
    Returns:
        bool: True if the call is not in the database, False otherwise.
    """
    try:
        with sqlite3.connect(config.db_path) as conn:
            c = conn.cursor()
            c.execute('SELECT 1 FROM llamados WHERE id = ?', (unique_id,))
            return c.fetchone() is None
    except sqlite3.Error as e:
        logger.error(f"Error checking for existing call {unique_id}: {e}")
        return True  # Assume it's new to avoid missing notifications

def add_llamado(unique_id: str, content: str, pub_date: str, call_type: str, call_date: str) -> bool:
    """
    Inserts a new call record into the database.
    
    Args:
        unique_id (str): Unique identifier of the call.
        content (str): Raw data or description of the call.
        pub_date (str): Date when the call was detected/published.
        call_type (str): Type of the call.
        call_date (str): The actual date of the call.
        
    Returns:
        bool: True if a new record was inserted, False if it already existed.
    """
    try:
        with sqlite3.connect(config.db_path) as conn:
            c = conn.cursor()
            c.execute('''INSERT OR IGNORE INTO llamados 
                     (id, contenido, fecha_publicacion, tipo_llamado, fecha_llamado) 
                     VALUES (?, ?, ?, ?, ?)''',
                  (unique_id, content, pub_date, call_type, call_date))
            inserted = c.rowcount > 0
            conn.commit()
            return inserted
    except sqlite3.Error as e:
        logger.error(f"Error adding call {unique_id} to database: {e}")
        return False