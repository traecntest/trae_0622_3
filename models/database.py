import sqlite3
import os
from config import DB_PATH


class Database:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.conn = None
            cls._instance._init_db()
        return cls._instance

    def _init_db(self):
        self.conn = sqlite3.connect(DB_PATH)
        self.conn.row_factory = sqlite3.Row
        self._create_tables()

    def _create_tables(self):
        cursor = self.conn.cursor()
        cursor.executescript("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                nickname TEXT,
                age INTEGER,
                is_elderly_mode INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS exercise_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                script_id TEXT NOT NULL,
                script_name TEXT NOT NULL,
                final_risk_score INTEGER DEFAULT 0,
                final_risk_level TEXT,
                total_duration INTEGER DEFAULT 0,
                choices_made TEXT,
                result_summary TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            );

            CREATE TABLE IF NOT EXISTS choice_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                record_id INTEGER NOT NULL,
                node_id TEXT NOT NULL,
                option_id TEXT NOT NULL,
                risk_delta INTEGER DEFAULT 0,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (record_id) REFERENCES exercise_records(id)
            );
        """)
        self.conn.commit()

    def get_connection(self):
        return self.conn

    def close(self):
        if self.conn:
            self.conn.close()
            self._instance = None
