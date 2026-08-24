# Architecture

## Workspace structure

`K3DF-local` 直下には、相互に独立したGitリポジトリが3つ存在する。ワークスペース全体を統括する既存のGitリポジトリは確認できない。

```text
K3DF-local/
├── K3DF/                         K3 Defender Lab
├── K3AT/                          attacker-side component
└── K3Defnder-K3Atacker-infra/     Raspberry Pi setup scripts
```

## K3DF

K3DFのCompose構成では、次のサービスが定義されている。

| Component | Confirmed responsibility |
| --- | --- |
| `web` | SQLiteデータを使うFlaskアプリケーション。コンテナ内ポート8080で動作する。 |
| `nginx` | `web` と `defender` に依存するリバースプロキシ。ホストの80番ポートを公開し、Nginxログをホスト側へ保存する。 |
| `defender` | アクセスログ、スキャナー結果、アクション結果を収集し、状態を `state/` へ保存する防御Agent。コンテナ内ポート8090を公開する。 |
| `dashboard` | Webのヘルスチェック、Nginxログ、Defenderが保存した状態を読み取り専用で表示する。ホストの8888番ポートを公開する。 |
| `scanner` | Composeサービスではなく、許可されたローカル環境に対して実行するPythonスクリプト。 |

確認できるデータ境界は次のとおり。

- `web` は `data/` を利用する。
- `nginx` は `logs/nginx/` へログを保存する。
- `defender` はNginxログを読み取り専用で読み、`state/` に状態・イベントを保存する。
- `dashboard` はNginxログと `state/` を読み取り専用で参照し、DefenderのPythonモジュールをimportしない。

## K3AT

K3ATのCompose構成には、次がある。

| Component | Confirmed responsibility |
| --- | --- |
| `k3-agent` | Kimi K3によるシナリオ生成、ローカルポリシー検証、許可済みHTTPリクエスト、状態保存を行う。 |
| `dashboard` | `k3-agent` と共有する状態ボリュームを読み取り専用で表示する。ホストの `127.0.0.1:8889` を公開する。 |

`k3-agent` は `latest.json` の現在スナップショットと `events.ndjson` の追記イベントを共有ボリュームへ保存する。対象は `K3DF_BASE_URL` で指定された正確なscheme・host・port境界に制限される。

## Infrastructure setup

`K3Defnder-K3Atacker-infra/setup/` には、初回起動、再起動後処理、システム、Git、Dockerのセットアップスクリプトがある。READMEでRaspbian GNU/Linux 12 (Bookworm) とRaspberry Piを前提としている。

## Architecture record policy

基本設計レベルの変更は `docs/DECISIONS.md` に、変更内容と採用理由を記録する。未確認の構成や将来の設計は、この文書に事実として追加しない。
