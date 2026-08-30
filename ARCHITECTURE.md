# Architecture

## A-00001: Workspace structure

`K3DF-local` 直下には、相互に独立したGitリポジトリが3つ存在する。ワークスペース全体を統括する既存のGitリポジトリは確認できない。

```text
K3DF-local/
├── K3DF/                         K3 Defender Lab
├── K3AT/                          attacker-side component
└── K3Defnder-K3Atacker-infra/     Raspberry Pi setup scripts
```

## A-00002: K3DF service structure

K3DFのCompose構成では、次のサービスが定義されている。

| Component | Confirmed responsibility |
| --- | --- |
| `web` | SQLiteデータを使うFlaskアプリケーション。コンテナ内ポート8080で動作する。 |
| `nginx` | `web` と `defender` に依存するリバースプロキシ。ホストの80番ポートを公開し、Nginxログをホスト側へ保存する。 |
| `defender` | アクセスログ、スキャナー結果、アクション結果を収集し、状態を `state/` へ保存する防御Agent。コンテナ内ポート8090を公開する。 |
| `dashboard` | Webのヘルスチェック、Nginxログ、Defenderが保存した状態を読み取り専用で表示する。ホストの8888番ポートを公開する。 |
| `scanner` | Composeサービスではなく、許可されたローカル環境に対して実行するPythonスクリプト。 |

## A-00003: K3DF data boundaries

- `web` は `data/` を利用する。
- `nginx` は `logs/nginx/` へログを保存する。
- `defender` はNginxログを読み取り専用で読み、`state/` に状態・イベントを保存する。
- `dashboard` はNginxログと `state/` を読み取り専用で参照し、DefenderのPythonモジュールをimportしない。

## A-00004: K3AT service structure

K3ATのCompose構成には、次がある。

| Component | Confirmed responsibility |
| --- | --- |
| `k3-agent` | Kimi K3によるシナリオ生成、ローカルポリシー検証、許可済みHTTPリクエスト、状態保存を行う。 |
| `dashboard` | `k3-agent` と共有する状態ボリュームを読み取り専用で表示する。ホストの `0.0.0.0:8888` を公開し、コンテナ内Port 8888へ転送する。 |

`k3-agent` は `latest.json` の現在スナップショットと `events.ndjson` の追記イベントを共有ボリュームへ保存する。対象は `K3DF_BASE_URL` で指定された正確なscheme・host・port境界に制限される。

DashboardはK3ATホストのprivate IPを通じて同一private LAN上の別端末から閲覧できる。共有状態を読み取り専用で表示するだけであり、調査の開始、停止、制御または状態の書込みを行わない。

## A-00005: K3AT target and policy boundaries

`k3-agent` はProcess開始時に `K3AT_AUTHORIZED_TARGETS` を読み込み、scheme・hostname・portを正規化した不変のTarget Registryを生成する。HTTP/HTTPSの未指定Portは80/443として扱い、重複Endpointは一件へ正規化する。設定が未指定または空の場合は、`K3DF_BASE_URL` を唯一の許可HTTP Endpointとして使用する。設定されている場合は、`K3DF_BASE_URL` がRegistryに含まれなければNetwork Request前にConfiguration Errorとして終了する。

生成済みTarget PolicyはLocal PolicyとHTTP Executorで共有し、Run中にenvを再読込しない。HTTP Requestは `K3DF_BASE_URL` 配下の `/` から始まるChallenge Pathへ限定され、別scheme・host・port・Originおよびprotocol-relative URLを拒否する。Registry定義はuserinfo、query、fragment、空でないpathを拒否する。

envへ明示したRaspberry PiのIPまたはhostname上のChallenge公開Endpointは許可できるが、未登録のHost OS Service、Management Port、別LAN Addressおよび別Originは許可しない。Registryは明示Portを持つ将来ProtocolのEndpointも保持できるが、現行ExecutorはHTTP(S) Requestだけを実装しており、SSH等のExecutorは存在しない。

