import sqlite3
import json
import os

DB_PATH = "history.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS runs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            api TEXT,
            passed INTEGER,
            failed INTEGER,
            latency_avg REAL,
            latency_p95 REAL,
            availability REAL,
            full_data TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_run(run_data):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        INSERT INTO runs (timestamp, api, passed, failed, latency_avg, latency_p95, availability, full_data)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        run_data["timestamp"],
        run_data["api"],
        run_data["summary"]["passed"],
        run_data["summary"]["failed"],
        run_data["summary"]["latency_ms_avg"],
        run_data["summary"]["latency_ms_p95"],
        run_data["summary"]["availability"],
        json.dumps(run_data)
    ))
    conn.commit()
    conn.close()

def list_runs(limit=20):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute('SELECT * FROM runs ORDER BY timestamp DESC LIMIT ?', (limit,))
    rows = c.fetchall()
    conn.close()
    return rows

def get_last_run():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute('SELECT * FROM runs ORDER BY timestamp DESC LIMIT 1')
    row = c.fetchone()
    conn.close()
    return row

# Initialize DB on import
if not os.path.exists(DB_PATH):
    init_db()
