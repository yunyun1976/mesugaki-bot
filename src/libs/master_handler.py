import sqlite3
import os

DB_DIR = 'data'
DB_NAME = 'masters.db'
DB_PATH = os.path.join(DB_DIR, DB_NAME)

def init_masters_db():
    """Initializes the masters database and creates the table if it doesn't exist."""
    os.makedirs(DB_DIR, exist_ok=True)
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS masters (user_id INTEGER PRIMARY KEY)")
        conn.commit()

def add_master(user_id: int) -> bool:
    """Adds a master user to the database."""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute("INSERT INTO masters (user_id) VALUES (?)", (user_id,))
            conn.commit()
            return True
    except sqlite3.IntegrityError:
        # User already exists
        return False
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return False

def get_all_masters() -> list[int]:
    """Gets all master user IDs from the database."""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute("SELECT user_id FROM masters")
            return [row[0] for row in c.fetchall()]
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return []

def remove_master(user_id: int) -> bool:
    """Removes a master user from the database."""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute("DELETE FROM masters WHERE user_id = ?", (user_id,))
            conn.commit()
            return c.rowcount > 0
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return False

def is_master(user_id: int) -> bool:
    """Checks if a user is a master."""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute("SELECT 1 FROM masters WHERE user_id = ?", (user_id,))
            return c.fetchone() is not None
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return False