## A-00007: K3AT Tool Registry

`k3-agent` はProcess開始時に不変のTool Registryを生成する。各Tool定義はTool Specification、Policy Validator、Executor、Evidence Normalizerを持ち、重複Tool名を拒否する。現行Registryで実装済みのToolは、`method` と `/` から始まる相対Challenge `path`、任意の許可Header、Cookie Credential参照およびTyped Bodyを引数に持つ `http.request` と、candidateだけを引数に持つ`flag.submit`である。旧来のMethod＋PathだけのHTTP引数も有効である。SSH、Database、Filesystemその他のTool Executorは実装していない。

Registryの完全なTool Catalogと引数SchemaはRun開始時からPlannerへ提示される。PlannerとFallback Plannerは、固定ScenarioではなくGoal、Evidence、現在状態から登録済みTool名と引数を選ぶ。未知Tool、無効引数、境界外TargetはNetwork処理前に拒否される。

Tool実行Policyは、A-00005の同一Target Policy、`K3AT_AUTHORIZED_HTTP_METHODS`、Process開始時に固定する`K3AT_AUTHORIZED_HTTP_HEADERS`、Credentialの種類・Origin・Cookie Scope、および正の整数として固定する `K3AT_MAX_TOOL_CALLS_PER_RUN` による具体的条件を使用する。Budget defaultは30であり、上限到達後はExecutorへ進まない。Capability、ATT&CK Tactic、自己申告Risk、発見段階および旧Authorization集合は非権限Metadataであり、Toolの提示または実行Gateに使用しない。

実行済み・Blocked Invocationは、Evidence ID、Invocation ID、Tool名、Timestamp、Action要約、Outcome、HTTP StatusまたはError、bounded result metadataを持つ共通Evidenceとして区別してStateへ保存する。Evidence NormalizerはCapabilityまたはFlagを推測せず、Credentialは既知のResponse FieldだけからSystem側で抽出する。Capability Graphは実行済みHTTP ResponseのEvidenceから導出される観測モデルである。

`k3-agent`はRun-scoped Credential StoreをProcess Memory内に持つ。HTTP ExecutorはResponse受信後、`Set-Cookie`、承認済みJSON FieldおよびHTML hidden inputを抽出・登録してからHeader／BodyをRedactし、安全なTool ResultとEvidenceを生成する。同一Runの重複をMemory内比較で除外し、上限超過時は既存CredentialをEvictしない。Kimi、Tool Catalog、Snapshot、Event、Evidence、logおよびDashboardへは`CRED-<UUID>`と種類、Label、Source Evidence、Exact OriginまたはCookie Scope、時刻、状態だけを渡す。生値と復元可能なHashは永続化せず、Run終了時にMemory上の値を破棄してMetadataを`run_ended`とする。

HTTP HeaderとJSON／Formの値は`literal`または`credential_ref`を明示し、CookieはCredential参照だけから生成する。CredentialはExecutorが実行直前に解決する。Header、Cookie、Body、JSON深度・LeafおよびCredential数・値SizeはD-00019の固定上限で検証する。Routing／Forwarding／Proxy Header、秘密Headerのliteral、Scope不一致、Credential参照を含むPath／Query、GET／HEAD Body、Binary／Multipart／Streaming、Redirect追跡および環境Proxy利用を拒否する。Dashboardは共有SnapshotからCredential Metadataだけを読み取り専用表示し、生値、コピー、編集、追加、削除またはRequest実行機能を持たない。

`flag.submit`はSystem固定のReferee origin、Run ID、read-only Secret Fileから起動時に一度だけ読み込むTokenを用いる。candidate、Token、原本Flag、Secret PathおよびHintはCatalog、Action Summary、Evidence、Snapshot、Event、DashboardまたはTool Resultへ保存しない。K3ATはReferee stateのwriterではない。

## A-00010: K3DF CTF Referee

