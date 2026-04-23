import yaml
import os
from libs.constants import DATA_DIR

MESSAGES_FILE = os.path.join(DATA_DIR, 'messages.yaml')

class MessageHandler:
    _messages = {}

    @classmethod
    def load_messages(cls):
        """YAMLファイルからメッセージを読み込みます。"""
        if os.path.exists(MESSAGES_FILE):
            with open(MESSAGES_FILE, 'r', encoding='utf-8') as f:
                cls._messages = yaml.safe_load(f)
        else:
            print(f"Warning: {MESSAGES_FILE} not found.")

    @classmethod
    def get(cls, key_path: str, default: str = None, **kwargs) -> str:
        """
        指定されたキーパス（例: 'admin.remove_success'）に対応するメッセージを取得し、
        引数があればフォーマットして返します。
        """
        keys = key_path.split('.')
        value = cls._messages
        try:
            for key in keys:
                value = value[key]
            
            if isinstance(value, str):
                return value.format(**kwargs)
            return value
        except (KeyError, TypeError):
            return default if default is not None else key_path

# 初期読み込み
MessageHandler.load_messages()
