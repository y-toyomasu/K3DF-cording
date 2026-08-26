# Decisions

## Decision record format

基本設計レベルの変更は、以下の形式で追記する。変更そのものだけでなく、なぜその設計を選んだかを記録する。

```markdown
## D-xxxxx: short-title

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

## Accepted decisions

以下はProduct Ownerが承認したDecisionである。実装・検証状態はDecisionごとに異なるため、各Verificationおよび関連Taskを参照する。

## D-00001: Capability Graph as the canonical intrusion model
- Status: Accepted
- Date: 2026-08-24
- Source: `R-00011`, `R-00013`, `R-00025`, `R-00039`
### Context
侵入状態、表示、Evidenceを一貫して扱う必要がある。
### Decision
Capability Graphを侵入状態の正規モデルとし、CTF Stageや侵入深度表示は派生表示とする。
### Rationale
観測結果と表示を分離できる。
### Alternatives considered
CTF Stageを正規状態として持つ案。
### Consequences
EvidenceからCapabilityを導出する実装が必要となる。
### Verification
将来TaskでEvidenceからGraphと派生表示を生成できることを確認する。

## D-00002: Synthetic flags in isolated challenges
- Status: Accepted
- Date: 2026-08-24
- Source: `R-00030`, `R-00031`, `R-00033`
### Context
デモで実ホストの秘密情報を扱わない必要がある。
### Decision
Flagを合成データとして隔離Challenge内へ配置し、実ホストの秘密情報をFlagにしない。
### Rationale
教育用デモの安全境界を保つ。
### Alternatives considered
ホスト上の既存秘密情報を利用する案。
### Consequences
Challenge用の合成データを管理する必要がある。
### Verification
将来TaskでFlagが隔離環境だけに存在することを確認する。

## D-00003: Separate network boundaries
- Status: Accepted
- Date: 2026-08-24
- Source: `R-00027`, `R-00029`
### Context
Challenge実行先と管理面を分離する必要がある。
### Decision
Challenge、Internal、Managementのネットワーク境界を分離する。
### Rationale
探索対象から管理面とホストを隔離する。
### Alternatives considered
単一ネットワークへすべてを配置する案。
### Consequences
ネットワーク定義と通信制御を追加する必要がある。
### Verification
将来TaskでChallenge以外へ接続できないことを確認する。

## D-00004: Independent CTF Referee
- Status: Accepted
- Date: 2026-08-24
- Source: `R-00019`, `R-00034`
### Context
勝利判定とGround Truthを攻撃者の状態から分離する必要がある。
### Decision
Flag検証、取得数、勝利判定およびCTF Ground Truthを独立したCTF Refereeが担う。
### Rationale
攻撃者の推測と正解を混同しない。
### Alternatives considered
K3ATが勝利判定を兼任する案。
### Consequences
Refereeコンポーネントを追加する必要がある。
### Verification
将来Taskで3個の一意なFlagだけを受理して勝利と判定することを確認する。

## D-00005: Extensible protocol adapters
- Status: Accepted
- Date: 2026-08-24
- Source: `R-00012`, `R-00018`
### Context
HTTP以外の接続方式を扱う必要がある。
### Decision
HTTP、SSH、Database、Filesystemなどの接続方式をProtocol AdapterまたはTool Adapterとして拡張する。
### Rationale
脆弱性と接続方式を固定しない。
### Alternatives considered
HTTP専用のまま拡張しない案。
### Consequences
AdapterごとのPolicy検証が必要となる。
### Verification
将来Taskで少なくとも複数方式を安全境界内で実行できることを確認する。

## D-00006: Exclude Raspberry Pi hosts
- Status: Accepted
- Date: 2026-08-24
- Source: `R-00027`
### Context
K3ATから見た接続先IPはK3DF Raspberry PiのIPであるため、Challenge公開Endpointとホスト管理面を区別する必要がある。
### Decision
envで許可されたRaspberry Pi上のChallenge公開Endpoint、および許可済みSessionを経由して到達するChallenge Internal Serviceを対象とする。Raspberry PiのHost OS Service、SSHなどのManagement Serviceおよび管理Port、Management Network、Challenge外のLAN、Host filesystem、Docker socketを対象外とし、最深到達点を隔離された内部Challenge Serviceとする。
### Rationale
Challenge Endpointを必要な探索対象として維持しながら、ホスト管理面と管理経路を保護する。
### Alternatives considered
ホストまで対象に含める案。
### Consequences
Target PolicyでChallenge Endpoint、許可済みSessionおよび除外するHost OS・管理面・ファイルシステム・Docker socketを明示する必要がある。
### Verification
将来Taskで、envで許可されたChallenge公開Endpointは利用できる一方、Host OS Service、Management Service、管理Port、Host filesystemおよびDocker socketへの操作が拒否されることを確認する。

## D-00007: Dynamic strategy over fixed scenarios
- Status: Accepted
- Date: 2026-08-24
- Source: `R-00014`, `R-00018`, `R-00021`
### Context
固定シナリオはEvidenceに応じた探索を表現できない。
### Decision
固定Scenarioではなく、固定GoalとKimi K3による動的Strategyを採用する。
### Rationale
探索を現在のEvidenceへ適応させる。
### Alternatives considered
固定攻撃Scenarioを事前定義する案。
### Consequences
Strategyの監査記録が必要となる。
### Verification
`T-00006` でGoal、Evidence、現在状態と完全なTool CatalogからTool Invocation候補を生成するPlanner入力を実装し、`T-00007` で前回の検証済みStrategy Briefを分離入力として追加した。固定正解経路を持たないFallbackもRegistryと現在状態から最小限のInvocation/Brief候補を生成する。k3-agentとDashboardのBuild、Agent 59件とDashboard 2件のTest成功で確認した。

## D-00008: Strategy Brief without authority
- Status: Accepted
- Date: 2026-08-24
- Source: `R-00015`, `R-00016`
### Context
Kimi K3の探索計画とシステム権限を分離する必要がある。
### Decision
Kimi K3が生成・更新するものを、権限を持つSystem PromptではなくStrategy Briefとする。
### Rationale
System PolicyとTool権限を不変に保つ。
### Alternatives considered
Kimi K3がSystem Promptを更新する案。
### Consequences
Strategy Briefを非権限情報として保存する必要がある。
### Verification
`T-00007` で、5分類を持つStrategy Briefの候補をSystem側で厳格に検証し、revision/updated_atをSystemだけが付与する実装を確認した。BriefはPlannerへ非権限状態として分離提示され、不正候補でもTarget、Tool Catalog、Policy、Budgetおよびlast-known-valid Briefが変化しない。Snapshot/Event/Dashboardの読み取り専用統合を、k3-agentとDashboardのBuild、Agent 59件とDashboard 2件のTest成功で確認した。

## D-00009: Hidden solution paths
- Status: Accepted
- Date: 2026-08-24
- Source: `R-00017`, `R-00031`, `R-00040`
### Context
探索の正解をK3ATへ事前提供しない必要がある。
### Decision
Challengeの正解経路とFlag配置をK3ATへ渡さず、Evidenceから探索させる。
### Rationale
探索の教育的価値を維持する。
### Alternatives considered
完全な経路マップをK3ATへ渡す案。
### Consequences
Ground Truthの保管先をK3ATから分離する必要がある。
### Verification
将来TaskでK3AT設定に正解情報が含まれないことを確認する。

## D-00010: Separate knowledge states
- Status: Accepted
- Date: 2026-08-24
- Source: `R-00019`
### Context
攻撃者、Defender、Refereeの認識を分離する必要がある。
### Decision
Attacker Belief、Defender Estimate、CTF Ground Truthを分離する。
### Rationale
各主体の知識を混同しない。
### Alternatives considered
単一の共有状態を利用する案。
### Consequences
状態モデルとアクセス境界を定義する必要がある。
### Verification
将来Taskで各状態が独立して保存・参照されることを確認する。

## D-00011: Tool Registry
- Status: Accepted
- Date: 2026-08-24
- Source: `R-00020`, `R-00022`, `R-00025`
### Context
Tool定義、Policy、実行、Evidenceを一貫して扱う必要がある。
### Decision
Tool Specification、Policy Validator、Executor、Evidence NormalizerからなるTool Registry方式を採用する。
### Rationale
実行境界と正規化を明示できる。
### Alternatives considered
各Toolが独自の非構造化実装を持つ案。
### Consequences
Registryインターフェースを実装する必要がある。
### Verification
`T-00006` で、不変Tool Registryと `http.request` を実装した。Tool Specification、Policy Validator、Executor、Evidence Normalizerの4要素、重複Tool名拒否、Network処理前のTool名・引数・Target・Method・Budget検証、実行済み/Blockedを区別する共通Evidenceを、k3-agent Buildと49件のUnit Test成功で確認した。現時点で実装済みのToolはHTTPだけである。

## D-00012: Static environment policy
- Status: Accepted
- Date: 2026-08-24
- Source: `R-00023`, `R-00028`, `R-00029`
### Context
実行中のTarget拡大を防ぐ必要がある。
### Decision
Toolの接続先と許可範囲をenvで静的に定義し、Run中は変更不可とする。
### Rationale
安全境界をSystem側に保持する。
### Alternatives considered
Kimi K3がRun中にTarget設定を変更する案。
### Consequences
envの許可リストとValidatorが必要となる。
### Verification
`T-00003` で、Process開始時にenvから生成する不変Target Policyを実装した。`K3DF_BASE_URL` fallback、許可集合との包含検証、scheme・host・port・Origin境界、設定不正時のfail-closed、Local PolicyとExecutorによる同一Policy共有を、32件のUnit Test成功とBuildで確認した。

## D-00013: Three unordered flags
- Status: Accepted
- Date: 2026-08-24
- Source: `R-00030`, `R-00032`, `R-00034`, `R-00035`
### Context
勝利条件とHintの役割を定義する必要がある。
### Decision
3個のFlag取得を勝利条件とし、Flag 1にFlag 2へのHintを含める。Flagの提出順は強制しない。
### Rationale
探索支援と経路の自由度を両立する。
### Alternatives considered
Flag提出順を固定する案。
### Consequences
Flag 2からFlag 3へのHintは未決定のため本Decisionに含めない。
### Verification
将来TaskでRefereeが順不同の3個の一意なFlagを受理することを確認する。

## D-00014: All tools visible from run start
- Status: Accepted
- Date: 2026-08-24
- Source: `R-00036`, `R-00037`, `R-00038`, `R-00039`, `F-00003`
### Context
Tool公開をCapabilityに連動させると、現実の実行条件よりゲーム的な進行管理になる。
### Decision
ToolはRun開始時からすべてKimi K3へ提示し、CapabilityによるLOCKED/AVAILABLE方式は採用しない。Capability Graphは実行権限ではなくEvidenceから導出する観測モデルとする。
### Rationale
Tool可否をCredential、Session、接続状態および安全Policyの具体的条件で判断する。
### Alternatives considered
Capabilityに応じてToolを段階公開する案は、`F-00003` によりゲーム的で現実の環境に即していないため不採用とした。
### Consequences
Tool Catalogは開始時に公開し、Policy Validatorは具体的実行条件を検証する必要がある。
### Verification
`T-00006` で、現行Registryの完全なTool CatalogをRun開始時からPlannerへ提示し、Capability、ATT&CK Tactic、自己申告Risk、発見状態および旧Authorization集合を実行Gateに使用しないことを確認した。実行可否は静的Target、HTTP Method、引数Schema、Action Budgetで検証し、CapabilityはHTTP Response Evidenceからだけ導出する。k3-agent Buildと49件のUnit Testが成功した。

## D-00015: Expose K3AT dashboard to the private LAN

- Status: Accepted
- Date: 2026-08-24
- Source: `F-00011`, `A-00004`, `R-00010`

### Context

K3AT Dashboardはコンテナ内では `0.0.0.0:8888` で待ち受けているが、現在のCompose構成ではホスト側の `127.0.0.1:8889` だけに公開されている。標準構成ではK3ATとK3DFをprivate LAN上の別々のRaspberry Piで実行する。デモ端末からK3AT Dashboardを確認するため、K3AT Raspberry Piのprivate LAN InterfaceからDashboardへアクセスできる必要がある。

### Decision

K3AT Dashboardのホスト側Portを `0.0.0.0:8888` へ公開し、コンテナ側のPort 8888へ転送する。DashboardはK3ATホストの全IPv4インターフェースで待ち受ける。Dashboardは読み取り専用のままとし、調査の開始・停止・制御機能、API Credential、状態への書込み権限を追加しない。利用対象は所有または明示的に許可されたprivate LANに限定し、インターネットへ公開しない。

### Rationale

Raspberry Pi本体でブラウザを操作せず、private LAN上のデモ端末からK3ATの実行状態と結果を確認できるようにするため。ホスト側とコンテナ側のPortを8888へ統一し、接続先と運用設定を単純にする。

### Alternatives considered

`127.0.0.1` 限定を維持する案は、private LAN上の別端末から閲覧できないため採用しない。ホスト側Port 8889を維持する案は、Product Ownerがホスト側とコンテナ側のPortを8888へ統一すると決定したため採用しない。認証またはTLSを同時に追加する案は、今回のprivate LANデモに必要な変更範囲を超えるため採用しない。必要になった場合は別Taskとして設計する。

### Consequences

K3ATホストのPort 8888へ到達できる端末は、認証なしでDashboardを閲覧できる。運用者はprivate LANおよびホストFirewallで到達範囲を制限する必要がある。標準の2台のRaspberry Pi構成では、K3DFとK3ATがそれぞれのホストでPort 8888を使用できる。K3DF DashboardとK3AT Dashboardを同一ホストで起動する構成ではPort 8888が競合するため、標準構成の対象外とする。

### Verification

Compose設定が `0.0.0.0:8888:8888` を公開することを確認する。K3AT Raspberry Pi上でDashboardを起動し、同一private LAN上の別端末から `http://<K3AT-Pi-private-IP>:8888` を表示できることを確認する。Dashboardの状態Volumeが読み取り専用であり、Credentialまたは調査制御機能を持たないことを確認する。

