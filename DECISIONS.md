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

T-00006のTool Registryと基本HTTP Tool、T-00007のStrategy Brief、T-00015のCTF Referee／Flag提出Tool／Ground Truth分離、およびT-00017のHTTP Header／Cookie／Typed Body／Run-scoped Credential Storeは実装済みである。T-00017では、実装済みToolの完全Catalog提示を維持し、Credential IDだけをPlannerへ渡し、Header、Cookie、Body、Scope、Target、Budgetおよび秘密情報非永続化の境界をAgent 77件とDashboard 3件のTestで確認した。T-00038〜T-00040で、静的TCP Target Registry、`tcp.scan`、TCP専用Budget、connect-only Executor、共通EvidenceおよびCatalog／Planner統合を実装・検証した。T-00042〜T-00045で、静的SSH Target Registry、固定Host Key／Credential Scope、Memory限定Session Store、`ssh.session.open`／`close`およびinternal-only Synthetic SSH統合検証を実装・検証した。SSHは固定IPv4、許可Port、Host Key照合後のPassword認証およびBudgetへ拘束され、Shell、Filesystem、DatabaseおよびChallengeへのFlag配置は未実装である。

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

`T-00014`で、state schema 2.0のCapability Graph／Flag Objective、Nginx・Scanner Evidence導出、Kimi提案のsuspected制限、旧Schema・不正状態FallbackおよびDashboard読み取り表示を実装した。Defenderコンテナ内Unit Test 15件、Dashboardコンテナ内Fallback確認、および静的GUI表示契約で確認した。GUI ReviewはTaskの確認状態を用いて継続する。
## D-00018: Session-scoped CTF Referee and raw-value Flag verification

- Status: Accepted
- Date: 2026-08-27
- Source: `R-00016`, `R-00019`, `R-00020`, `R-00022`, `R-00023`, `R-00030`〜`R-00036`, `R-00038`, `R-00039`

### Context

CTF Ground TruthをK3ATまたはDefenderが所有すると、攻撃側の推測、Defenderの推定、正解が混在する。Flag ID、原本Artifact、Refereeおよび将来のChallenge配置の対応も未定義である。3個のFlagに対してHMACは複雑すぎるため、独立Referee内での安全な生値比較を採用する。

### Decision

- K3DF RepositoryにDefenderとプロセス、責務、状態を分離した`referee` Serviceを追加する。RefereeはDefender、Dashboard、Webの内部Moduleをimportせず、CTF Ground Truthを独立管理する。
- Runごとの永続状態は`run_id`、受理済みFlag ID／件数、合計`3`、`won`、時刻および値を含まないAudit情報だけとする。Flagは順不同で受理し、重複は件数に加算せず、3個すべてで勝利とする。
- Refereeは各原本を分離したread-only Secret Fileから読み、候補の生値を比較する。Hash、HMAC、DigestまたはKeyは使用しない。constant-timeの生文字列比較は許可する。値はメモリ内だけで扱い、state、log、response、evidence、tracebackまたはauditへ保存しない。
- Flag形式は`K3DF{<43文字のBase64URL文字列>}`とし、32 byteの暗号学的乱数から生成する。番号、配置、Container、HintまたはPathを値へ埋め込まない。
- Secret-free Manifestにはschema version、Flag ID、原本Artifact名、形式、consumer role、暫定Challenge Path、Referee Path、Hint targetおよび配置状態を記録する。初期対応は次のとおりとする。

| Flag ID | Original artifact | Consumer role | Provisional Challenge path | Referee path | Hint target |
| --- | --- | --- | --- | --- | --- |
| `flag-1` | `flag-1.value` | Public Web Challenge | `/run/k3df-flags/flag-1.value` | `/run/referee-flags/flag-1.value` | `flag-2`へのHintを別Fileで持つ |
| `flag-2` | `flag-2.value` | Internal Service Challenge | `/run/k3df-flags/flag-2.value` | `/run/referee-flags/flag-2.value` | なし |
| `flag-3` | `flag-3.value` | Challenge Database初期化 | `/run/k3df-flags/flag-3.value` | `/run/referee-flags/flag-3.value` | なし |

  Challengeのconsumer roleとPathは、K3DFの脆弱性・Service・DB設計後にDesign AgentとProduct Ownerの承認で更新できる。Flag ID、原本名およびReferee Pathは独断で変更しない。
- 未追跡runtime Artifactは次の構造とし、Flagごとに分離する。

```text
runtime/ctf/
├── flag-1/
│   ├── flag-1.value
│   └── flag-1-hint.txt
├── flag-2/
│   └── flag-2.value
├── flag-3/
│   └── flag-3.value
└── run/
    ├── run-id
    └── run-auth.token
```

  Refereeは`.value`だけをread-only mountし、Hintはmountしない。将来のChallengeは対応するFlagだけをread-only mountする。runtimeは追跡せず、stdout、log、CLIへSecretを出さず、暗黙上書きをせず、部分失敗時は既存Artifactを保持し、権限を制限する。Hint本文はprivate inputでCommitせず、Testではsynthetic hintだけを使う。
- Referee APIは`POST /ctf/referee/v1/runs/{run_id}/submissions`、`GET /ctf/referee/v1/runs/{run_id}/status`およびhealthとする。run認証を必須とし、Nginxは定義済みReferee Pathだけをproxyし、runtime、state、Flag Fileを公開しない。
- K3ATの`flag.submit`はLLMから候補値だけを受け取る。Referee URL、run ID、token、timeout、redirectおよびbudgetはSystem固定とし、run IDとtokenはExecutor内に限定しCatalog、Tool Result、Evidence、Snapshot、Event、Brief、Dashboardへ残さない。候補もtransitだけで、Invocation、Action Summary、log、error、Evidenceへ残さない。Tool CatalogはRun開始時から提示し、Capability、DepthまたはFlagでLOCKしない。
- Responseは`accepted`、`duplicate`、`rejected`、`budget_exhausted`だけを安全に返す。accepted／duplicateのFlag ID、accepted count、total、wonは返せるが、候補、原本、token、認証情報、Secret Path、error、Hint、配置またはPathは返さない。

### Rationale

