from enum import Enum


class Category(Enum):
    """フレーズのカテゴリ。

    各カテゴリにSQLiteのDBファイル名、API上のカテゴリ名、返信時に付与する
    接尾辞、一覧表示時のタイトルを紐づけて一元管理する。
    """

    BATOU = ("barizougon.db", "batou", "♡", "罵詈雑言一覧")
    WAKARASE = ("abikyoukan.db", "wakarase", "ぉぉぉお♡♡♡", "阿鼻叫喚一覧")

    def __init__(self, db_name: str, api_name: str, suffix: str, list_title: str):
        self.db_name = db_name
        self.api_name = api_name
        self.suffix = suffix
        self.list_title = list_title
