# Task Sentinel運用手順

この文書は、`D-00032`および`T-00066`で定めたTask Sentinel（TS）のHeartbeat運用を、Product OwnerがTS専用チャットから実行するための手順である。TSは`gpt-5.6-luna`／`medium`想定のread-only Roleであり、Task、Git、管理Repositoryの正本、Product RepositoryまたはAgent設定を変更しない。

## Heartbeatの開始

Product OwnerはTS専用チャットへ、次の内容を送る。

```text
Task Sentinelの10分Heartbeatを開始してください。報告はこのチャットへ送ってください。
```

TSは開始を確認し、同じチャットで開始時刻と、10分ごとに行う観測の対象（Task ID、Status、依存、更新時刻、Review情報および必要な候補）を簡潔に報告する。TSは外部送信先や別チャットを追加しない。

各Cycleでは管理Repositoryの`tasks/`からhelperを実行する。通常観測は状態追跡だけを許可し、新規Action予約を作らない。

```powershell
python tools/task_sentinel.py
```

Product Ownerが候補の予約を承認した運用Cycleでは、同じTS専用チャットで明示的に予約を指示し、`--reserve`を使う。

```powershell
python tools/task_sentinel.py --reserve
```

helperのruntime保存先はrepository-relativeな`runtime/task-observer/`に固定される。CLIで別保存先を指定しない。helperのJSON出力は安全なTask ID、Lifecycle判断、許可されたModel／Reasoning、Review Revisionおよび候補種別だけを返し、Task本文を返さない。

## Cycleごとの報告

TSは各Cycleの結果を同じチャットへ、候補がある場合だけ行動可能な粒度で報告する。候補がない正常Cycleは「異常・通知候補なし」と簡潔に報告し、通常状態を繰り返して過剰通知しない。報告にTask本文、Prompt、Command／Error本文、Secret、Credential、Token、Flag、認証情報またはHost固有絶対Pathを含めない。

報告対象は次のとおりである。

- 依存解消済み`READY`のStart候補（Task ID、Taskの推奨Model／Reasoning）。TS Roleはこの候補を根拠に、対象Taskの推奨Model／ReasoningでEngineering Agentを別途自動起動できる。起動中のEngineering Agentは最大2件で、先行候補の`CLAIMED`確認前に次の予約を報告しない。
- `GUI_REVIEW`の報告候補。TSはProduct Ownerへ知らせるだけで、Reviewや修正を予約・実行しない。
- 非GUIの`ACCEPTANCE_REVIEW`のReview候補（Task ID + Task記録の`Review Main Revision`または`Task Review Revision`）。同じ組合せは一度だけ予約する。
- `BLOCKED`、依存不整合、受入れ待ち、45分以上更新されない`CLAIMED`／`IMPLEMENTING`、Revision不足などの通知候補。

`READY`でDependencyが未解消でも、それ自体は異常または通知候補にしない。一方、取得後またはReview状態でDependencyが未解消ならLifecycle不整合として通知する。Review Revisionが不足する場合、TSは現在のmain HEADや別情報から補完せず、担当Engineering Agentへ「Revision不足」として報告する。

## Actionの境界

Start候補は、依存がすべて`DONE`であり、設定値がhelperの許可リストに適合する`READY`だけである。helperは候補と予約情報を返すだけで、Agentを起動しない。TS Roleはhelperの結果を受けて、対象Taskの推奨Model／ReasoningでEngineering Agentを別途自動起動できるが、Taskを直接`CLAIMED`へ遷移させない。起動中は最大2件とし、先行Start予約の`CLAIMED`確認を観測してから次の候補を扱う。

Review候補は、非GUI`ACCEPTANCE_REVIEW`に限る。TSまたはReview AgentはReviewを行えるが、Product Ownerの最終受入れを代行しない。Product Ownerが明示的に受入れた後だけ、新規Engineering Agentが受入れ結果をTaskへ記録し、必要なlocal main統合確認を経て`DONE`へ遷移させる。`GUI_REVIEW`は報告のみである。

helperはTaskファイル、Git、正本、Product RepositoryおよびAgent設定を変更しない。runtime状態への書込みは固定された観測用ディレクトリだけで、排他Lock取得に失敗したCycleは状態変更とAction予約を行わず、Lock unavailableとして報告して停止する。runtime状態は原子的に更新し、自動削除しない。

## 通知の抑制と再通知

`CLAIMED`または`IMPLEMENTING`が45分以上更新されない場合、初回通知を出す。`BLOCKED`、取得後／Review状態の依存不整合および受入れ待ちも初回通知の対象である。同一通知は未解消でも24時間が経過するまで再通知しない。`DONE`は最終Revisionを保存して以後の通常ScanとTask本文再読込から除外する。必要な最終Revisionがない`DONE`は推測せず不足通知とする。

## Heartbeatの停止・再開

Product Ownerは同じTS専用チャットへ次の内容を送る。

```text
Task SentinelのHeartbeatを停止してください。以後のCycleと予約を停止し、停止結果をこのチャットへ報告してください。
```

TSは新しいCycle、候補の予約およびAgent／Review起動を行わず、停止確認だけを同じチャットへ返す。すでに観測用runtime状態へ保存された完了Task、通知抑制および予約情報は自動削除しない。

再開時は、Product Ownerが同じチャットへ次の内容を送る。

```text
Task Sentinelの10分Heartbeatを再開してください。再開確認後、通常観測から開始し、報告はこのチャットへ送ってください。
```

TSは再開を確認してからhelperの通常観測を一度実行し、以後10分Cycleへ戻る。停止中に発生した外部状態を推測して埋めず、再開時に観測できるTask記録とhelper runtime状態だけを根拠に報告する。

## 障害時の安全停止

helperがLockを取得できない、JSON状態を安全に読み書きできない、入力TaskのLifecycle情報が不正で候補を確定できない場合、TSは予約・Agent起動・Review・受入れ・Task遷移を行わない。同じチャットへ障害種別を安全な識別子だけで報告し、Product Ownerの指示があるまでHeartbeatを停止する。エラー本文やHost固有Pathは報告へ転記しない。