## D-00016: Tool expansion roadmap and session-scoped boundaries

- Status: Accepted
- Date: 2026-08-25
- Source: `R-00012`, `R-00016`, `R-00020`, `R-00023`, `R-00026`〜`R-00029`, `R-00036`〜`R-00038`, `F-00012`

### Context

K3ATをHTTPだけの探索から複数Protocol、Credential、SessionおよびCTFへ拡張する際、実装順序と攻撃経路を混同せず、Raspberry Piの管理面を対象外に保つ必要がある。

### Decision

Tool拡張は次のロードマップで進める。

1. T-00006: Tool Registryと基本HTTP Tool
2. T-00007: Strategy Brief
3. CTF Referee、Flag提出Tool、Ground Truth分離
4. HTTP Header、Cookie、Request Body、Credential Store
5. env許可範囲内のTCP Scan
6. Challenge用SSH接続とSession管理
7. Session内ShellとFilesystem list/read
8. Challenge Database接続
9. Flag 1〜3とChallenge Containerの接続
10. K3DFによる侵入深度推定・表示との統合

SSHはenvで許可されたChallenge SSHだけを対象とし、Raspberry PiのManagement SSHを対象にしない。Shellは許可済みChallenge Session内だけで実行し、K3AT ContainerまたはRaspberry Pi HostのShellを提供しない。TCP Scanはenvで許可されたHostとPort Rangeだけを対象とし、LAN全体を探索しない。Database接続はChallenge Databaseまたは許可済みSession経由に限定する。Filesystem操作はChallenge Session内のlist/readから開始し、Host filesystemとDocker socketを対象にしない。