Ground Truthを攻撃側およびDefenderから分離し、少数のFlagを安全かつ単純に判定する。Secret-free Manifestで将来のChallenge実装との対応を追跡しつつ、K3ATへ正解経路を渡さない。

### Alternatives considered

- K3ATまたはDefenderがGround Truthを所有する案は、知識状態を混同するため採用しない。
- HMAC Digest、`verifiers.json`、`verification.key`を用いる案は、3個のFlagには過剰で、鍵・検証データの管理面を増やすため採用しない。
- 全Flagを一つのContainerまたはenvへ集約する案は、分離要件に反するため採用しない。

### Consequences

`T-00015`はReferee、Provisioner、ManifestおよびK3ATの`flag.submit`を実装する。Challenge Containerへのmount、実Hint、Database初期化、Capability Graphとの統合は後続Taskで行う。`ARCHITECTURE.md`には実装・検証前の構成を追加しない。

### Verification

`T-00015`でsecret-free Manifest、32 byte乱数形式のProvisioner、Git管理外runtime、独立Referee、限定Nginx proxy、固定Run認証、constant-time raw-value比較、順不同・重複非加算・3件勝利、原子的なsecret-free stateおよびsubmission budgetを実装した。K3ATにはSystem固定Referee Clientと`flag.submit` Registry sliceを実装し、candidateとTokenをCatalog、Evidence、Snapshot、Event、Dashboardおよびsafe Tool Resultから除外した。K3AT Unit Test 63件、K3DF Unit Test 3件、両Python sourceの構文検査およびReferee image buildで確認した。実Challenge配置、Hint本文、Pi間Secret自動配送および未実装Protocolは実装済みと扱わない。

## D-00019: Run-scoped Credential Store and typed HTTP requests

- Status: Accepted
- Date: 2026-08-27
- Source: `R-00012`, `R-00014`, `R-00016`, `R-00018`, `R-00020`〜`R-00023`, `R-00025`〜`R-00029`, `R-00036`〜`R-00039`, `R-00042`

### Context

現在の`http.request`はMethodとPathだけを扱い、Header、CookieおよびRequest Bodyを拒否する。このためPassword、TokenまたはSession Cookieを発見しても、Login、認証後Request、Form送信またはJSON APIへ利用できない。生CredentialをKimi、通常のTool引数、Evidenceまたは永続Snapshotへ渡すと秘密情報が漏えいする。

### Decision

K3ATへRun-scoped Credential Storeを追加し、HTTP ResponseからSystem側が抽出したCredentialをMemory上だけで保持する。Kimiには生値ではなくCredential IDと安全なMetadataだけを提示し、HTTP Executorは実行直前にCredential IDを解決してHeader、CookieまたはBodyへ挿入する。生値はProcess終了時に失われ、暗号化永続Storeおよび再起動後の復元は対象外とする。Snapshot、Event、Evidence、DashboardにはMetadataだけを保存し、復元不能な過去Metadataを利用可能Credentialとして扱わない。

Credential IDは`CRED-<UUID>`とし、`cookie`、`bearer_token`、`api_key`、`password`、`form_token`、`opaque_secret`を扱う。MetadataはID、種類、安全なLabel、Source Evidence ID、Exact Origin、CookieのName／Domain／Path／Secure／HttpOnly／SameSite／Expiry、取得時刻、最終使用時刻、利用可能・期限切れ・Run終了済み状態を持つ。生値、復元可能なHash、Authorization HeaderまたはCookie Header全体を含めない。

Systemは`Set-Cookie`、JSONの`token`、`access_token`、`refresh_token`、`api_key`、`apikey`、`password`、`secret`、HTML hidden inputの`csrf`、`csrf_token`、`_token`、`authenticity_token`から抽出する。`email`など一般的な個人情報は表示でRedactできてもStoreへ保存しない。Kimiが生値を再入力する`credential.store` Toolは追加しない。将来のHTTP以外のToolもSystem側Evidence Normalizerから同じStoreへ登録できる構造とし、同一Run・Origin・種類・生値はMemory内比較で重複登録しない。

HTTP Executorの生Responseは、(1)受信、(2)Credential抽出・登録、(3)Header／Body Redact、(4)Credential IDを含む安全なTool Result生成、(5)安全なEvidenceとSnapshot永続化、の順に処理する。`Set-Cookie`値、Authorization値、Token、Password、API Keyおよび抽出済みCredentialをBody Previewへ残さない。

`http.request`はHeader、Cookie参照およびTyped Bodyを持ち、Header・Bodyの値を`literal`または`credential_ref`で明示する。Credential参照をPath、QueryまたはURLへ挿入しない。許可Header名はProcess開始時のSystem設定で固定し、件数、名称、値、合計Size、CR／LF／NUL／制御文字を検証する。`Host`、`Content-Length`、`Transfer-Encoding`、`Connection`、`TE`、`Trailer`、`Upgrade`、`Proxy-Authorization`、`Proxy-Connection`、`Forwarded`、`Via`、`X-Forwarded-*`を拒否する。CookieはCookie Credential参照だけから生成し、Authorization、API Key系および秘密Headerのliteralを拒否する。`User-Agent`、`Content-Type`、`Content-Length`はSystemが生成し、Redirectを追跡しない。

Cookie値はStoreだけがMemory上で保持し、KimiはCredential IDだけを指定する。Exact Origin、Domain、Path、Secure、Expiryを検証し、別Origin、Path不一致、期限切れ、HTTP上のSecure Cookieを拒否する。Cookie Header全体をEvidenceまたはlogへ記録せず、Cookie名、Credential ID、適用結果だけを記録できる。

Bodyは`json`、`form`、`text`を対象とし、JSON／Formの各値は`literal`または`credential_ref`とする。JSONは上限付き入れ子を許可する。Binary、Multipart、File Upload、Streaming、Chunked Encoding、CredentialのPath／Query埋込み、およびGET／HEAD Bodyを拒否し、Content-TypeはSystemがBody種別から決める。

固定上限はHeader数32、Header名64文字、Header値1,024文字、Header合計8 KiB、Cookie参照32、Body 16 KiB、JSON深度8、JSON／Form Leaf 128、Credential 128／Run、Credential値4 KiBとする。上限超過では暗黙Evictionせず、登録またはRequestをfail closedとする。

