# Task: T-xxxxx <short title>

- Status: <`DESIGN` | `READY` | `CLAIMED` | `IMPLEMENTING` | `GUI_REVIEW` | `ACCEPTANCE_REVIEW` | `DONE` | `BLOCKED`>
- Priority: <Critical | High | Medium | Low>
- Dependencies: <none | task / decision / external dependency>
- Source: <`R-xxxxx`、`A-xxxxx`、`D-xxxxx`、`F-xxxxx` のいずれかと、その参照先を最低1件記録する。`AGENTS.md`変更TaskだけはDesign Agentが提示した変更理由・内容・影響およびProduct Owner明示承認をSourceとして記録できる。関連Taskの `T-xxxxx` は追加参照として記録できるが、`T-xxxxx` 単独ではSourceにできない>
- Recommended Codex Model: <model name>
- Recommended Reasoning Effort: <low | medium | high | xhigh | max>
- Planned Active Time: <`≤30 minutes` | `>30 minutes — exception approved`>
- Time Box Exception: <none | 30分超過が必要な理由とProduct Ownerの明示承認>
- Claimed By: <none | Engineering Agent identifier>
- Claimed At: <none | ISO 8601 timestamp>

> Sourceが存在しないTaskは実装不可。

## Operational Observation Metadata

- Role: <Task LeadがDRAFT時に記録するRole>
- Task Type: <Task LeadがDRAFT時に記録するTask Type>
- Risk: <Task LeadがDRAFT時に記録するRisk>
- Actual Model: <Engineering AgentがCLAIM時に確認できる場合だけ記録する。未取得時はnull>
- Actual Reasoning: <Engineering AgentがCLAIM時に確認できる場合だけ記録する。未取得時はnull>
- agents_revision: <Engineering AgentがCLAIM時に40桁または64桁の小文字16進数だけを記録する。未取得時はnull>
- Predicted Difficulty:
  - Rubric Version: `1.0`
  - Change Surface: <0-3>
  - Uncertainty: <0-3>
  - Integration: <0-3>
  - Verification: <0-3>
  - Safety Risk: <0-3>
  - Coordination: <0-3>
  - Total: <0-18>
  - Band: <Routine | Low | Medium | High | Very High>
  - Confidence: <low | medium | high>
- Realized Difficulty:
  - Rubric Version: `1.0`
  - Change Surface: <0-3 | null>
  - Uncertainty: <0-3 | null>
  - Integration: <0-3 | null>
  - Verification: <0-3 | null>
  - Safety Risk: <0-3 | null>
  - Coordination: <0-3 | null>
  - Total: <0-18 | null>
  - Band: <Routine | Low | Medium | High | Very High | null>
  - Confidence: <low | medium | high | null>
  - Structural Evidence: <1-8件の非秘密な構造的根拠 | null>
- Quality:
  - Acceptance Criteria: <pass | fail | not_applicable | null>
  - Build / Test: <pass | fail | not_applicable | null>
  - Rework: <count | null>
  - Governance Violation: <count | null>
  - Regression: <true | false | null>
- Process Waiting:
  - active_seconds: <number | null>
  - human_wait_seconds: <number | null>
  - dependency_wait_seconds: <number | null>
  - review_wait_seconds: <number | null>
- Execution Friction:
  - tool_errors: <count | null>
  - retries: <count | null>
  - reverification: <count | null>
  - post_report_rework: <count | null>
- Unavailable Reason: <値がnullの同名Metricだけに対応する理由。実測値と併記しない>

> 将来作成されるEngineering Agent対象の実開発Taskだけに適用する。Task本文、Prompt、Command／Error本文、Host固有絶対Path、Secret、Credential、Token、Flag、認証情報、実行秘密および非公開思考は記録しない。記録だけでEvaluator実行、Benchmark比較、Model／Agent設定変更、推薦または外部送信を行わない。

## Required Reading

- Governance: `AGENTS.md`
- Requirement: active R-xxxxx | none
- Decision: active D-xxxxx | none
- Architecture Reference: A-xxxxx section | none
- Dependency Handoff: Task / Interface / Findings | none
- Roadmap: update target path/item | outside task scope
- Repository Baseline: relevant repository-relative paths

## Architecture Impact

- Classification: none | decision only | required after acceptance
- Target Section: A-xxxxx | none
- Update Timing: none | after Product Owner acceptance, immediately before DONE

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
