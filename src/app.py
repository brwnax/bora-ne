from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from pathlib import Path

app = Flask(__name__)

app.secret_key = "dev"

DB_PATH = (Path(__file__).parent / "database.db").resolve()

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    if not DB_PATH.exists():
        print('[INT_DB] Criando novo banco...')
        with get_db_connection() as conn:
            conn.executescript('''
                CREATE TABLE produtos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    email TEXT NOT NULL
                    )
            ''')
        conn.commit()
    print('[INIT_DB] Banco criado em ', DB_PATH)