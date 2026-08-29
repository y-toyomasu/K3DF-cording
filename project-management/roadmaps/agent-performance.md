# Agent Performance Roadmap

## Purpose

品質、安全性、Traceabilityを維持しながら、応答時間、Tool利用、Context量および手戻りを、固定Benchmarkと測定結果に基づいて改善する。`AGENTS.md`、Playbook、Model、Reasoning Effortの最適化は感覚ではなく測定に基づく。

## Principles

- 品質を速度より優先し、品質条件を満たす実行だけを比較する。
- 一度に一要因だけを変え、現行構成のBaseline取得後に最適化する。
- Evaluatorは読み取り専用で、結果からAgent設定やTaskを自動変更しない。判断と優先順位はProduct Ownerが決定する。
- 非公開思考を取得・評価しない。Token、Costは実行環境から取得できる場合だけ記録し、推測を事実にしない。

## Metrics

### Quality

Acceptance Criteria達成率、Build／Test成功率、受入れまでの修正回数、Design手戻り、Governance違反、他Task・利用者変更の混入、不必要な`BLOCKED`、必要な`BLOCKED`の見逃しを扱う。

### Performance

Wall-clock、最初のTool Callまでの時間、Tool Call、同一ファイル再読込、Command retry、Build／Test再実行、Input／Output Token、Cost、Context量、`AGENTS.md`・Playbook読込量を扱う。取得不能値は測定不能として報告する。

### Process

`CLAIMED`→`IMPLEMENTING`、`IMPLEMENTING`→Review、`BLOCKED`回数・滞在時間、Review→Acceptance、不必要な確認、無関係文書・Repository読込、REPORT後の修正・再検証を扱う。

## Benchmark Suite

固定Snapshotまたは使い捨て環境で次を実行し、実プロジェクトのTask状態やProduct Codeを変更しない。

1. Task進捗の読み取りレビュー
2. 新規TaskのDesign
3. Task LeadによるTask作成と公開
4. 文書だけの小規模変更
5. 単純なUI修正
6. Task Branch・worktreeを伴う通常実装
7. 安全境界を伴う複雑実装
8. GUI Review後のStatus遷移
9. `BLOCKED` Taskの再開判断
10. Product Owner受入れ後のlocal main統合

各Benchmarkは入力、期待結果、合否条件、Task種別、難易度、Model、Reasoning Effort、Prompt Version、複数回のRunを定義する。

## Operational Observation Pilot

固定BenchmarkはModel／Prompt／AGENTS変更の因果比較とRegression確認に維持する。Operational Baselineは実開発Taskをread-only観測し、異なるTaskを直接A/B比較せず、Role、Task Type、Difficulty、Risk、AGENTS Versionで比較可能性を限定する。個別生RecordはGit管理外とし、追跡対象はSchema、Rubric、Evaluator、Test、Sanitized Fixture、手順および別途承認済み集計Reportだけとする。

Difficulty Rubric v1.0はChange Surface、Uncertainty、Integration、Verification、Safety Risk、Coordinationを各0～3で採点する。合計Bandは0～3 Routine、4～7 Low、8～11 Medium、12～15 High、16～18 Very Highとする。各Axisの0=なし、1=限定的、2=複数要素または通常の判断、3=広範・高不確実・高リスクまたは複数主体の調整をAnchorとする。Task LeadはREADY前に承認済みTask本文・永続文書だけでPredicted Score、confidence、短い根拠を固定し、迷う場合は最も妥当な値とlow confidenceを記録する。追加調査、差戻し、BLOCKED、公開保留、Requirementsや推奨設定の変更はしない。Engineering AgentはVERIFY後に構造的EvidenceによるRealized Score、予測差、confidenceだけを記録する。負荷はActive作業の10%未満を目標としLifecycle Gateにしない。

Difficulty計算はModel、Reasoning、wall-clock、Tool Call、Retry、Qualityを入力に使わない。Safety Risk=3またはUncertainty=3はRecommendation Safety Floorとして別扱いにできる。Evaluatorは同じRubricを再計算し差をCalibration Warningとして返すが、差戻し、自動修正、BLOCKEDにしない。

