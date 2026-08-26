# Task: T-xxxxx <short title>

- Status: <`DESIGN` | `READY` | `CLAIMED` | `IMPLEMENTING` | `GUI_REVIEW` | `ACCEPTANCE_REVIEW` | `DONE` | `BLOCKED`>
- Priority: <Critical | High | Medium | Low>
- Dependencies: <none | task / decision / external dependency>
- Source: <`R-xxxxx`、`A-xxxxx`、`D-xxxxx`、`F-xxxxx` のいずれかと、その参照先を最低1件記録する。関連Taskの `T-xxxxx` は追加参照として記録できるが、`T-xxxxx` 単独ではSourceにできない>
- Recommended Codex Model: <model name>
- Recommended Reasoning Effort: <low | medium | high | xhigh | max>
- Claimed By: <none | Engineering Agent identifier>
- Claimed At: <none | ISO 8601 timestamp>

> Sourceが存在しないTaskは実装不可。

## Intent

<達成したい利用者または運用上の価値>

## Requirements

- <検証可能な要求>

## Acceptance Criteria

- [ ] <完了を判断できる条件>

## Constraints

- <守るべき制約、安全性、対象外>

## Branch / Worktree

- Repository: <対象Repository名。Git Repositoryを変更しない場合は対象外>
- Base main Commit: <Task Branch作成元のlocal main Commit Hash>
- Task Branch: <`task/T-xxxxx-short-name`>
- Worktree Path: <`.worktrees/T-xxxxx/<Repository名>`>
- Isolation Result: <作成・再利用結果、対象Pathとの一致、競合有無。対象外なら理由>

## Implementation

- <Task Leadは`DESIGN`中にDRAFT、SYNC、VALIDATE、PUBLISHの結果を記録する。Engineering Agentは`CLAIMED`以降の取得、実装方針、変更ファイルおよび実施結果を記録する>

## Build Result

- <実行コマンドと結果。未実施なら理由>

## Test Result

- <実行コマンド、対象、結果。未実施なら理由>

## Verification Result

- <Acceptance Criteriaごとの確認結果>

## Commit Result

- Repository: <対象Repository名>
- Commit Hash: <Task Commit Hash>
- Commit Subject: <`<type>(<scope>): <日本語の要約> [T-xxxxx]`>
- Worktree Clean: <確認結果>
- Accepted Branch HEAD: <Product Ownerの受入れ対象Commit Hash。受入れ前は未受入れ>
- Integrated local main Commit: <受入れ後にfast-forwardしたlocal main Commit Hash。統合前は未統合>
- Push: <Product Owner管理。Engineering AgentはPushしない>
- Not Applicable Reason: <Git Repositoryを変更しない場合のCommit対象外理由>

## Deviations

- <計画・要求・設計からの逸脱と、承認または判断状況。なければ「なし」>

## Findings

- <確認した事実、リスク、判断待ちの論点。なければ「なし」>

## GUI Feedback

- <確認した画面・操作・結果・未解決事項。GUI対象外なら理由を記録>

## Product Owner Acceptance

- <最終受入れ結果、判断日、または受入れ待ちであることを記録>