HTTP EvidenceにはMethod、Path、Header名、Body種別・Size・Field名、使用Credential IDと適用箇所、HTTP Status、Content-Type、Redact済みBody Preview、新規Credential ID、種類、安全なScopeだけを記録できる。Header秘密値、Cookie値、Authorization値、Body内Credential値、Token、Password、API Key、復元可能情報は記録しない。Blocked EvidenceとExceptionにも同じRedactionを適用する。

K3AT Dashboardには、Credential ID、種類、安全なScope、Source Evidence ID、状態、取得時刻、最終使用時刻だけを読む専用一覧として表示する。生値、コピー、編集、追加、削除、Request実行、Cookie HeaderまたはAuthorization Headerの表示を提供しない。

### Rationale

Credentialを安全に再利用してLogin・認証後探索へつなげ、同じ参照方式を将来のSSH、Session、Database Toolにも再利用するため。

### Alternatives considered

- 生CredentialをKimiがTool引数へ再入力する案
- Cookie値をAgent Stateへ保存する案
- Credential StoreなしでHeaderとBodyだけを追加する案
- Cookie Jarの自動全送信、平文永続化、Capabilityによる使用Gate、任意Header／Body／Redirectの無制限許可

いずれも秘密情報の露出、安全境界または動的探索の要件に反するため採用しない。

### Consequences

Tool Registry、HTTP Executorおよび永続化前のTool Resultに秘密値解決・安全化境界を追加する。DashboardにMetadataを表示するが、再起動後に過去Credentialを再利用できない。実装と検証は`T-00017`で行う。

### Verification

`T-00017`でRun-scoped Credential Store、`Set-Cookie`／既知JSON Field／既知HTML hidden inputの抽出、重複・上限処理、Metadata、Exact Origin／Cookie Scope、Secret非永続化、Header／Cookie Policy、JSON／Form／Text Body、Credential参照、Response／Blocked／Executor Error Redaction、Evidence、Planner入力、Dashboardおよび既存Method＋Path互換性を実装した。K3AT Agent 77件とDashboard 3件の自動Test、K3AT／Dashboard image Build、Desktop 1280pxおよび狭幅390pxのGUI確認に合格した。GUIではCredential Metadata 2件、既存Run／Finding／Strategy Brief表示、横Overflowなし、操作要素なしおよび合成生値Marker不在を確認した。外部Target、Kimi API Keyおよび実Credentialは使用していない。
`T-00042`〜`T-00045`で、このStoreのavailableな`password` CredentialだけをSSH TargetのExact Originと照合して利用するSession境界を追加した。生PasswordはSession、Tool Result、Evidence、Snapshot、Event、Dashboardまたはlogへ保存しない。

## D-00020: Single-demo-run CTF Referee with a shared validation seed

- Status: Accepted
- Date: 2026-08-30
- Source: `F-00031`, `R-00016`, `R-00019`, `R-00030`〜`R-00035`, `R-00043`, `D-00018`

### Context

`D-00018`で採用したRun IDとRun TokenのFile配送およびread-only bind mountは、教育・展示向けの単一デモRunには運用負荷が大きい。mount元Fileが存在しない場合、Docker Composeが同名Directoryを生成し、K3AT Agentが起動時検証で停止する事象も発生した。Flag原本とCTF Ground Truthの分離は維持しながら、Flag提出の照合だけを簡素化する。

### Decision

- `D-00018`のRun ID／Run Token Fileによる提出認証部分を、単一デモRun向けの共有Seed方式へ置き換える。独立Referee、Flag原本の分離、constant-time比較、順不同、重複非加算、3件受理時の勝利、submission budgetおよびGround Truth分離は維持する。
- K3ATとK3DFは環境変数`K3DF_CTF_DEMO_SEED`を使用し、未指定時は公開既定値`ValidationSeed`を使う。overrideする場合は両環境に同じ値を設定する。SeedはFlag生成、正解経路、Flag配置、Capability判断または実環境のSecurity境界に使用しない。
- Run ID、Run Token、K3ATの`runtime/ctf/run/`依存および対応するPath環境変数とbind mountを廃止する。ProvisionerはFlag 1〜3とFlag 1 Hintだけを生成する。
- Referee APIは`POST /ctf/referee/v1/submissions`、`GET /ctf/referee/v1/status`および`GET /health`とする。submissionとstatusはHeader `X-K3DF-CTF-Demo-Seed`で同じSeedを検証し、`/health`はSeed不要とする。
- Seed Headerは1文字以上128文字以下のvisible ASCIIとする。欠落または不一致は`401`、上限超過または不正形式は`400`とし、照合はconstant-timeで行う。
- Seed値はKimi、Tool Catalog、Tool Result、Evidence、Snapshot、Event、Dashboard、Referee State、Responseまたは通常Logへ出さない。Flag提出候補とFlag原本に対する既存の非露出境界も維持する。
- Flag 1〜3の原本はK3DF RefereeだけがFlagごとに分離されたread-only Fileとして参照する。Flag原本をSeedまたは`.env`へ移さない。
- `ValidationSeed`は公開されたValidation用既定値であり、Secret、Credentialまたは本番認証値として扱わない。`.env`の実FileはGit管理外を維持する。

### Rationale

単一デモRunの起動準備を、両Piで同じ環境変数を設定するだけに縮小する。公開Seedに強い認証を期待せず、CTF Ground TruthとFlag原本を攻撃側から分離する本来の境界へ運用上の注意を集中する。

### Alternatives considered

- Run IDとRun Token Fileの配送を維持する案は、デモ用途に対して準備と障害復旧が複雑なため採用しない。
- Flag原本またはFlag生成SeedをK3ATと共有する案は、正解を攻撃側へ提供し、Flag分離要件に反するため採用しない。
- Seedを安全な認証Credentialとして扱う案は、公開既定値と矛盾するため採用しない。

### Consequences

K3DF Referee、K3ATの`flag.submit` Client、両Compose、Nginx、Provisioner、Testおよび運用文書を更新する。実装はRepository間の契約を固定した小さなTaskへ分割し、実装後に確認済み構成だけを`ARCHITECTURE.md`へ反映する。