Operational RecordはConfiguration、Difficulty、Quality、Performance、Process/Waiting、Execution Friction、Unavailable Reasonを分離する。Model／ReasoningはTask推奨、Product Owner選択、環境確認済み実値および各Sourceを別Fieldにし、取得不能値は推測せずunavailable_reasonとする。Active作業とDependency／Human／Review待ちは混合しない。Quality合格RunだけをPerformance根拠に用いる。Task本文、Prompt、Command/Error、絶対Path、Secret、Credential、Token、Flag、認証情報、実行秘密、非公開思考をRecord／Reportへ含めない。

RecommendationはRetain、Change Candidate、More Data Requiredだけとし、比較Class、Sample数、Quality条件、Configuration、Difficulty Range、指標、根拠、Confidence、制約を示す。同一ClassのQuality合格Sampleが3未満、比較不能、品質Regression、設定不明またはRubric Version不一致ならMore Data Requiredとする。自動的にTask推奨、Agent設定、AGENTS.mdまたはModelを変更しない。

## Roadmap

### Now — Measurement Foundation

読み取り専用Evaluatorの責務、取得可能Metric、Quality／Performance／Process分離Reportを定義する。Benchmarkの入力・期待結果・合否条件を固定し、現行`AGENTS.md`・Model・Reasoning EffortのBaselineを複数回測定する。固定Benchmark、Baseline Report、測定不能項目・代替指標、read-only検証をExit Criteriaとする。

### Next — AGENTS.md Optimization

`AGENTS.md`をRole共通の最上位規則に限定し、詳細手順を必要時だけ読むPlaybookへ分離する。Role・権限境界、Lifecycle、Ownership、Traceability、Approval、Repository境界、Push権限を維持する。規則を重複させず、安全・承認・Ownershipを省略しない。各Instruction Group変更後にBenchmarkを再実行し、同Qualityで改善が確認された場合だけ採用する。

### Next — Model and Reasoning Optimization

Task種別ごとにModelとReasoning Effortを比較する。初期候補はStatus確認=`gpt-5.6-luna / low`、Task Lead／通常Design／通常実装=`gpt-5.6-terra / medium`、複雑Architecture／安全境界実装=`gpt-5.6-sol / high`とする。Model変更とPrompt変更を同時に行わず、品質を下げる速度改善は採用しない。

### Later — K3Ops Integration

K3OpsへRole・Task種別・Model・Reasoning別のWall-clock中央値、Tool Call、Retry、Rework、`BLOCKED`・Review待ち時間、`AGENTS.md` Version比較、Benchmark Trend、Quality Regression Alertを追加する。読み取り専用とし、Task・Agent設定変更、Agent起動、Git操作、非公開思考、Secret・Credential・Token・Flagの表示を行わない。

### Ongoing — Continuous Evaluation

`AGENTS.md`、Playbook、Model／Reasoning推奨、Lifecycle、Branch／worktree／Commit／統合規則、Agent Tool構成の変更時、およびRegression検出時にBenchmarkを再実行する。通常Taskごとには実行しない。

## Performance Report Contract

ReportはConfiguration（AGENTS／Playbook Version、Model、Reasoning Effort、Benchmark、Runs）、Quality（Result、Acceptance Criteria、Build/Test、Rework、Governance Violations）、Performance（Median Wall Time、Time to First Tool、Tool Calls、Retries、Input/Output Tokens、Cost）、Comparison（Baselineとの差分）、Bottlenecks、Recommendation（Adopt／Reject／More Data Required）、Confidenceを分離して記録する。

## Change Governance

結果は判断材料であり自動承認ではない。`AGENTS.md`変更にはProduct Owner明示承認、Model推奨変更にはDesign Agent判断を要する。Quality Regressionは採用せず、不安定な結果は追加Sampleを取得する。Performance改善を理由にSafety、Approval、Traceability、Verificationを省略しない。

## Dependencies

- Current Baselineは`AGENTS.md`最適化より先に実施する。
- K3Ops DashboardはPerformance EvaluatorなしでもTask／Roadmap表示を実装できる。
- K3OpsへのPerformance統合はMetric Contract確定後に実施する。
- 管理Repository移行と本RoadmapのGitHub管理は管理Repository設計・移行Taskに従う。

## References

品質、完全性、Token、Latency、Cost、Tool Call、Turn、Retryを代表Taskで比較し、品質基準を維持した場合だけ効率改善と判断する。

- [OpenAI Model guidance](https://developers.openai.com/api/docs/guides/latest-model)
