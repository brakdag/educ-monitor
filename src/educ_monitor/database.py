import sqlite3
from .config import config

def init_db():
    """Initializes the database schema if it doesn't exist."""
    conn = sqlite3.connect(config.DB_PATH)
    c = conn.cursor()
    # Create table only if it doesn't exist to prevent data loss
    c.execute('''CREATE TABLE IF NOT EXISTS llamados
                 (id TEXT PRIMARY KEY, contenido TEXT, fecha_publicacion TEXT, tipo_llamado TEXT, fecha_llamado DATE)''')
    conn.commit()
    conn.close()

def is_new_llamado(unique_id):
    conn = sqlite3.connect(config.DB_PATH)
    c = conn.cursor()
    c.execute('SELECT 1 FROM llamados WHERE id = ?', (unique_id,))
    exists = c.fetchone() is not None
    conn.close()
    return not exists

def add_llamado(unique_id, contenido, fecha_publicacion, tipo_llamado, fecha_llamado):
    conn = sqlite3.connect(config.DB_PATH)
    c = conn.cursor()
    c.execute('INSERT OR IGNORE INTO llamados (id, contenido, fecha_publicacion, tipo_llamado, fecha_llamado) VALUES (?, ?, ?, ?, ?)',
              (unique_id, contenido, fecha_publicacion, tipo_llamado, fecha_llamado))
    inserted = c.rowcount > 0
    conn.commit()
    conn.close()
    return inserted
