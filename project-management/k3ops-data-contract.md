# K3Ops Data Contract

## Scope

この契約は、将来のK3Opsが`project-management/roadmaps/development-operations.toml`と`tasks/T-*.md`を安全かつ決定論的に読むための契約である。Parser、API、UIの実装契約ではない。

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
