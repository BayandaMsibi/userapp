import sqlite3
import os
from flask import g

DB_PATH = 'users.db'

def get_db():
    """Return a sqlite3 connection (attached to flask.g) with dict-like rows."""
    db = getattr(g, '_database', None)
    if db is None:
        db = sqlite3.connect(DB_PATH)
        db.row_factory = sqlite3.Row
        g._database = db
    return db

def close_connection(exception):
    """Close DB connection at the end of the request."""
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    """Create users table if it doesn't exist."""
    if not os.path.exists(DB_PATH):
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('''
            CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                full_name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                age INTEGER,
                bio TEXT
            )
        ''')
        conn.commit()
        conn.close()
        print('Initialized database at', DB_PATH)

def add_sample_data():
    """Insert sample data if no users exist."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    try:
        c.execute('SELECT COUNT(*) FROM users')
        count = c.fetchone()[0]
    except sqlite3.Error:
        count = 0
        
    if count == 0:
        c.execute('INSERT INTO users (username, full_name, email, age, bio) VALUES (?, ?, ?, ?, ?)',
                  ('jdoe', 'John Doe', 'jdoe@example.com', 34, 'A short bio about John.'))
        c.execute('INSERT INTO users (username, full_name, email, age, bio) VALUES (?, ?, ?, ?, ?)',
                  ('asmith', 'Alice Smith', 'alice@example.com', 28, 'Alice loves coding and coffee.'))
        conn.commit()
        print('Inserted sample users.')
    conn.close()