### Verification

未実装。`T-00026`〜`T-00029`で実装、統合検証および確認済みArchitecture反映を行う。

## D-00021: Operator-managed per-flag volumes and private-network Referee

- Status: Accepted
- Date: 2026-08-30
- Source: `R-00016`, `R-00017`, `R-00019`, `R-00030`〜`R-00035`, `R-00043`, `R-00044`, `F-00032`, `D-00018`, `D-00020`

### Context

現行K3DFではFlag原本、Run IDおよびRun TokenをHost Fileからbind mountする。Provisioning前にComposeを起動すると、不足しているmount元がroot所有のDirectoryとして生成され、Refereeが通常File検査で異常終了し、再起動を繰り返す。Host上で生成した`0600` FileとContainer内の`nobody`の所有者も一致せず、単純な権限変更ではSecret分離と読取り可能性を同時に満たしにくい。`D-00020`の共有Seedは公開されたDemo連携キーであり、Token認証の代替となるSecurity境界ではない。

### Decision

- `K3DF_CTF_DEMO_SEED`はK3ATとK3DFの単一Demo Runを対応付ける非秘密の検証値として使用する。Header照合は誤接続検出のため維持できるが、認証またはSecurity境界として扱わない。Run Token Secret Fileは廃止し、Referee APIはK3DFのprivate Network境界、限定されたNginx Path、接続先Policyおよび非公開のReferee Container Portで保護する。
- Flag原本は`k3df-ctf-flag-1`、`k3df-ctf-flag-2`、`k3df-ctf-flag-3`の3個のDocker named volumeへ分離する。生成処理だけがread-writeでmountし、Refereeは3個すべてをread-only、各Challenge Consumerは担当する1個だけをread-onlyでmountする。単一Consumerへ複数Flagを渡さず、Docker socketを渡さない。
- Flag 1 HintはFlag原本Volumeと分離して管理し、Refereeへmountしない。Refereeの受理状態はFlag Volumeと分離した`k3df-referee-state` named volumeに保存する。
- 固定IdentityはRefereeをUID/GID `10001:10001`、Flag reader GroupをGID `20001`とする。Flag Fileは`root:20001`、Mode `0440`とし、Refereeと各Consumerには必要な補助Groupと担当Volumeだけを付与する。Referee stateは`10001:10001`、Mode `0700`とする。起動時に通常File、形式、Size、一意性、所有者、Modeおよび書込み不可を検査し、不適合時はfail closedとする。
- Flag生成とLifecycle操作は`K3Defnder-K3Atacker-infra` Repositoryの通常Setupから分離した`operations` Scriptが担う。`ensure`は3 Volumeがすべて未生成の場合だけ暗号学的乱数によるFlagを一組として生成し、正常な既存値を維持する。`status`は値を表示せず、存在、Generation IDおよび検証結果だけを返す。`rotate`は人間の明示確認を必要とし、Hot reloadとして扱わない。
- `rotate`はK3AT停止済みの確認、K3DFのReferee／Flag Consumer停止、対象Volume名と用途の検証、再確認、3 Flag VolumeとReferee stateだけの再作成、3個一括生成、形式・一意性・所有者・Mode検証、成功後のK3DF再起動を順に行う。通常のOS／Compose／Container再起動ではFlagを再生成しない。失敗時はRefereeを起動しない。
- `docker compose down -v`を使用せず、無関係なDatabase、Application Stateまたは他Volumeを作成、削除、変更しない。正常な既存Flagを暗黙に上書きせず、一部だけ存在する状態、Directory、Symlinkまたは特殊Fileは異常として停止する。
- Flag値、共有Seed、Hint本文をCLI引数、標準出力、通常Log、Git、Compose設定またはSecret用途の環境変数へ出さない。Generation ID、対象を限定した操作結果および値を含まない検証結果だけを表示できる。FlagはSeedから生成せず、正解経路、配置またはCapability判断にもSeedを使用しない。
- K3DF Composeは個別Host File bind mountを廃止し、必要なexternal named volumeが存在しない場合は起動前または起動時に明確に失敗させる。Provisioning成功後だけRefereeを起動する。未実装の構成は検証完了まで`ARCHITECTURE.md`へ現行事実として記載しない。

### Rationale

Dockerが管理する分離Volumeと固定Identityにより、Host固有Path、File所有者差異および不足PathのDirectory化を避ける。生成・再生成をInfrastructureの明示的な管理操作へ集約し、通常再起動の安定性、Challenge間のFlag分離および事故時の安全な復旧を両立する。

### Alternatives considered

- Dockerfile Build時にFlagを生成する案は、Image LayerへFlagを残し、Build間で値を固定するため採用しない。
- RefereeのEntryPointでHost mount元を生成する案は、mount解決後では遅く、Refereeへ不要な書込み権限を与えるため採用しない。
- 3個のFlagを単一Volumeへ格納する案は、1個のChallenge侵害で他Flagも読めるため採用しない。
- Host bind Fileを権限調整して維持する案は、Host／Container間の所有者差異と不足Path生成を運用へ残すため採用しない。
- 稼働中にFlagだけを差し替えるHot reload案は、Referee stateおよびK3AT実行中の状態と不整合になるため採用しない。

### Consequences

K3DFはReferee Identity、Flag／state mount、Compose、Network公開、起動時検査およびTestを更新する。`K3Defnder-K3Atacker-infra`はFlag Volumeを管理する独立運用Script、確認手順および安全なTestを追加する。K3ATの共有Seed Client変更は`T-00027`で扱い重複させない。旧Host Artifactを前提とする`T-00028`と旧統合検証を前提とする`T-00029`は、このDecisionに基づく新規Taskで置き換え、公開しない。

### Verification

未実装。K3DFのNamed Volume消費、InfrastructureのFlag Lifecycle操作およびRepository間統合検証を後続Taskで実施し、確認済み構成だけを`ARCHITECTURE.md`へ反映する。

## D-00022: Static bounded TCP Scan

