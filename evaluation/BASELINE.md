# Baseline取得手順

1. `benchmarks.json`と同じPrompt Version、Model、Reasoning Effortを使い、秘密情報を含まない固定Snapshotまたは使い捨て環境を準備する。
2. Benchmarkごとに3回以上実行し、実行ごとの品質合否と取得可能な実行記録だけを`records.json`へ保存する。実プロジェクトのTask、Git、Agent、文書、Product Code、設定は変更しない。
3. `python evaluation/evaluator.py --records records.json`を実行し、標準出力のReportを判断材料として保管する。Evaluatorは外部送信、Git操作、Agent起動、Status変更、自動承認を行わない。
4. 品質条件を満たすRunだけの中央値とばらつきを比較する。Token、Cost、非公開思考など取得不能な項目は推測せず、`unavailable`の理由を比較結果に含める。
5. 単一Runを性能改善の結論にしない。品質Regression、Safety、Approval、TraceabilityまたはVerificationの低下がある比較結果は採用しない。
