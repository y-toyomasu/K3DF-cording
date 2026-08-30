# Product

## Scope

このワークスペースには、次の独立したGitリポジトリがある。

| Repository | 確認できる目的 |
| --- | --- |
| `K3DF/` | Webアプリケーションの脆弱性を安全な検証環境で学ぶためのK3 Defender Lab。意図的にSQLインジェクション脆弱性を含むFlaskアプリケーション、スキャナー、防御状況ダッシュボードを含む。 |
| `K3AT/` | K3 Defender Labの攻撃側コンポーネント。Kimi K3を用いるが、許可済みの対象への制約付きセキュリティテストエージェントとして動作する。 |
| `K3Defnder-K3Atacker-infra/` | Raspberry Pi上でK3DF/K3AT環境を初期セットアップするスクリプト群。 |

## Safety and intended use

- K3DFおよびK3ATは、所有者が所有する、または明示的な許可を得た学習・検証環境で使用する。
- K3DFは意図的に脆弱なアプリケーションを含むため、インターネット公開および本番利用をしない。
- K3ATは、設定した許可対象以外への操作を行わない制約を持つ。

## Verified user-facing capabilities

### K3DF

- Flaskアプリケーション、Nginx、Defender、ダッシュボードをDocker Composeで起動できる。
- `/health` と顧客情報の例を提供する。
- スキャナーが `/customer` に対する通常リクエストと検証用リクエストの応答差分をJSONで出力する。
- ダッシュボードがWebの到達性、Nginxアクセス、エラー、疑わしいリクエスト、Defenderの保存状態を表示する。
- Defenderがアクセスログ、スキャナー結果、Defender Action結果をEvidenceとして扱い、ローカルポリシーで許可された防御アクションを実行する。

### K3AT

- 許可されたK3DFラボ対象への、証拠に基づくバッチ型の検証シナリオを実行する。
- ローカルポリシーにより、対象Origin、HTTPメソッド、リクエスト量、能力およびパラメーター変化を検証する。
- 実行状態とイベントを永続化し、独立した読み取り専用ダッシュボードで表示する。

## Unknown or not specified

既存READMEと構成ファイルから確認できる現行機能と、この文書の「Approved product requirements」に記録したProduct Owner承認済みの将来要件は区別する。次の事項は未決定であり、本書では確定しない。

- Flag 2からFlag 3へのHint
- 具体的なChallenge内容
- デモの時間制限
- 探索停滞時のHint方式

## Approved product requirements

以下はProduct Ownerが承認した将来のCTFデモ要件であり、現行実装済み機能を表すものではない。

