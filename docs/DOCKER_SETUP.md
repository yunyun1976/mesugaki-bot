# Docker環境による低スペック環境の再現とテスト

Raspberry Pi Zero WH（ARMv6）などの低スペック環境で発生する「インタラクション・タイムアウト（error code: 10062）」を再現し、対策をテストするためのDocker環境について説明します。

## 1. 再現用イメージのビルド

以下のコマンドで、Python 3.13ベースの再現用イメージを作成します。

```bash
docker build -t mesugaki-repro -f Dockerfile.repro .
```

※ビルドがうまくいかない場合は `--no-cache` オプションを付けて試してください。

## 2. リソース制限付きでの実行

Raspberry Pi Zero WHのシングルコア性能に近づけるため、CPU使用率を10%（0.1コア分）に制限して実行します。

```bash
docker run --rm \
  --cpus=".1" \
  --memory="512m" \
  --env-file .env \
  -v "C:/path/to/your/project/data:/app/data" \
  mesugaki-repro
```

### オプション解説
- `--cpus=".1"`: CPUリソースを極端に制限し、処理の遅延を擬似的に発生させます。
- `--memory="512m"`: メモリをPi Zero WHと同等に制限します。
- `-v`: データベースファイルをホスト側と同期させます。パスは絶対パスで指定することを推奨します。

## 3. テスト項目

この環境下で以下の挙動を確認します。
1. Discordでコマンドを打った直後に「(ボット名) が考えています...」と表示されるか。
2. 3秒のタイムアウト制限を超えずにメッセージが正常に届くか。
3. 公開コマンド（/batou等）と非公開コマンド（/help等）の表示範囲が正しいか。