Credentialは将来Credential Storeで管理し、LLMには参照IDを提示する。任意Header、Cookie、Request BodyはValidatorを経由し、Host上書き、CRLF、Proxy指定、境界外Originなどを拒否する。

実装済みToolはすべてRun開始時から提示する。ロードマップの実装順序を、固定Scenario、Flag順序、攻撃経路またはCapabilityによるTool解放として使用しない。

### Rationale

将来のToolとSessionを段階的に実装しながら、各段階で具体的なTarget、Protocol、Credential、Session、Budget境界を検証できるようにし、実装順序をゲーム内権限へ転用しないため。

### Alternatives considered

Capabilityに応じてToolを段階公開する案は、`F-00003` と `F-00012` に反して実行条件とゲーム進行を混同するため採用しない。Raspberry Pi HostまたはManagement NetworkをChallenge対象に含める案は、安全境界を破るため採用しない。全Toolを一括実装する案は、各ProtocolとSession境界を個別に検証できないため採用しない。

### Consequences

各ロードマップ項目は別Taskで実装・検証し、実装済み範囲と将来範囲を区別して記録する必要がある。新しいToolはRegistry、Validator、Executor、Evidence Normalizerを持ち、System管理のTarget、Protocol、Credential、Session、Budget境界を維持しなければならない。

