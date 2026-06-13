import os
from typing import Optional, Protocol, runtime_checkable

from libs import db_handler
from libs.categories import Category


@runtime_checkable
class PhraseRepository(Protocol):
    """フレーズの永続化層を抽象化するインターフェース。

    SQLite実装と外部API実装を差し替え可能にするため、メソッドは全て
    非同期として定義する。
    """

    @property
    def description(self) -> str:
        """起動ログ用の、このバックエンドを表す人間可読な文字列。"""
        ...

    async def setup(self) -> None:
        """リポジトリの初期化（テーブル作成・接続準備等）を行う。"""
        ...

    async def close(self) -> None:
        """リポジトリの後始末（接続のクローズ等）を行う。"""
        ...

    async def get_random(self, category: Category) -> Optional[str]:
        """指定カテゴリからランダムに1件のフレーズを取得する。"""
        ...

    async def add(self, category: Category, phrase: str) -> bool:
        """フレーズを追加する。成功時True、重複時等はFalse。"""
        ...

    async def remove(self, category: Category, phrase: str) -> bool:
        """フレーズを削除する。削除できた場合True。"""
        ...

    async def get_all(self, category: Category) -> list[str]:
        """指定カテゴリの全フレーズを取得する。"""
        ...


class SqliteRepository:
    """SQLiteを永続化先とするPhraseRepository実装。

    既存の ``db_handler`` をラップするだけで、挙動は従来と同一。
    """

    @property
    def description(self) -> str:
        return "SQLite (local)"

    async def setup(self) -> None:
        for category in Category:
            db_handler.init_db(category.db_name)

    async def close(self) -> None:
        # SQLiteは都度接続・クローズしているため後始末は不要。
        return None

    async def get_random(self, category: Category) -> Optional[str]:
        return db_handler.get_random_phrase(category.db_name)

    async def add(self, category: Category, phrase: str) -> bool:
        return db_handler.add_phrase(category.db_name, phrase)

    async def remove(self, category: Category, phrase: str) -> bool:
        return db_handler.remove_phrase(category.db_name, phrase)

    async def get_all(self, category: Category) -> list[str]:
        return db_handler.get_all_phrases(category.db_name)


def get_repository() -> PhraseRepository:
    """環境変数 ``PHRASE_BACKEND`` に応じたリポジトリ実装を返す。

    ``sqlite``（既定）でSQLite、``api`` で外部APIを使用する。
    """
    backend = os.getenv("PHRASE_BACKEND", "sqlite").lower()
    if backend == "api":
        # 遅延importで、SQLite利用時にaiohttp等の依存を読み込まないようにする。
        from libs.api_repository import ApiRepository

        return ApiRepository()
    return SqliteRepository()
