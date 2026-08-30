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

T-00006のTool Registryと基本HTTP Tool、T-00007のStrategy Brief、T-00015のCTF Referee／Flag提出Tool／Ground Truth分離、およびT-00017のHTTP Header／Cookie／Typed Body／Run-scoped Credential Storeは実装済みである。T-00017では、実装済みToolの完全Catalog提示を維持し、Credential IDだけをPlannerへ渡し、Header、Cookie、Body、Scope、Target、Budgetおよび秘密情報非永続化の境界をAgent 77件とDashboard 3件のTestで確認した。TCP、SSH、Shell、Filesystem、Database、ChallengeへのFlag配置およびK3DF侵入深度統合は未実装であり、各将来Taskで本Decisionの境界を検証する。

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
