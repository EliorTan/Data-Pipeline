"""
Database operations for the API Data Pipeline.
"""
import logging
import sqlite3
from pathlib import Path
from typing import List, Dict

logger = logging.getLogger(__name__)

def save_to_database(data: List[Dict], db_name: str = 'pipeline_data.db') -> str:
    current_dir = Path(__file__).parent.parent
    data_dir = current_dir / 'data'
    data_dir.mkdir(exist_ok=True)
    db_path = data_dir / db_name
    
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        name TEXT,
        email TEXT,
        company TEXT
    )
    ''')
    
    for user in data:
        cursor.execute('''
        INSERT OR REPLACE INTO users (id, name, email, company)
        VALUES (?, ?, ?, ?)
        ''', (user['id'], user['name'], user['email'], user['company']))
    
    conn.commit()
    conn.close()
    logger.info(f"Data saved to database: {db_path}")

    return str(db_path)