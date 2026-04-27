import sqlite3
import os

DB_PATH = os.path.join('instance', 'database.db')

def get_db_connection():
    # 確保 instance 資料夾存在
    os.makedirs('instance', exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    with open('database/schema.sql', 'r', encoding='utf-8') as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()
