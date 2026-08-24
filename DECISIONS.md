# Decisions

## Decision record format

基本設計レベルの変更は、以下の形式で追記する。変更そのものだけでなく、なぜその設計を選んだかを記録する。

```markdown
## ADR-YYYYMMDD-short-title

- Status: Proposed | Accepted | Superseded | Rejected
- Date: YYYY-MM-DD
- Source: Requirement | Architecture | Decision | Problem / Feedback の参照

### Context

判断が必要になった背景、確認済みの事実、制約。

### Decision

採用した設計と変更内容。

### Rationale

この設計を選んだ理由。

### Alternatives considered

検討した選択肢と採用しなかった理由。

### Consequences

利用者、実装、運用、セキュリティ、互換性への影響。

### Verification

判断どおりに機能することを確認する方法または結果。
```

## Current records

このワークスペースの既存構成から、日時・背景・代替案を伴う設計判断として記録できる変更履歴は確認できなかった。既存READMEに記載された現行構成は `docs/ARCHITECTURE.md` に記録する。
