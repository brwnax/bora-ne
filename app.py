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
                CREATE TABLE inscritos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    email TEXT NOT NULL UNIQUE
                    )
            ''')
        conn.commit()
        print('[INIT_DB] Banco criado em ', DB_PATH)
    else:
        print('[INIT_DB] Banco já existe em ', DB_PATH)

@app.route("/sobre")
def sobre():
    return render_template("sobre.html")

@app.route('/', endpoint='home')
def home():
    with get_db_connection() as conn:
        inscritos = conn.execute("SELECT id, email FROM inscritos ORDER BY id").fetchall()
    return render_template('index.html', inscritos=inscritos)

@app.route('/subscribe', methods=['POST'])
def subscribe():
    email = request.form.get('email')

    if not email:
        flash("Você precisa inserir um email válido!", "error")
        return redirect(url_for('home'))
    try:
        with get_db_connection() as conn:
            conn.execute('INSERT INTO inscritos (email) VALUES (?)', (email,))
            conn.commit()
        flash("Obrigado(a) por se inscrever!", "success")
    except sqlite3.IntegrityError:
        flash("Esse email já está inscrito!", "info")
    
    return redirect(url_for('home'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
    