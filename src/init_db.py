import sqlite3

conn = sqlite3.connect('database.db')

c = conn.cursor()

c.execute('''
CREATE TABLE produtos(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL,
)
''')

conn.commit()

conn.close()