- Status: Accepted
- Date: 2026-08-31
- Source: `R-00016`, `R-00020`〜`R-00023`, `R-00025`, `R-00027`〜`R-00029`, `R-00036`〜`R-00040`, `R-00045`〜`R-00047`, `F-00012`, `D-00016`

### Context

K3ATのTool expansion roadmapにはTCP Scanが含まれるが、任意Host、LAN全体またはManagement Endpointを探索可能にするとTarget Boundaryを越える。Kimi K3へHost、Range、Timeout、ConcurrencyまたはBudgetを直接選ばせず、起動時に固定されたTarget Registryと小さなconnect-only契約へ限定する必要がある。

### Decision

- 設定はJSON形式の環境変数`K3AT_AUTHORIZED_TCP_TARGETS`とする。最大16 Targetを許可し、Target IDはASCII小文字、数字、`-`だけの最大32文字とする。
- 各Targetは一意なTarget ID、ASCII hostnameまたはIPv4、および整数または`start-end`で表す許可Portを持つ。Port設定はTargetごとに最大4096個の一意な許可Portへ展開する。
- HostはRun開始時にIPv4へ解決して固定する。解決失敗、複数IPv4へ解決される曖昧なTarget、loopback、link-local、multicastおよびunspecified addressは起動時に拒否する。
- Tool引数は`target_id`と展開済み整数Port配列だけとし、Range、Host、Timeout、ConcurrencyまたはBudgetを含めない。
- 設定されたTarget IDと許可PortはSystem PolicyとしてTool Catalogへ提示できるが、開放状態または内部Service構成として扱わない。
- `tcp.scan`はCapabilityやFlag状態にかかわらずRun開始時からCatalogへ掲載する。Target未設定時もTool定義を維持し、Network接続前に「許可TCP Targetなし」として拒否する。
- `tcp.scan`は1 Invocationあたり1〜128個の一意なPortへ、最大8並列、1接続500ms、再試行なし、全体12秒Hard TimeoutでTCP connectだけを実行する。TCP専用Budgetは既定256 Port／Runとし、Action Budgetとともに接続開始前にInvocation全体分を確保する。
- 不正入力、重複Port、許可範囲外PortまたはBudget不足では一件も接続しない。connect成功後は直ちにcloseし、Banner取得、Payload送信、TLS Handshakeまたは受信処理を行わない。
- 結果は`open`、`closed`、`timeout`、`unreachable`へ正規化する。生Socket Error、受信Data、DNS内部情報、秘密情報またはHost固有情報をEvidenceへ保存せず、Capabilityを自動確定しない。
- Fallback Plannerは根拠なしにTCP Scanを自動選択せず、既存HTTP既定動作を維持する。
- IPv6、Banner取得、Protocol Probe、UDP、SYN Scan、Service Fingerprint、Credential使用、Proxy、SSH SessionおよびDatabase接続は対象外とする。

### Rationale

静的Registry、事前検証、二重Budgetおよびconnect-only上限により、Kimi K3の動的探索を維持しながらTarget Boundary、Management Network分離、予測可能な実行時間およびEvidence非露出を両立する。

### Alternatives considered

- Kimi K3へ任意HostまたはRangeを渡す案
- LAN全体を自動探索する案
- SYN Scan、Banner取得またはProtocol Probeを同時実装する案
- Capability状態に応じてToolを公開する案
- Target未設定時にTool定義をCatalogから除外する案

いずれもTarget Boundary、Tool Catalog完全性、最小ScopeまたはEvidence安全性に反するため採用しない。

### Consequences

K3ATに静的TCP Target Registry、`tcp.scan` Tool、TCP専用Budget、connect-only Executor、正規化EvidenceおよびPlanner／Catalog統合を追加する。実装は`T-00038`〜`T-00040`、確認済みArchitectureとDecision Verificationの反映は`T-00041`で行う。

### Verification

T-00038〜T-00040で、起動時に固定されるTCP Target Registry、`tcp.scan`、TCP専用Budget、connect-only Executor、正規化Evidenceおよび完全Tool Catalog／Planner統合を実装した。K3AT Agent ImageのBuild、Unit Testおよび隔離したSynthetic TCP ServiceによるDocker統合Testに合格した。検証では、許可Target／Portへのconnect-only動作、未許可Portの接続前拒否、Budget不足時の接続前拒否、Target／Port／Socket Errorの非露出、Capability非自動確定を確認した。外部Network、Kimi API Key、Banner取得、Payload送信、TLS Handshake、受信処理、Credential使用および未実装Protocolは検証対象に含めていない。

## D-00023: Pinned-host-key Challenge SSH sessions

- Status: Accepted
- Superseded By: `D-00026` (2026-09-08)
- Date: 2026-09-01
- Source: `R-00016`, `R-00020`〜`R-00023`, `R-00026`〜`R-00029`, `R-00036`〜`R-00040`, `R-00042`, `R-00048`〜`R-00051`, `F-00012`, `D-00016`, `D-00019`, `D-00022`

### Context

Challenge SSHを動的探索へ追加するには、任意Host、Management SSH、TOFU、Private KeyまたはShell実行を許可せず、既存TCP／HTTP／Credential境界に結び付ける必要がある。生Password、Host Key、Banner、暗号交渉情報および生ErrorをKimi K3や永続状態へ渡さず、安全なSession Metadataだけを保持する。

### Decision

