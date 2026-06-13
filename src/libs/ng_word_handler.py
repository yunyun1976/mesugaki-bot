import sqlite3
import os
import re
import unicodedata
from typing import Optional
from libs.constants import DATA_DIR

DB_NAME = 'ng_words.db'
DB_PATH = os.path.join(DATA_DIR, DB_NAME)

# 飾り文字・空白・記号を除去するための正規表現（単語構成文字以外をまとめて除去）。
_STRIP_PATTERN = re.compile(r'[\s\W_]+', re.UNICODE)


def normalize(text: str) -> str:
    """NG判定用にテキストを正規化する。

    NFKC正規化・小文字化を行い、空白や `♡` 等の飾り文字・記号を除去する。
    これにより「ば　か」「ば♡か」のような単純な回避を吸収する。
    """
    text = unicodedata.normalize('NFKC', text)
    text = text.lower()
    return _STRIP_PATTERN.sub('', text)


def init_ng_words_db():
    """NGワードDBを初期化し、テーブルが無ければ作成する。"""
    os.makedirs(DATA_DIR, exist_ok=True)
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS ng_words (word TEXT UNIQUE)")
        conn.commit()


def add_ng_word(word: str) -> bool:
    """NGワードを追加する。成功時True、重複時はFalse。"""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute("INSERT INTO ng_words (word) VALUES (?)", (word,))
            conn.commit()
            return True
    except sqlite3.IntegrityError:
        # Word already exists
        return False
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return False


def remove_ng_word(word: str) -> bool:
    """NGワードを削除する。削除できた場合True。"""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute("DELETE FROM ng_words WHERE word = ?", (word,))
            conn.commit()
            return c.rowcount > 0
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return False


def get_all_ng_words() -> list[str]:
    """登録されている全NGワードを取得する。"""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute("SELECT word FROM ng_words")
            return [row[0] for row in c.fetchall()]
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return []


def find_ng_match(phrase: str) -> Optional[str]:
    """フレーズがNGワードを含むか判定する。

    正規化した上での部分一致で判定し、最初に一致したNGワード（元の表記）を返す。
    一致しない場合はNoneを返す。軽量な文字列比較のみで実装している。
    """
    normalized_phrase = normalize(phrase)
    if not normalized_phrase:
        return None
    for ng_word in get_all_ng_words():
        normalized_ng = normalize(ng_word)
        # 正規化後に空になるNGワード（記号のみ等）は誤爆防止のためスキップ。
        if normalized_ng and normalized_ng in normalized_phrase:
            return ng_word
    return None
