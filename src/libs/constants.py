import datetime
import os

# タイムゾーン設定
JST = datetime.timezone(datetime.timedelta(hours=9))

# ディレクトリ設定
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
DATA_DIR = os.path.join(BASE_DIR, 'data')
