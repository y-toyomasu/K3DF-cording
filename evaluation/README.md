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

ConfigurationはTask推奨、Product Owner選択、環境確認済み実値をModel／Reasoning／Source付きで別々に記録します。取得不能値は推測せず、Fieldの`unavailable_reason`へ理由を記録します。Active作業時間とHuman、Dependency、Reviewの各待ち時間を分離し、Tool Error、Retry、再検証、REPORT後手戻りはExecution Frictionへ記録します。WaitingまたはExecution Frictionを取得できない場合は値を`null`とし、`unavailable_reason`へ同名Fieldの理由を必ず記録します。実測`0`は取得済みの0だけを表し、未取得値の代用には使用しません。

生RecordはGit管理外の`evaluation/raw-records/`だけに置きます。Task本文、Prompt、Command／Error本文、Host固有Path、Secret、Credential、Token、Flag、認証情報、実行秘密、非公開思考を収集・表示・永続化しません。

```powershell
python evaluation/operational.py --records evaluation/fixtures/operational-sample.json
python -m unittest evaluation.test_operational
```

Recommendationは`Retain`、`Change Candidate`、`More Data Required`だけです。同一比較Class・同一Configurationの品質合格Sampleが3件未満、設定不明、Rubric不一致、品質Regression、Calibration不一致、主要Metric不足または比較不能の場合は`More Data Required`を返します。Operational Observationだけで因果関係を断定せず、結果からTask、Model、Agent設定、`AGENTS.md`またはLifecycleを自動変更しません。
