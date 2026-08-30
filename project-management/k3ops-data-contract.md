# K3Ops Data Contract

## Scope

この契約は、将来のK3Opsが`project-management/roadmaps/development-operations.toml`と`tasks/T-*.md`を安全かつ決定論的に読むための契約である。Parser、API、UIの実装契約ではない。

Product正本は`project-management/roadmaps/product.toml`、Development Operations正本は`project-management/roadmaps/development-operations.toml`とする。両者はFile単位で独立Parseし、一方の不正で他方を失敗させず、Item IDの同名を暗黙mergeしない。既存のSchema、Size、Count、String、Horizon、Task ID、reference上限を両Roadmapへ適用する。Task Metadataは引き続きTask Fileだけを正本とし、RoadmapへStatus、Priority、Claim、Acceptance、Commit、Branch、集計値を保存しない。Product／Development OperationsのItem数、完了数、完了率、PLANNED、進行中、レビュー中、BLOCKED、Warningは別々に計算する。Product Roadmap ReferencesはAPI／UIへ表示しない。Secret、Credential、Token、Flag値、Hint本文、配置Path、正解経路、非公開思考をProduct Roadmapへ記録・表示しない。K3OpsはPRODUCT.md、DECISIONS.md、ARCHITECTURE.mdをmount、探索、Parseせず、Product Roadmap Fileだけを将来read-only mountできる。WarningはSource識別可能な正規化CodeだけとしRaw Error／Pathを出さない。

## Roadmap TOML

- UTF-8の通常Fileだけを読み、Schema Versionは必須の文字列とする。
- `workstreams`は1件以上、各Workstreamは一意の`id`と非空`name`を持つ。
- Itemは一意の`id`、`horizon`、正の`display_order`、非空`name`・`purpose`、`task_ids`配列、`references`配列を必須とする。
- `horizon`は`now`、`next`、`later`、`ongoing`だけを許可する。Task IDは`T-`+5桁数字形式とし、同一Item内で重複させない。
- 最大値はWorkstream 32、Item 256、Task ID 64／Item、reference 64／Item、文字列4 KiB、ファイル1 MiBとする。超過、不正TOML、未知必須型、重複IDはData Warningとし安全に未完了扱いにする。
- Status、Priority、Claimed By／At、Acceptance、Branch、Commit、集計結果はRoadmapに保存しない。これらはTask Markdownだけを正本とする。

## Task metadata allowlist and safety

Taskから読むのはファイル名のTask ID、Title、Status、Priority、Dependencies、Source、Claimed By、Claimed At、Product Owner Acceptanceだけとする。既存Lifecycle Statusは`DESIGN`、`READY`、`CLAIMED`、`IMPLEMENTING`、`GUI_REVIEW`、`ACCEPTANCE_REVIEW`、`DONE`、`BLOCKED`のみである。

Task Pathは`tasks/`直下の`T-*.md`通常Fileだけを許可する。Path traversal、Symlink、Directory、特殊File、サイズ超過（1 MiB）、件数超過（1,024）を拒否しData Warningにする。Secret、Credential、Token、Flag、本文の機密情報、Git情報は表示・集計しない。

## Aggregation

- `PLANNED`は`task_ids = []`のRoadmap Item表示でありLifecycle Statusではない。
- 「進行中」は`CLAIMED`と`IMPLEMENTING`の集計表示、「レビュー中」は`GUI_REVIEW`と`ACCEPTANCE_REVIEW`の集計表示であり、いずれも新Statusではない。`BLOCKED`は独立表示する。
- Itemは関連Taskが1件以上あり、その全件が`DONE`のときだけ完了とする。Task未作成ItemはPLANNEDかつ未完了である。
- 完了率は、全Itemを分母、完了Itemを分子とする。複数Task Itemは各Taskの実Statusと`DONE件数/関連Task数`を表示し、合成Lifecycle Statusを作らない。
- 欠落Task、ID不一致、許可外Status、不正Metadataは未完了としてData Warningを生成する。

## Display boundary

表示可能なのはRoadmap Item名、Horizon、目的、Task ID、Task allowlist、集計表示、Data Warning、完了率である。表示禁止はSecret、Credential、Token、Flag、実行秘密、非公開思考、Task本文、Commit・Branch詳細、認証情報である。
