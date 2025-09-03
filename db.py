import sqlite3
import numpy as np
import os

DB_PATH = "faces.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            embedding BLOB
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS served (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            session TEXT,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)
    conn.commit()
    conn.close()

def add_user(name, embedding):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("INSERT OR REPLACE INTO users (name, embedding) VALUES (?, ?)",
                (name, embedding.tobytes()))
    conn.commit()
    conn.close()

def get_all_users():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT id, name, embedding FROM users")
    rows = cur.fetchall()
    users = [(r[0], r[1], np.frombuffer(r[2], dtype=np.float64)) for r in rows]
    conn.close()
    return users

def mark_served(user_id, session):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("INSERT INTO served (user_id, session) VALUES (?, ?)", (user_id, session))
    conn.commit()
    conn.close()

def has_been_served(user_id, session):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM served WHERE user_id=? AND session=?", (user_id, session))
    result = cur.fetchone()
    conn.close()
    return result is not None