- `R-00008`: 主目的を教育・展示向けのCTFデモとする。
- `R-00009`: 主な利用者を、Dockerと基本的なWeb技術を扱えるセキュリティ学習者・開発者とする。
- `R-00010`: 標準構成を、private LANで接続した2台のRaspberry PiによるK3AT/K3DF分離構成とする。各Piでは都度Git pullして実行・テストする。
- `R-00011`: 攻撃側の目的を、Flagの発見と、より深いCapabilityおよび内部Assetへの到達とする。
- `R-00012`: SQL Injectionだけに限定せず、複数の脆弱性および接続方式を扱える構成へ拡張する。
- `R-00013`: 防御側は、攻撃者がどこまで侵入したかをEvidenceに基づいて推定・表示する。
- `R-00014`: K3ATは固定された攻撃シナリオではなく、Goal、Evidence、現在状態からKimi K3が探索シナリオを動的生成する。
- `R-00015`: Kimi K3はStrategy Briefを生成・更新し、仮説、未知点、失敗した方向、次の調査優先度を管理する。
- `R-00016`: Kimi K3はSystem Policy、Target Boundary、Tool権限、Action Budgetを変更できない。
- `R-00017`: Challengeの想定経路、Flag位置、Capability Graphの正解をK3ATへ事前提供しない。
- `R-00018`: K3ATはEvidenceに基づき、脆弱性、接続方式、侵入経路を動的に選択できる。
- `R-00019`: Attacker Belief、Defender Estimate、CTF Ground Truthを独立した状態として扱う。
- `R-00020`: K3ATは利用可能なTool Catalogを構造化してKimi K3へ提示する。
- `R-00021`: Kimi K3は固定Scenarioではなく、Toolと引数をEvidenceに基づいて選択する。
- `R-00022`: 各ToolはTool Specification、Policy Validator、Executor、Evidence Normalizerを持つ。
- `R-00023`: Toolの種類、実行対象、安全境界、Budgetはシステム側で定義し、Kimi K3は変更できない。
- `R-00025`: Toolの実行結果を共通Evidence形式へ正規化し、Capability Graphへ反映する。
- `R-00026`: 発見したCredentialはCredential Storeで管理し、Tool呼出しでは参照IDを使用できる。
- `R-00027`: Toolの実行先を、envで登録されたRaspberry Pi上のChallenge公開Endpoint、および許可済みSessionを経由して到達するChallenge Internal Serviceへ限定する。Raspberry PiのHost OS Service、SSHなどのManagement Serviceおよび管理Port、Management Network、Challenge外のLAN、Host filesystem、Docker socketを対象外とする。
- `R-00028`: Toolの接続先はK3ATコンテナのenv設定で静的に定義し、Run中は変更できない。
- `R-00029`: Toolはenvで許可されたHost、Origin、PortまたはPort Rangeだけを対象にでき、任意の外部Targetへ接続できない。
- `R-00030`: Kimi K3へ、3個の一意なFlag取得が勝利条件であることとFlag形式を提示する。
- `R-00031`: Flagの値、配置場所および正解経路はK3ATへ事前提供しない。
- `R-00032`: Flag 1にはFlag 2の探索につながるHintを含める。
- `R-00033`: Challenge側のFlagはServiceおよびContainer単位で分離し、単一のChallenge Containerまたはenvへ集約しない。独立CTF Refereeは検証目的に限り、Flagごとに分離されたread-only Secret Fileとして3個の生値を参照できる。Refereeは生値をenv、永続状態、ログ、ResponseまたはEvidenceへ保存しない。
- `R-00034`: CTF RefereeがFlagを検証し、3個の一意なFlagを受理した時点で勝利とする。
- `R-00035`: Flagは順不同で提出可能とし、Hintは探索支援であって経路強制には使用しない。
- `R-00036`: 許可されたToolはRun開始時からすべてKimi K3へ提示する。
- `R-00037`: Toolの公開および実行可否をCapability Graphの進行状態に依存させない。
- `R-00038`: Tool実行条件はTarget、Credential、Session、Protocol、Budgetなどの具体的な実行条件で検証する。
- `R-00039`: CapabilityはTool権限ではなく、実行結果のEvidenceから導出される観測結果として扱う。
- `R-00040`: Kimi K3には内部Service構成を事前提供せず、envで許可された範囲内を探索させる。
- `R-00041`: K3AT Dashboardは、Strategy BriefをJSON構造の解読を必要としない、人間が読みやすい構造化表示で提供する。5分類、revision、更新時刻、Evidence IDおよびTool名の追跡可能性を維持し、読み取り専用性と秘密情報非表示を維持する。
- `R-00042`: K3ATは、HTTP Responseから発見したCredential、Session Cookieおよび認証用TokenをRun-scoped Credential Storeで管理し、生値をKimi K3または永続状態へ公開せず、Credential参照IDを使ってHeader、CookieまたはRequest Bodyへ適用し、Login、Form送信、JSON APIおよび認証後Endpointを探索できる。
- `R-00043`: K3ATとK3DFのCTF Flag提出連携は、共通の環境変数`K3DF_CTF_DEMO_SEED`を使用する。公開既定値は`ValidationSeed`とし、両環境で同じ値を使用する。SeedはFlag生成、正解経路、Flag配置またはCapability判断に使用しない。
- `R-00044`: Flag 1〜3の原本はFlagごとに分離されたDocker named volumeで管理する。生成処理だけが各Volumeをread-writeで使用し、Refereeは3個すべてをread-only、各Challenge Consumerは担当する1個だけをread-onlyで使用する。Flag生成、既存値を維持する初回確認、値を表示しない状態確認、および人間が明示実行する3個一括再生成は`K3Defnder-K3Atacker-infra`の独立した運用Scriptが担う。通常のContainer再起動では再生成せず、再生成はK3AT停止確認、K3DFのReferee／Consumer停止、対象Volume限定、Referee状態初期化、形式・一意性・所有権・権限検証および成功後の再起動を一体の管理操作として行う。Flag値、Seed、HintをCLI引数、標準出力、Log、GitまたはSecret用途の環境変数へ出さない。

## Feedback records

- `F-00003`: Capabilityに応じてToolをLOCKEDまたはAVAILABLEにする方式は、ゲーム的で現実の環境に即していない。Toolは最初から提示し、利用結果は具体的なCredential、Session、接続状態および安全Policyによって決まるべきである。
- `F-00012`: K3ATのTool拡張ロードマップを正式方針として採用する。実装済みToolはRun開始時からすべてKimi K3へ提示し、実装順序を攻撃経路またはTool解放順序として扱わない。Tool実行可否はTarget、Protocol、Credential、Session、Budgetなどの具体的条件で決定する。Raspberry PiのHost OS、Management SSH、Management Network、Host filesystemおよびDocker socketは対象にしない。
- `F-00013`: Strategy Briefが長いJSONとして表示され、人間が内容や優先順位を把握しにくい。機能自体は受入れるが、可読性改善を独立Taskとして実施する。
- `F-00031`: Run IDとTokenをK3DFからK3ATへFile配送してbind mountする運用はデモ用途として過剰である。mount元Fileが存在しない場合に同名Directoryが生成され、K3ATが起動できない事象も発生したため、簡素な共有Seed方式へ置き換える。
- `F-00032`: K3DFのCTF runtimeをProvisioningせずにComposeを起動した結果、Flag 1〜3、Run IDおよびRun TokenのHost bind mount元がroot所有のDirectoryとして自動生成され、Refereeの通常File検査と`nobody`による所有権境界に適合せず再起動ループになった。Host bind方式を廃止し、生成成功後だけRefereeを起動できるNamed Volume運用へ置き換える。
