<div align="center">

<img src="image/icon.png" width="200" height="200" style="border-radius: 50%;" alt="mesugaki-bot-icon">

😭😭😭😭😭😭😭😭

# Mesugaki Bot♡

[![GitHub version](https://img.shields.io/github/v/release/yunyun1976/mesugaki-bot?include_prereleases&style=for-the-badge&color=ff69b4)](https://github.com/yunyun1976/mesugaki-bot/releases)
[![License](https://img.shields.io/github/license/yunyun1976/mesugaki-bot?style=for-the-badge&color=ffb6c1)](LICENSE.md)
[![Stars](https://img.shields.io/github/stars/yunyun1976/mesugaki-bot?style=for-the-badge&color=ffc0cb)](https://github.com/yunyun1976/mesugaki-bot/stargazers)
[![Downloads](https://img.shields.io/github/downloads/yunyun1976/mesugaki-bot/total?style=for-the-badge&color=ff1493)](https://github.com/yunyun1976/mesugaki-bot/releases)

[![Python](https://img.shields.io/badge/Python-3.15+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![discord.py](https://img.shields.io/badge/discord.py-2.7.1+-5865F2?style=for-the-badge&logo=discord&logoColor=white)](https://discordpy.readthedocs.io/)
[![SQLite](https://img.shields.io/badge/SQLite-3-003B57?style=for-the-badge&logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![uv](https://img.shields.io/badge/uv-Package%20Manager-000000?style=for-the-badge&logo=python&logoColor=white)](https://github.com/astral-sh/uv)
[![YAML](https://img.shields.io/badge/YAML-Messages-CB171E?style=for-the-badge&logo=yaml&logoColor=white)](https://yaml.org/)

---

### 概要も知らないの？♡ ざぁこ♡

このDiscord Botは、お兄ちゃん/お姉ちゃんみたいなザコをからかうために作られたんだよ〜♡  
アタシの魅力にひれ伏しなさいよね♡

</div>

## 🎀 主な機能♡

- **罵倒**: キミにぴったりの言葉を投げかけてあげる♡
- **わからせ**: わからせられるぉぉぉお♡♡♡
- **NGワードフィルタ**: お下品な言葉は登録させてあげないんだから♡
- **データ保存先の切り替え**: ローカルでも外部APIでも、好きな方を選ばせてあげる♡
- **マスターユーザー管理**: アタシを操れるのは選ばれた人だけ！
- **おやすみタイマー**: 夜はアタシも寝るから、勝手に話しかけないでよね♡

## 🛠️ セットアップと実行♡

キミみたいなザコでも分かるように、特別に説明してあげるね♡

### 1. コードの入手♡
```bash
git clone https://github.com/yunyun1976/mesugaki-bot.git
cd mesugaki-bot
```

### 2. 環境構築♡
`uv` を使って一瞬で終わらせてあげるわ♡
```bash
# 依存ライブラリのインストールと環境構築
uv sync
```

### 3. 起動♡
キミみたいなザコはトークンを漏らしそうだから、環境変数で設定するのが推奨だよ♡

#### **推奨：コマンドラインで設定（一時的）♡**
セキュリティ的に一番安全な方法よ♡

- **Linux / macOS の場合♡**
  ```bash
  export DISCORD_TOKEN="your_token_here"
  uv run src/main.py
  ```

- **Windows (PowerShell) の場合♡**
  ```powershell
  $env:DISCORD_TOKEN="your_token_here"
  uv run src/main.py
  ```

#### **非推奨：.env ファイルを使う場合♡**
どうしてもって言うなら、`.env` ファイルを作ってアタシの魂（トークン）を入れなさいよね♡  
※外部に漏らさないように厳重に注意すること！

```env
DISCORD_TOKEN=your_token_here
```

その後、以下のコマンドで起動してね♡
```bash
uv run src/main.py
```

## 🗄️ データの保存先を選べるんだよ♡

アタシが覚えた言葉、どこに置くか選ばせてあげる♡ 環境変数 `PHRASE_BACKEND` で切り替えてね♡

| `PHRASE_BACKEND` | 保存先 | 説明 |
| :--- | :--- | :--- |
| `sqlite`（既定） | ローカルのSQLite | `data/` に保存。何も設定しなくてもコレだよ♡ |
| `api` | 外部API | [dac-bot-integrated](https://github.com/kurosiko/dac-bot-integrated) に保存♡ |

`api` を使うときは、こんな環境変数も教えてよね♡

| 環境変数 | 必須 | 説明 |
| :--- | :--- | :--- |
| `API_BASE_URL` | ✅ | APIのベースURL（例: `https://your-worker.workers.dev`） |
| `API_TYPE` | ー | 語彙のtype（既定: `mesugaki`） |
| `API_TOKEN` | ー | 認証トークン（設定時のみ `Authorization: Bearer` で送信） |

```powershell
$env:PHRASE_BACKEND="api"
$env:API_BASE_URL="https://your-worker.workers.dev"
uv run src/main.py
```

起動するとアタシが今どっちを使ってるか教えてあげる♡ ちゃんと確認しなさいよね♡

```text
Phrase backend: SQLite (local)
# または
Phrase backend: API (https://your-worker.workers.dev, type=mesugaki)
```

> **ざぁこ向け注意♡**: 外部APIに切り替えても、その `type` の語彙が空っぽだとアタシは何も言えないからね♡ `/add_batou` とかで言葉を登録してからじゃないと、罵倒もわからせもスカスカだよ♡

## 📜 コマンド一覧♡

| カテゴリ | コマンド | 説明 |
| :--- | :--- | :--- |
| **一般** | `/help` | 使えるコマンドを教えてあげる♡ |
| **メッセージ** | `/batou` | アタシがキミを罵倒してあげる♡ |
| | `/wakarase` | わからせてほしいのぉぉぉお♡♡♡ |
| **語彙追加** | `/add_batou` | 新しい罵倒の言葉、教えてよ♡ |
| | `/add_wakarase` | 新しいわからせ、期待してるよ♡ |
| **管理** | `/add_master` | マスターユーザーを増やしちゃう♡ |
| | `/set_channel` | ここをアタシの拠点にするね♡ |
| **NGワード** | `/add_ng_word` | 登録できない言葉を決めちゃう♡ |
| | `/remove_ng_word` | NGワードを解除してあげる♡ |
| | `/list_ng_word` | NGワードの一覧を見せてあげる♡ |