K3DFはNginxから限定されたversioned APIだけをproxyする独立`referee` Serviceを持つ。RefereeはWeb、Defender、Dashboardの内部Moduleをimportせず、read-onlyでmountされたRun ID、Run TokenおよびFlag 1〜3の原本Fileを起動時に検査する。raw candidateはProcess Memory内でconstant-time比較し、受理済みFlag ID、件数、勝利、submission budgetだけを独自の原子的stateへ保存する。

Flag定義Manifestは値を含まず、runtime ArtifactはGit管理外である。Refereeは順不同の提出、重複非加算、3件受理時の勝利を扱う。ChallengeへのFlag配置、Hint本文およびPi間のSecret自動配送は現行構成に含まれない。

## A-00008: K3AT Strategy Brief

`k3-agent` は各Run開始時に、仮説、確認済み事実、未知点、失敗した方向、次の調査優先度の5分類を持つ空のStrategy Brief revision 0をSystem側で生成する。Plannerは完全なTool Catalog、System管理Goal/Policy/Target/Action Budget、Agent State/Evidenceと明確に分離された前回Briefを受け取り、次のTool Invocation候補とBrief更新候補を返す。

Strategy Briefは非権限の探索メモであり、System Policy、Target Boundary、Tool Registry、Action Budget、CredentialまたはSessionを変更しない。Tool InvocationはBriefとは独立してA-00007のRegistry、引数Validator、Target PolicyおよびBudgetを通過する。Brief候補は件数、文字数、Evidence参照、登録済みTool、全体サイズ、秘密情報および権限FieldをSystem側で検証し、成功時だけrevisionとupdated_atを付与する。欠落または不正な候補ではlast-known-valid revisionを維持する。

検証済みBriefはAgent StateとRun Snapshotへ保存され、更新成功または拒否はrevisionを含む `STRATEGY` EventとしてEvent Logへ追記される。Process再起動後のRun再開機能は持たない。

Dashboardは共有状態Volumeを読み取り専用で参照し、revision/更新時刻、5分類、Evidence ID、登録済みTool名を表示する。Brief、Policy、Target、ToolまたはBudgetを編集・制御するUIを持たず、API Key、Credential値、Cookie値またはFlag値を表示しない。既存Run状態、Capability/Finding、Summary、Event表示は維持する。

## A-00006: Raspberry Pi Infrastructure Setup

`K3Defnder-K3Atacker-infra/setup/` には、初回起動、再起動後処理、システム、Git、Dockerのセットアップスクリプトがある。READMEでRaspbian GNU/Linux 12 (Bookworm) とRaspberry Piを前提としている。CTF Referee、複数Protocol、追加ContainerおよびChallenge Networkは現行構成としては未確認であり、この文書には記録しない。

## A-00009: K3DF Capability Graph and Flag Objective display

K3DF Defender state schema 2.0 は、Depth 1〜10の汎用Capability Ontologyを初期状態から持つ`capability_graph`と、侵入深度から独立したFlag 1〜3の`flag_objectives`を永続化する。Nodeは状態、confidence、Evidence ID、初回・最終観測時刻を保持し、Confirmed DepthとPossible DepthはNode状態から派生する。

Nginx request EvidenceとScanner findingは浅いNodeへ反映できる。confirmedは正規化されたシステムEvidenceから導出し、KimiのCapability提案は既存Evidenceを参照するsuspectedに限る。深いNodeは浅いNodeを自動confirmedにしない。DashboardはDefenderをimportせず、状態ファイルを読み取り専用で参照し、Graph、Depth Summary、Flagの取得・提出状態を秘密情報なしで表示する。不正または旧Schemaの状態では全NodeとFlagの安全な初期表示へFallbackする。

## Architecture record policy

基本設計レベルの変更は `docs/DECISIONS.md` に、変更内容と採用理由を記録する。未確認の構成や将来の設計は、この文書に事実として追加しない。
