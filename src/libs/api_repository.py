import os
from typing import Optional

import aiohttp

from libs.categories import Category

# get_all/remove 用のlimit。APIは limit > 0 が必須で全件取得エンドポイントが
# 無いため、十分大きな値を指定して実質的な全件取得とする。
FETCH_ALL_LIMIT = 100000

# このBotが使用する固定の type。APIは mesugaki/osugaki/onesan を取りうる。
DEFAULT_TYPE = "mesugaki"


class ApiRepository:
    """外部API (dac-bot-integrated) を永続化先とするPhraseRepository実装。

    APIの仕様上の差異を吸収する:
    - ランダム取得: GET /vocabulary?limit=1 （API側が ORDER BY RANDOM()）。
    - 全件取得: 全件取得用エンドポイントが無いため大きなlimitで代替。
    - 追加: APIは重複を許可するため、既存チェックで従来の重複時Falseを再現。
    - 削除: APIはID指定削除のみのため、フレーズ→ID解決の2段階で行う。
    """

    def __init__(self):
        base_url = os.getenv("API_BASE_URL")
        if not base_url:
            raise ValueError("API_BASE_URL is not set (required for PHRASE_BACKEND=api).")
        self._base_url = base_url.rstrip("/")
        self._type = os.getenv("API_TYPE", DEFAULT_TYPE)
        self._token = os.getenv("API_TOKEN")
        self._session: Optional[aiohttp.ClientSession] = None

    @property
    def description(self) -> str:
        return f"API ({self._base_url}, type={self._type})"

    async def setup(self) -> None:
        headers = {}
        if self._token:
            headers["Authorization"] = f"Bearer {self._token}"
        self._session = aiohttp.ClientSession(headers=headers)

    async def close(self) -> None:
        if self._session is not None:
            await self._session.close()
            self._session = None

    @property
    def _vocab_url(self) -> str:
        return f"{self._base_url}/vocabulary"

    async def _fetch(self, category: Category, limit: int) -> list[dict]:
        """指定カテゴリの語彙を取得する。各要素は {'id': int, 'word': str}。"""
        params = {"type": self._type, "category": category.api_name, "limit": limit}
        try:
            async with self._session.get(self._vocab_url, params=params) as resp:
                if resp.status != 200:
                    print(f"API error (GET /vocabulary): status={resp.status}")
                    return []
                return await resp.json()
        except aiohttp.ClientError as e:
            print(f"API request failed (GET /vocabulary): {e}")
            return []

    async def get_random(self, category: Category) -> Optional[str]:
        rows = await self._fetch(category, limit=1)
        if rows:
            return rows[0].get("word")
        return None

    async def get_all(self, category: Category) -> list[str]:
        rows = await self._fetch(category, limit=FETCH_ALL_LIMIT)
        return [row["word"] for row in rows if "word" in row]

    async def add(self, category: Category, phrase: str) -> bool:
        # APIは重複を許可するため、追加前に存在チェックして従来の挙動を再現する。
        if phrase in await self.get_all(category):
            return False
        payload = {"word": phrase, "type": self._type, "category": category.api_name}
        try:
            async with self._session.post(self._vocab_url, json=payload) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return bool(data.get("success"))
                print(f"API error (POST /vocabulary): status={resp.status}")
                return False
        except aiohttp.ClientError as e:
            print(f"API request failed (POST /vocabulary): {e}")
            return False

    async def remove(self, category: Category, phrase: str) -> bool:
        # APIはID指定削除のみのため、一覧からフレーズに一致するIDを解決する。
        rows = await self._fetch(category, limit=FETCH_ALL_LIMIT)
        target_id = next((row["id"] for row in rows if row.get("word") == phrase), None)
        if target_id is None:
            return False
        try:
            async with self._session.delete(f"{self._vocab_url}/{target_id}") as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return bool(data.get("success"))
                print(f"API error (DELETE /vocabulary/{target_id}): status={resp.status}")
                return False
        except aiohttp.ClientError as e:
            print(f"API request failed (DELETE /vocabulary): {e}")
            return False
