import sqlite3
import os
from libs.constants import DATA_DIR

DB_NAME = 'config.db'
DB_PATH = os.path.join(DATA_DIR, DB_NAME)

def init_config_db():
    """Initializes the config database and creates the channels table."""
    os.makedirs(DATA_DIR, exist_ok=True)
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS announcement_channels (guild_id INTEGER PRIMARY KEY, channel_id INTEGER)")
        conn.commit()

def set_announcement_channel(guild_id: int, channel_id: int):
    """Sets or updates the announcement channel for a guild."""
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("INSERT OR REPLACE INTO announcement_channels (guild_id, channel_id) VALUES (?, ?)", (guild_id, channel_id))
        conn.commit()

def get_announcement_channel(guild_id: int) -> int:
    """Gets the announcement channel ID for a guild."""
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("SELECT channel_id FROM announcement_channels WHERE guild_id = ?", (guild_id,))
        result = c.fetchone()
        return result[0] if result else None

def unset_announcement_channel(guild_id: int):
    """Removes the announcement channel setting for a guild."""
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("DELETE FROM announcement_channels WHERE guild_id = ?", (guild_id,))
        conn.commit()

def get_all_announcement_channels() -> list[tuple[int, int]]:
    """Gets all registered announcement channels (guild_id, channel_id)."""
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("SELECT guild_id, channel_id FROM announcement_channels")
        return c.fetchall()