- `K3AT_AUTHORIZED_SSH_TARGETS`はJSON配列とし、最大16 SSH Targetを許可する。各Targetは`target_id`、`tcp_target_id`、`port`、`host_key_sha256`、`credential_source_origins`を持つ。
- `tcp_target_id`は既存TCP Target Registryに存在し、SSH Portは同Targetの許可Portに含まれなければならない。Credential取得元Originは既存HTTP Target Policyに含まれるExact Originだけを許可する。
- Host KeyはSHA-256 fingerprintで固定する。未指定、形式不正、不一致、TOFUまたは自動登録を拒否する。
- Usernameは`[A-Za-z0-9._-]`による1〜64文字のTool literalとする。初期対応の認証は`password` Credential参照だけとし、Private Key、SSH Agent、Keyboard InteractiveおよびGSSAPIは対象外とする。
- Host Key確認後にPassword認証を行う。`ssh.session.open`は最大4 Session、8接続試行／Run、接続3秒、認証5秒、Invocation全体8秒とし、Action BudgetとSSH試行BudgetをNetwork接続前に確保する。
- SSH Sessionは`SESSION-<UUID>`で識別し、live SSH HandleとPasswordをProcess Memory外へ保存しない。Idle Timeoutは5分、自動再接続なし、Process終了時に全Sessionをcloseする。
- 接続失敗は`authentication_failed`、`host_key_mismatch`、`timeout`、`unreachable`、`policy_blocked`へ正規化する。`ssh.session.close`はSession IDだけを受け取り、Credentialや接続先を再指定しない。
- Shell、PTY、SFTP、SCP、Port Forwarding、Agent Forwarding、X11、環境変数送信、SSH CommandまたはLocal Key探索を許可しない。Session確立はCapabilityを自動確定せず、Shell／Filesystem権限も付与しない。
- 全ToolはCapabilityまたはFlag状態に依存せずRun開始時からCatalogへ掲載する。
- Password、Host Key内容、SSH Banner、暗号交渉情報、生Error、解決IPまたは受信DataをKimi K3、Evidence、State、Event、Dashboard、Logまたは永続状態へ公開しない。

### Rationale

既存TCP Target Registry、HTTP Exact Origin PolicyおよびRun-scoped Credential StoreへSSH接続を拘束し、Pinned Host Keyと最小のSession管理を組み合わせることで、Challengeだけに限定した認証済み接続を安全に提供する。

### Alternatives considered

- 任意HostまたはManagement SSHへの接続
- TOFUまたはHost Key自動登録
- Private Key、SSH Agent、Keyboard InteractiveまたはGSSAPI
- Shell、PTY、SFTP、SCP、Forwardingまたは環境変数送信
- SSH接続成功時にCapabilityやFilesystem権限を自動付与する案

いずれもTarget Boundary、Credential非露出または最小権限の要件に反するため採用しない。

### Consequences

K3ATに静的SSH Target Registry、Host Key Policy、Credential Scope、Memory限定Session Store、`ssh.session.open`／`close` ToolおよびSynthetic SSH統合検証を追加する。実装は`T-00042`〜`T-00045`、確認済みArchitectureとDecision Verificationの反映は`T-00046`で行う。

### Verification

`T-00042`〜`T-00045`で、静的SSH Target Registry、固定Host Key／Credential Scope、Run-scoped Session Store、`ssh.session.open`／`close`およびinternal-only Synthetic SSH検証を実装した。Docker Build、全Unit Test、固定Fingerprintを使う実SSH readiness、成功／失敗Password認証、Host Key不一致、Session／試行上限、実TCP後のネゴシエーションTimeout、Session closeおよびShell／Command／SFTP／Forwarding拒否を確認した。実Target、Management SSH、Host OS、Docker socket、Private Key、SSH Agent、Keyboard Interactive、GSSAPI、Shell、Filesystem、SCPまたはForwarding機能は検証対象外かつ現行機能に含まれない。
## D-00024: Common Challenge Target

- Status: `Accepted`
- Fixed Host Key portion: Superseded by `D-00026` (2026-09-08). Other Common Challenge Target boundaries remain in effect.
- Date: `2026-09-06`
- Source: `R-00045`〜`R-00052`、Product Owner承認済みDesign

### Context

HTTP、TCPおよびSSHがProtocol設定ごとにHostを受け取ると、同一Challengeを対象にする保証が弱まり、Tool引数や設定から探索対象を拡張できる余地が生じる。

### Decision

K3ATは起動時に固定した共通Challenge Targetを唯一の探索Hostとして扱う。HTTPは共通IPv4から構成した`http`・80番のBase URLだけを使う。TCPは同一IPv4に対する明示Port Allowlistだけを使い、TCP設定から独立Hostを廃止する。SSHは共通Targetに対応するTCP Target参照、固定Host KeyおよびCredential Scopeだけを使う。`flag.submit`のSystem固定RefereeはChallenge探索Targetの例外とする。

Tool引数およびProtocol設定からHost、IPまたはURLを指定・上書きすることは禁止する。旧TCP設定の独立Hostは非互換として受け付けず、暗黙変換しない。共通Targetまたは必要なProtocol設定が空・不正の場合はNetwork接続前にfail closedとする。Evidence、State、Event、DashboardおよびLogには既存の非露出境界を維持し、新しいHost／URLの生値を追加しない。

### Consequences

- TCP設定とSSH Registryは共通Challenge Targetへ移行する。
- HTTP、TCPおよびSSHのSynthetic統合検証は同一IPv4を使用する。
- 既存のPort、Credential、Host Key、Session、Budgetおよび禁止操作の境界は緩和しない。

### Verification

共通Target Context、TCP Host廃止、SSH Registry適合、Synthetic統合Testおよび確認済みArchitecture反映は後続Taskで検証する。

## D-00025: Isolated Attack Paths for K3DF

- Status: `Accepted`
- Date: `2026-09-07`
- Source: `R-00053`、`D-00016`、`D-00019`、`D-00023`、`D-00024`、Product Owner承認済みDesign

### Decision

- AP-01はNext.js CVE-2025-29927の隔離再現とする。公開PoCは参照元と対象依存版を固定した検証に使用し、通常実行時に外部取得しない。Flag 1専用ConsumerだけがFlag 1 Volumeをread-onlyで参照する。
- AP-02は単一のChallenge DBだけを対象にするCVE-inspired SQLiとし、Flag原本をDBに置かない。成功時に得られる認証素材はRun-scoped Credential Store経由でChallenge SSHへ使う。
- AP-03はSessionに束縛された限定Challenge操作で疑似`admin`、内部Asset、Collectionおよび固定Exfiltrationを表現する。一般的なShellやForwardingは将来も導入しない。
- 新しいSession Action Toolおよび内部Assetは別の設計・実装Taskで扱い、現在の`ssh.session.open`／`close`だけでAP-03成立を主張しない。
- すべての接続先は共通Challenge Targetと既存のPolicy／Budget境界内に限定する。

### Consequences

