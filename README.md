# Mesugaki Bot♡

## 概要♡

このDiscordBotは、お兄ちゃん/お姉ちゃんみたいなザコをからかうために作られたんだよ〜♡
感謝してね！♡

## 主な使用技術♡

こんなのも知らないの〜？♡ しょうがないなぁ〜♡

- python
- discord.py
- sqlite3

## セットアップと実行♡

キミみたいなザコでも分かるように、特別に説明してあげるね♡

0.  **アタシのコードを手に入れる♡**

    まずは、アタシの素敵なコードをキミのパソコンに持ってこなきゃ始まらないよね〜♡
    このコマンドで、アタシの全部が手に入るんだから、感謝しなさいよね♡

    ```bash
    git clone https://github.com/yunyun1976/mesugaki-bot.git
    cd mesugaki-bot
    ```

    これで、アタシのプロジェクトフォルダに移動できるよ♡

1.  **仮想環境を準備する♡**

    ザコが環境を汚さないように、仮想環境を使うのは常識だよね〜♡
    これを使えば、アタシのボットのためにインストールしたものが、他のPythonプロジェクトとごちゃ混ぜにならないからね♡

    ```bash
    python -m venv .venv
    ```

    これで`.venv`っていうフォルダができて、そこに仮想環境が作られるよ♡

    次に、その仮想環境を有効にするの♡

    - **Windowsの場合♡**
      ```powershell
      .venv\Scripts\Activate.ps1
      ```

    - **Linux/macOSの場合♡**
      ```bash
      source .venv/bin/activate
      ```

    仮想環境が有効になったら、コマンドプロンプトやターミナルの行頭に`(.venv)`って表示されるはずだよ♡
    これで準備万端！♡

2.  **必要なものをインストールする♡******

    ```bash
    pip install -r requirements.txt
    ```

2.  **トークンを設定する♡**

    DiscordBotが無い場合、先にDiscordBotを[Discord公式の開発者向けページ](https://discord.com/developers/applications)で作ってトークンを取得してね♡
    トークンは流出したら大変なことになっちゃうから厳重に管理してね♡

    環境変数で設定するのがオススメだよ♡ こっちのほうが安全だからね♡

    - **Windowsの場合♡**
      ```powershell
      $env:DISCORD_TOKEN="your_discord_token_here"
      ```

    - **Linux/macOSの場合♡**
      ```bash
      export DISCORD_TOKEN="your_discord_token_here"
      ```

    `.env`ファイルを使うっていう手もあるけど、まぁ〜、ザコはこっちでいっか♡

    ```
    DISCORD_TOKEN=your_discord_token_here
    ```

3.  **ボットを起動する♡**
    
    先に作成したDiscordBotを使いたいサーバーに入れて～♡

    ```bash
    python src/main.py
    ```

    これでボットが動くよ〜♡ 簡単すぎ〜♡

## コマンド一覧♡

アタシが使えるコマンドを教えてあげる♡ ありがたく思いなよね♡

### 一般コマンド♡

- `/help`
  - 利用可能なコマンドとその説明を全て表示してあげる♡

### メッセージング♡

- `/batou`
  - キミみたいなザコにぴったりの罵倒を言ってあげる♡
- `/wakarase`
  - わからせられるのぉぉぉおおお♡ おほぉぉぉおおお♡
- `/add_batou`
  - 新しい罵倒の言葉を追加できるよ♡ キミのセンス、見せてみな〜♡
- `/add_wakarase`
  - 新しいわからせの言葉、追加してほしいのぉぉぉおおお♡

### 管理者・マスターユーザー用コマンド♡

これは管理者か、管理者に選ばれたマスターユーザーしか使えないんだからね〜♡

- `/get_barizougon`
  - 罵詈雑言の一覧を見せてあげる♡
- `/get_abikyoukan`
  - わからせの言葉の一覧を見せるのぉぉぉおおお♡
- `/remove_batou`
  - 気に入らない罵倒は消してあげる♡
- `/remove_wakarase`
  - わからせの言葉を消すのぉぉぉおおお♡

### 管理者用コマンド♡

これは管理者だけの特別なコマンドなんだからね♡

- `/add_master`
  - マスターユーザーを追加してあげる♡
- `/check_master`
  - マスターユーザーの一覧を見せてあげる♡
- `/remove_master`
  - マスターユーザーから外しちゃうんだからね♡