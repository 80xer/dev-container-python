import sqlite3

def get_db_connection():
    conn = sqlite3.connect('quotes.db')
    conn.row_factory = sqlite3.Row
    return conn

def create_table():
    conn = get_db_connection()
    conn.execute('CREATE TABLE IF NOT EXISTS quotes (quote TEXT UNIQUE, author TEXT)')
    conn.commit()
    conn.close()

def save_quote(quote, author):
    conn = get_db_connection()
    try:
        conn.execute('INSERT INTO quotes (quote, author) VALUES (?, ?)', (quote, author))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        # Quote already exists
        return False
    finally:
        conn.close()