- 実在CVEの隔離再現とCVE-inspired実装を明確に区別する。
- Capabilityは実行済みEvidenceから観測し、正解経路、Flag値およびFlag配置をK3ATへ事前提供しない。
- AP-01〜AP-03の実装、公開PoC固定検証、Session ActionおよびArchitecture Verificationは後続の独立Taskで扱う。

## D-00026: Simplified Common-target SSH Registry

- Status: `Accepted`
- Date: `2026-09-08`
- Source: `R-00048`〜`R-00052`, `R-00054`, `D-00023`, `D-00024`, Product Owner承認済みDesign

### Context

共通Challenge Target設計の後も、従来のSSH RegistryはTCP Target参照、個別Credential OriginおよびHost Key fingerprintを重複して保持している。SSH接続先を共通Challenge IPv4へ固定した構成では、この重複を取り除き、TCPと同じPort指定の正規化方式へ合わせる必要がある。

### Decision

- `K3AT_AUTHORIZED_SSH_TARGETS`は起動時に一度だけ読むJSON配列とする。各Entryは`target_id`と`ports`だけを持つ。`ports`は整数および`"開始-終了"`形式のRangeを混在でき、起動時に展開して重複のない許可Port集合へ正規化する。
- SSH接続先Hostは常に`K3DF_BASE_URL`から導出した共通Challenge IPv4とする。SSH設定、TCP設定およびTool引数からHost、IPまたはURLを指定・上書きできない。TCP Registryへの参照は持たない。
- 旧`tcp_target_id`、`credential_source_origins`または`host_key_sha256`を含む設定は互換変換せず、起動時にfail closedとする。空配列、Range逆転、範囲外、重複または不正型も接続前に拒否する。
- Credential OriginはCredential MetadataのOriginが`K3DF_BASE_URL`から生成したHTTP Exact Originと一致する場合だけ有効とする。
- Host Keyの設定、固定、照合、TOFUおよび自動登録は行わない。固定された共通Challenge IPv4、許可Port、private Challenge環境、Credential Origin、Action／SSH試行BudgetおよびSession制約を接続境界とする。
- `ssh.session.open`は`target_id`、許可Port集合から選ぶ単一の整数`port`、UsernameおよびPassword Credential参照だけを受け取る。Port Range文字列はTool引数として受け取らない。
- Password、SSH Banner、暗号交渉情報、生Error、解決IPおよび受信Dataは、Kimi K3、Evidence、State、Event、Dashboard、Logまたは永続状態へ公開しない。
- `D-00023`は本DecisionによりSupersededとする。`D-00024`の固定Host Keyに関する部分も本Decisionにより置換する。既存の共通Challenge Target、Budget、Sessionおよび禁止操作の境界は維持する。

### Consequences

- K3ATのSSH Registry、Session予約、SSH Adapter、Tool Schema、README、`.env.example`およびUnit／Synthetic統合Testを新書式へ更新する。
- Host Key mismatch専用の処理、TestおよびEvidenceは削除し、Host Key値を設定、状態または出力へ残さない。
- `ARCHITECTURE.md`は実装・検証後に確認済み構成だけを更新する。事前のArchitecture変更は行わない。

### Verification

T-00056で、Port Range正規化、共通Target Context、Credential Origin、接続前fail-closed、既存SSH制約および秘密非露出を検証する。

## D-00027: AP-01 isolated Next.js authorization-bypass Challenge

- Status: `Accepted`
- Date: `2026-09-08`
- Source: `R-00053`, `D-00024`, `D-00025`, GitHub Advisory `GHSA-f82v-jwr5-mffw`, Product Owner承認済みDesign

### Context

AP-01は実在CVEの隔離再現として、固定手順をK3ATへ与えずに、共通Challenge Target内のTCP調査からHTTP認可迂回およびFlag 1到達を検証可能にする。脆弱な実装、公開面、Flag Consumer、K3AT連携およびEvidence境界を、実装開始前に限定する必要がある。

### Decision

- Challenge Frameworkは自己ホスト型のNext.jsをproduction buildと`next start`で実行する。後続実装Taskは公式GitHub Advisory `GHSA-f82v-jwr5-mffw`の影響範囲内で依存を選定し、package lockとベースイメージのdigestを確定してからBuildする。
- `challenge-next-ap1`は既存Webとは別Containerとし、外部Portを公開しない。Flag 1 Volumeだけをread-onlyでmountし、非rootで実行する。Docker socket、Host bind mount、Referee State、Flag 2／3 Volumeおよび外向き実行権限を持たない。
- Nginxは`/ap1/`だけを`challenge-next-ap1`へproxyする。既存Defender認可はこのRouteへ適用せず、Challenge自身のNext.js Middleware認可だけを対象とする。
- `/ap1/`以外の外部RequestではNginxが`x-middleware-subrequest`を明示的に除去する。`/ap1/`ではCVE再現のため当該Headerを加工せず`challenge-next-ap1`へ転送し、意図的脆弱性をAP-01だけへ閉じ込める。
- Challengeの保護RouteはMiddlewareだけで認可し、通常Requestは拒否する。公開PoCと同じRequest特性を持つ場合だけ認可迂回が成立する。
- K3ATは共通Challenge Targetに対する既存`http.request`だけを使用する。AP-01実装時に`x-middleware-subrequest`をHeader Allowlistへ明示追加するが、Host、Origin、Redirectまたは任意外部Targetの許可は追加しない。
- K3ATが許可済みToolで発見したFlag値の取扱いは`D-00028`に従う。K3DFおよびReferee側のFlag Artifact、Provisioning、read-only Volume、原本非露出および提出検証の保護要件は変更しない。
- CVE-2025-29927の脆弱性範囲、修正版および回避策の唯一の判定基準は公式GitHub Advisory `GHSA-f82v-jwr5-mffw`とする。`DanielHallbro/CVE-2025-29927-Nextjs-Bypass-PoC`は挙動確認の参考資料に留め、公式根拠、依存または実装成果物として扱わない。
- 後続実装Taskは当該Public PoCの参照Commitを固定して内容を読取り確認する。外部Repositoryのclone、実行、vendor、依存導入またはPoC全文の転載は行わない。実装時は最小のBlack-box回帰Testを自作し、参照URLと確認済みCommit IDだけを非秘密の検証記録へ残す。