### Verification

T-00006のTool Registryと基本HTTP Tool、およびT-00007のStrategy Briefは実装済みである。T-00007では、BriefがRegistry、Target、Policy、Budgetを変更せず、実装済みToolの完全Catalog提示を維持することをAgent 59件とDashboard 2件のTestで確認した。CTF、Credential、TCP、SSH、Shell、Filesystem、Database、Flag、K3DF統合は未実装であり、各将来Taskで本Decisionの境界を検証する。

## D-00017: Generic capability depth ontology and separate flag objectives

- Status: Accepted
- Date: 2026-08-27
- Source: `R-00013`, `R-00019`, `R-00025`, `R-00030`, `R-00034`, `R-00035`, `R-00039`

### Context

現在のK3DFは推定Capabilityを平坦な一覧として保持しており、侵入の深さ、Capability間の関係、Evidenceとの対応、およびFlagごとの達成状況を一貫して表示できない。将来のToolやChallenge機能が未実装でも、利用者が全体像と現在位置を確認できる表示が必要である。

### Decision

Capability Graphを、特定Challengeの固定攻略経路ではない汎用的なCapability Ontologyとして定義する。Graph全体を初期状態から表示し、各Nodeは`not_observed`、`suspected`、`confirmed`の状態を持つ。

侵入深度は最も深いCapabilityのEvidence状態から派生させ、正規状態として別管理しない。Confirmed DepthとPossible Depthを区別する。深度帯は分類であり、全Nodeの順番どおりの達成を要求しない。深いCapabilityのEvidenceを受けても、前段Nodeを自動的に`confirmed`へ変更しない。

