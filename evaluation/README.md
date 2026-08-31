# Agent Performance Evaluator

`evaluator.py`は固定された実行記録JSONを読み取り、標準出力へBaseline Reportを返す読み取り専用ツールです。Task、Git、Agent、永続文書、Product CodeおよびAgent設定を変更せず、外部送信、Agent起動、Git操作および通常Task LifecycleのGate化を行いません。

```powershell
python evaluation/evaluator.py --records evaluation/fixtures/sample-records.json
python -m unittest evaluation.test_evaluator
```

入力は秘密情報を含まない固定Snapshotまたは使い捨て環境から作成します。取得できない値は推測せず、Reportの`unavailable`へ理由とともに記録します。

Benchmark定義は`benchmarks.json`、Report Contractは`report_contract.json`、再現可能なBaseline取得手順は`BASELINE.md`にあります。

## Operational Evaluator

`operational.py`は実開発Taskの設定、難易度、品質、Performance、Active作業、Waiting、Execution FrictionをSanitized Recordから観測するread-only Evaluatorです。Task、Git、Agent、文書、Product Codeまたは設定を変更せず、Git操作、Agent起動、外部送信、自動承認・自動最適化を行いません。

Schemaは`operational-schema.json`、合成Fixtureは`fixtures/operational-sample.json`です。Rubric v1.0はChange Surface、Uncertainty、Integration、Verification、Safety Risk、Coordinationを0〜3で採点し、EvaluatorがTotalとBandを再計算します。Model、Reasoning、PerformanceおよびQualityはDifficulty Scoreに使用しません。

Measurement Identityは`benchmark_id`、`snapshot_version`、`prompt_version`および`agents_revision`の4 Fieldを必須とします。最初の3 Fieldは固定Benchmark入力とPrompt条件を識別する80文字以下の非秘密Identifierです。`agents_revision`はRunで使用した`AGENTS.md`内容のGit object IDを40桁または64桁の小文字16進数で記録し、本文、Host固有Pathまたは取得Commandを保存しません。EvaluatorはIdentityを生成せず、Record Producerが提供した値を検証して許可FieldだけからReportへ再構築します。

Experiment Axisは`model_reasoning`または`agents_revision`のどちらか1種類を、異なるBaseline／Candidate値とともに明示します。`model_reasoning`ではMeasurement Identityの4 Fieldを固定し、実Model／Reasoningだけを比較します。`agents_revision`ではBenchmark、Snapshot、Promptおよび実Model／Reasoningを固定し、`agents_revision`だけを比較します。未知Axis、未宣言cohort、固定条件不一致または複数要因変更は性能結論に使わず、`More Data Required`として報告します。

ConfigurationはTask推奨、Product Owner選択、環境確認済み実値をModel／Reasoning／Source付きで別々に記録します。取得不能値は推測せず、Fieldの`unavailable_reason`へ理由を記録します。Performance、WaitingまたはExecution Frictionの全Fieldは必須で、値は非負数または`null`です。`null`では`unavailable_reason`へ同名Fieldの理由を必ず記録し、実測値と理由の併存は拒否します。実測`0`は取得済みの0だけを表し、未取得値の代用には使用しません。Active作業時間とHuman、Dependency、Reviewの各待ち時間を分離し、Tool Error、Retry、再検証、REPORT後手戻りはExecution Frictionへ記録します。

生RecordはGit管理外の`evaluation/raw-records/`だけに置きます。Task本文、Prompt、Command／Error本文、Host固有Path、Secret、Credential、Token、Flag、認証情報、実行秘密、非公開思考を収集・表示・永続化しません。

```powershell
python evaluation/operational.py --records evaluation/fixtures/operational-sample.json
python -m unittest evaluation.test_operational
```

Recommendationは`Retain`、`Change Candidate`、`More Data Required`だけです。各Experiment cohortについて総Run数、品質合格数、Regression数、`wall_time_seconds`、`retries`、`reverification`、`post_report_rework`および`governance_violations`の取得数、測定不能数、理由と中央値をReportへ再構築します。Quality不合格Runは破棄せずRegression数へ残しますが、Performance中央値には含めません。両cohortに品質合格Sampleが3件以上あり、全指標が取得済みで、固定条件、Configuration、RubricおよびCalibrationが比較可能な場合にだけ主指標`wall_time_seconds`の中央値を比較します。Candidate中央値が厳密に小さければ`Change Candidate`、同等以上なら`Retain`です。比較対象不足、各cohortのSample不足、指標不足、品質Regression、設定不明、Rubric不一致、Calibration不一致または比較不能では`More Data Required`を返します。判定は観測上の候補提示であり、因果関係を断定せず、結果からTask、Model、Agent設定、`AGENTS.md`またはLifecycleを自動変更しません。