### Consequences

- AP-01のProduct Code、Compose、Nginx設定、K3AT Header許可設定、Container image、Flag ArtifactおよびArchitecture Verificationは後続の独立Taskで扱う。
- 公開PoCの実行および外部Network利用は本DecisionのSYNCおよびT-00057の対象外とする。

### Verification

T-00057でDecision、RoadmapおよびTask定義の整合を確認する。実装時は固定依存、Container境界、Nginx Route、K3AT連携、`D-00028`に従うFlag取扱い、Flag以外の秘密非露出およびBlack-box回帰Testを後続Taskで検証する。

## D-00028: K3AT-discovered Flag handling

- Status: `Accepted`
- Date: `2026-09-09`
- Source: `D-00025`, `D-00027`, Product Owner承認済みDesign

### Context

K3ATが許可済みToolで実際に発見したFlag値は、探索結果および提出候補として運用上利用できる必要がある。一方、K3DFおよびRefereeが保持するFlag Artifactの原本保護と、K3ATへの事前情報投入または直接読取を禁止する境界は維持する。

### Decision

- K3ATが許可済みToolで発見したFlag値は、K3AT側では秘匿情報として扱わない。
- 発見済みFlag値は、Kimi K3への送信、Tool Result、`flag.submit`候補、Evidence、State、Event、Dashboard、Log、Strategy Briefおよび人間向け出力に含めてよい。発見済みFlag値の検出、Redact、拒否、Run終了時の自動破棄または永続化禁止は要求しない。
- この許容は許可済みToolで実際に発見した値だけに適用する。Flag値、配置または正解経路をK3ATへ事前投入すること、K3ATへFlag ArtifactまたはReferee原本の直接読取権限を与えることは引き続き禁止する。
- K3DFおよびReferee側のFlag Artifact、Provisioning、read-only Volume、原本非露出および提出検証の保護要件は変更しない。

### Consequences

- K3AT実装、Evidence、State、Event、Dashboard、Log、Strategy BriefおよびArchitecture Verificationの変更は後続の独立Taskで扱う。
- `D-00027`のAP-01におけるK3AT側Flag取扱いは本Decisionを参照する。

### Verification

T-00058でDecision、D-00027整合およびRoadmap関連付けを確認する。K3AT側の実装・検証は後続Taskで扱う。

## D-00029: AP-03 session-scoped SSH internal access

- Status: `Accepted`
- Date: `2026-09-09`
- Source: `R-00049`〜`R-00055`, `D-00025`〜`D-00028`, Product Owner承認済みDesign

### Context

AP-03は、接続済みSSH Sessionを起点としてChallenge内部の限定されたラテラルムーブ、疑似`admin`状態、Internal Assetおよび固定Exfiltrationを表現する。任意の接続先、対話操作、転送またはHost権限昇格を許可せず、Sessionに束縛した非対話実行とDocker内部networkのAllowlistで範囲を限定する。

### Decision

- `ssh.session.exec`は有効かつ接続済みの`SESSION-*`とCommandだけを受け取る。Host、Port、Credential、Forwarding設定または別Sessionを受け取らない。Session有効性、Action BudgetおよびExec BudgetはNetworkまたはChannel作成前に確認・消費する。
- Commandは最大4 KiB、1 invocationは最大30秒、stdoutとstderr合計は最大1 MiBとする。Exit Code、`timed_out`および`output_truncated`を機械可読に返し、TimeoutまたはOutput上限時には取得済み部分だけを返す。
- 非対話Exec Channelだけを許可する。PTY、対話入力、SCP、SFTP、Port Forwarding、Agent Forwarding、X11 Forwarding、環境変数送信および再接続は許可しない。
- Tool Result、Evidence、State、Event、DashboardおよびLogには、Session ID、Commandの安全な正規化結果、Exit Code、timeout／truncation状態および取得済みOutputだけを記録できる。`D-00028`に従い許可済みToolで発見したFlag値はK3AT側で非秘匿として扱う。Password、Credential、Token、認証情報、実行秘密およびそれらを含む出力はSystem側がRedactする。
- Docker構成は`ap3-ingress`、`ap3-asset`および`ap3-exfil`を含む内部networkを使用する。各networkは`internal`として隔離し、SSH Challengeは必要なnetworkだけへ接続する。Docker networkの追加・変更、任意の外部宛先または未定義Serviceへの到達を許可しない。
- SSH Challengeは`NET_ADMIN`を持たず、IP forwardingを行わず、Docker socket、Host mount、管理networkまたは外部egressを持たない。Outbound通信はDocker構成のホワイトリストにより、AP-03で明示したInternal AssetおよびExfil ReceiverのService／Portだけに限定する。Internet、Docker host、管理系、未定義Challenge、未定義networkおよびDNSを許可しない。
- Internal Assetは限定されたChallenge内部情報を提供し、Exfil Receiverは固定されたAP-03の到達先だけを受け取る。両Serviceは外部Portを公開しない。AP-03の疑似`admin`はChallenge Container内の状態に限り、Host権限昇格ではない。
- `R-00050`のShell／PTY禁止および`R-00051`の安全なOutcome／Session Metadata限定は、`R-00055`が定義するSession限定非対話ExecとOutput Contractに置換する。Session lifecycle、転送系の禁止、Credential等のRedactionおよび`R-00053`のHost境界は維持する。
- 実装前のため、`ARCHITECTURE.md`を現行構成として更新しない。

### Consequences

- AP-03のK3AT Tool、SSH Adapter、Budget、Evidence／State／Dashboard、K3DF Container、Compose、networkおよびSynthetic統合Testは後続の独立Taskで実装・検証する。
- AP-02のSSH Challenge構成を確定する後続実装Taskが作成された場合、その`DONE`をAP-03実装TaskのDependencyとして分離して記録する。本Decisionおよび文書設計は待たない。

### Verification

T-00059でRequirement、DecisionおよびProduct Roadmapの整合を確認する。実装後に限り、Session／Budget／Output境界、Docker network Allowlist、内部到達範囲、秘密RedactionおよびArchitectureを検証・記録する。
