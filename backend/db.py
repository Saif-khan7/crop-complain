# db.py
import sqlite3

DB_NAME = "complaints.db"

def get_db_connection():
    """
    Creates and returns a SQLite connection to 'complaints.db'.
    """
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    conn.row_factory = sqlite3.Row  # So we get rows as dictionaries
    return conn

def init_db():
    """
    Ensures the 'complaints' table is created with these columns:
      id, text, latitude, longitude, embedding, cluster_id, created_at
    """
    conn = get_db_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS complaints (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            latitude REAL,
            longitude REAL,
            embedding TEXT,
            cluster_id INTEGER,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.commit()
    conn.close()
