# Agent Performance Evaluator

`evaluator.py`は固定された実行記録JSONを読み取り、標準出力へBaseline Reportを返す読み取り専用ツールです。Task、Git、Agent、永続文書、Product CodeおよびAgent設定を変更せず、外部送信、Agent起動、Git操作および通常Task LifecycleのGate化を行いません。

```powershell
python evaluation/evaluator.py --records evaluation/fixtures/sample-records.json
python -m unittest evaluation.test_evaluator
```

入力は秘密情報を含まない固定Snapshotまたは使い捨て環境から作成します。取得できない値は推測せず、Reportの`unavailable`へ理由とともに記録します。

Benchmark定義は`benchmarks.json`、Report Contractは`report_contract.json`、再現可能なBaseline取得手順は`BASELINE.md`にあります。
