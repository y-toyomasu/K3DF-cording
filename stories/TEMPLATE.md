# S-xxxxx: Title

- Status: `ACTIVE` | `PAUSED` | `DONE`
- Started: YYYY-MM-DD
- Last Updated: YYYY-MM-DD

## Purpose

## Confirmed Decisions

## Open Questions

## Resume From

## Handoff

## SubAgent Execution Observation

- Requested Model:
- Requested Reasoning:
- Observed Model:
- Observed Reasoning:
- Observation Status:
- Observation Source:
- Unavailable Reason:
- Observation Reference:

> Requested値、親Agent説明、既定設定または推測からObserved値を作らない。V1では公式`SubagentStart` Hook入力のmodelだけをObserved対象とし、Reasoningは未観測とする。Hook未導入、Project未信頼、未読込またはHook失敗は起動を妨げず、最小限のUnavailable Reasonとともに`unavailable`を記録する。子Task Leadは最終報告でObservation Referenceを返す。Session ID、Agent ID、transcript path、Prompt、Command／Error本文、Host固有絶対Path、Secret、Credential、Token、Flag、認証情報または非公開思考は記録しない。

- Status: `not prepared` | `awaiting approval` | `approved` | `delivered` | `delivery unavailable`
- Task Lead Instruction:
- Product Owner Approval:
- Approved At:
- Delivery Requested At:
- Delivery Channel:
- Delivery Agent Model:
- Delivery Agent Reasoning:
- Delivery Result:
- Delivered At:
- Delivery Reference:

日時はISO 8601で記録する。取得不能な値は推測せず`null`とする。

## Completion

- Completed At:
- Result:
