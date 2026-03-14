import sqlite3
from config import DB_PATH

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS problem_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title_slug TEXT UNIQUE,
            title TEXT,
            difficulty TEXT,
            sent_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def is_problem_sent(title_slug):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT 1 FROM problem_history WHERE title_slug = ?', (title_slug,))
    result = cursor.fetchone()
    conn.close()
    return result is not None

def record_problem(title_slug, title, difficulty):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO problem_history (title_slug, title, difficulty)
            VALUES (?, ?, ?)
        ''', (title_slug, title, difficulty))
        conn.commit()
    except sqlite3.IntegrityError:
        pass  # Already exists
    conn.close()

if __name__ == "__main__":
    init_db()
    print(f"Database initialized at {DB_PATH}")
