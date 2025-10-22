import sqlite3
import os

DB_DIR = 'data'

def init_db(db_name: str):
    """Initializes the database and creates the phrases table if it doesn't exist."""
    os.makedirs(DB_DIR, exist_ok=True)
    with sqlite3.connect(os.path.join(DB_DIR, db_name)) as conn:
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS phrases (phrase TEXT UNIQUE)")
        conn.commit()

def get_db_connection(db_name: str):
    """Gets a connection to the specified database."""
    return sqlite3.connect(os.path.join(DB_DIR, db_name))

def get_random_phrase(db_name: str) -> str | None:
    """Gets a random phrase from the specified database."""
    try:
        with get_db_connection(db_name) as conn:
            c = conn.cursor()
            c.execute("SELECT phrase FROM phrases ORDER BY RANDOM() LIMIT 1")
            result = c.fetchone()
            return result[0] if result else None
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return None

def add_phrase(db_name: str, phrase: str) -> bool:
    """Adds a new phrase to the specified database."""
    try:
        with get_db_connection(db_name) as conn:
            c = conn.cursor()
            c.execute("INSERT INTO phrases (phrase) VALUES (?)", (phrase,))
            conn.commit()
            return True
    except sqlite3.IntegrityError:
        # Phrase already exists
        return False
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return False


def get_all_phrases(db_name: str) -> list[str]:
    """Gets all phrases from the specified database."""
    try:
        with get_db_connection(db_name) as conn:
            c = conn.cursor()
            c.execute("SELECT phrase FROM phrases")
            return [row[0] for row in c.fetchall()]
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return []

def remove_phrase(db_name: str, phrase: str) -> bool:
    """Removes a phrase from the specified database."""
    try:
        with get_db_connection(db_name) as conn:
            c = conn.cursor()
            c.execute("DELETE FROM phrases WHERE phrase = ?", (phrase,))
            conn.commit()
            return c.rowcount > 0
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return False
