import sqlite3

def init_db():
    conn = sqlite3.connect('llamados.db')
    c = conn.cursor()
    # Dropping old table to refresh schema for prototype
    c.execute('DROP TABLE IF EXISTS llamados')
    c.execute('''CREATE TABLE llamados
                 (id TEXT PRIMARY KEY, contenido TEXT, fecha_publicacion TEXT, tipo_llamado TEXT, fecha_llamado DATE)''')
    conn.commit()
    conn.close()

def is_new_llamado(unique_id):
    conn = sqlite3.connect('llamados.db')
    c = conn.cursor()
    c.execute('SELECT 1 FROM llamados WHERE id = ?', (unique_id,))
    exists = c.fetchone() is not None
    conn.close()
    return not exists

def add_llamado(unique_id, contenido, fecha_publicacion, tipo_llamado, fecha_llamado):
    conn = sqlite3.connect('llamados.db')
    c = conn.cursor()
    c.execute('INSERT OR IGNORE INTO llamados (id, contenido, fecha_publicacion, tipo_llamado, fecha_llamado) VALUES (?, ?, ?, ?, ?)',
              (unique_id, contenido, fecha_publicacion, tipo_llamado, fecha_llamado))
    inserted = c.rowcount > 0
    conn.commit()
    conn.close()
    return inserted