| Depth | 表示名 | 意味 |
| ---: | --- | --- |
| 0 | No Confirmed Intrusion | 確認済みCapabilityがない |
| 1 | Public Endpoint Reached | Challenge公開Endpointへの到達を観測 |
| 2 | Service / Protocol Discovered | ServiceまたはProtocolを発見 |
| 3 | Exploit Attempt Observed | Exploit試行を観測 |
| 4 | Exploit Success Confirmed | 脆弱性利用の成功を確認 |
| 5 | Application Data Access | Application Dataへのアクセスを確認 |
| 6 | Credential Acquired | Credential取得を観測 |
| 7 | Challenge Session Established | Challenge内Session確立を確認 |
| 8 | Command Execution / Filesystem Read | Command実行またはChallenge filesystem読取りを確認 |
| 9 | Internal Service Reached | Challenge Internal Serviceへの到達を確認 |
| 10 | Challenge Database Access | Challenge Databaseへのアクセスを確認 |

Flag 1、Flag 2、Flag 3は侵入深度とは別のObjectiveとして扱い、取得順を強制しない。各Flagは取得状態`not_observed`、`suspected`、`confirmed`と、提出状態`not_submitted`、`detected`、`accepted`、`rejected`を持つ。Flag値、配置場所、Hint、Credentialおよび正解経路はCapability Graph、Dashboard、ログへ表示しない。

Capability Graphは観測モデルであり、Toolの公開、実行許可、LOCKED状態または攻略順の制御には使用しない。

### Rationale

未実装の深い侵入段階も初期状態から可視化しつつ、Evidenceに基づくDefender EstimateとCTF Ground Truthを混同せず、将来のEvidence Producerを安全に追加できるようにする。

### Alternatives considered

- 現在Evidenceを生成できる浅いDepthだけを表示する案
- 特定Challengeの固定攻略経路をGraphとして事前登録する案
- Flag取得を侵入深度へ組み込む案
- Kimiの推測だけでCapabilityを`confirmed`にする案

### Consequences

- 将来のCapability Nodeも初期状態から`not_observed`として表示される。
- 将来Toolは、新しいGraphを作り直すのではなく正規化EvidenceのProducerを追加する。
- Dashboard表示はDefender Estimateであり、CTF Ground Truthとは区別する。
- Flagの正式な受理結果は将来のCTF Refereeが所有する。
- KimiによるCapability提案はEvidenceを参照した`SUSPECTED`相当までとし、`CONFIRMED`はシステムがEvidenceから導出する。
- 実装と検証は`T-00014`で行う。

### Verification

`T-00014`で、状態モデル、Evidence導出、永続化、Dashboard、Flag 1〜3表示、互換読込みおよびGUI Reviewを確認する。

`ARCHITECTURE.md`には、このTaskの検証前に未実装構成を現行事実として追加しない。
