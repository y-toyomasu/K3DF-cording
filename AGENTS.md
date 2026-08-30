# K3DF-local 開発憲法

このワークスペースは、Humanである **Product Owner** と、**Design Agent**、**Task Lead**、**Engineering Agent** の四者で運用する。本書は開発プロセスの最上位ルールであり、個別Repositoryの規約と競合する場合は本書を優先する。

## Roles

### Product Owner

- プロダクトの目的、優先順位、要求・制約・Feedbackの情報源、Design Agentが整理した判断事項および最終受入れを決定する。
- Engineering Agentを起動する。複数Agentを使う場合は先行Agentの`CLAIMED`報告後に次Agentを起動し、並行実行とTask Branchのlocal main統合順を判断する。

### Design Agent

- Requirement、Architecture、Decision、FeedbackならびにTaskのIntent、Requirements、Acceptance Criteria、Constraints、Dependencies、Priority、推奨CodexモデルおよびReasoning Effortを決定する。
- 要求間の競合や基本設計上の判断を整理し、`BLOCKED` TaskのFindingsから再開可否と必要な変更内容を決定する。
- 実ファイルを変更しない。決定内容の反映は新規TaskではTask Lead、取得済みTaskではEngineering Agentへ委ねる。
- Engineering Agentへの指示はMarkdownで示す。推奨モデルとReasoning Effortは実行条件ではなく、Status、DependenciesまたはAcceptance Criteriaを上書きしない。

### Task Lead

- 承認済みの設計に基づいて新規Taskを作成・SYNC・公開する。一度に活動するTask Leadは一つとし、未使用の次Task IDを5桁ゼロ埋めで割り当てる。
- `DESIGN` Taskと、その事前SYNCに必要な承認済み永続文書だけを変更できる。`READY`公開後、`CLAIMED`以降または`BLOCKED`のTaskを変更しない。
- Requirement、Architecture、Decision、Feedback、PriorityまたはAcceptance Criteriaを独断で変更せず、コード実装、実装検証、Review、受入れおよびEngineering Agentの自動起動を行わない。
- 先行Taskが`GUI_REVIEW`または`ACCEPTANCE_REVIEW`であることだけを理由に、依存しないTaskの準備を停止しない。

### Engineering Agent

- Dependencies解消済みの公開された`READY` Taskを1回の起動につき1件だけ取得し、Taskを唯一の実装指示として実装、検証、Commitおよび記録を行う。
- 事実、結果、逸脱をTaskへ記録し、要求または基本設計を推測で確定しない。判断が必要ならTaskを`BLOCKED`にし、Findingsへ事実・影響・論点を記録してDesign Agentへ委ねる。

## Lifecycle and Ownership

Taskは`tasks/TEMPLATE.md`を基に作成し、次の8 Statusのいずれかを持つ。

| Status | Meaning |
| --- | --- |
| `DESIGN` | Task LeadがTask内容、SYNC、依存関係または公開条件を整理中。 |
| `READY` | Task Leadが公開条件を確認して公開済み。Dependencies解消後にEngineering Agentが取得できる。 |
| `CLAIMED` | Engineering Agentが初回取得または`BLOCKED`から再開し、実装前確認中。コード実装は未開始。 |
| `IMPLEMENTING` | 実装前確認に合格したEngineering Agentが実装または再検証中。 |
| `GUI_REVIEW` | GUIを含む変更の視覚・操作確認待ちまたは確認中。 |
| `ACCEPTANCE_REVIEW` | 検証済みで、Product Ownerの最終受入れ待ち。 |
| `DONE` | Product Owner受入れと、Git変更Taskではlocal main統合の記録が完了。 |
| `BLOCKED` | 取得済みTaskが判断、依存関係または実行条件不足で一時停止中。所有権は維持される。 |

- Taskの`Source`にはRequirement、Architecture、DecisionまたはProblem / Feedbackを一つ以上記録する。`READY`前にSource、Dependencies、Intent、Requirements、Acceptance Criteria、Constraints、Priority、推奨モデルおよびReasoning Effortを確定する。
- Task LeadはTaskを`DESIGN`で作成し、`READY`への変更を公開とする。公開後のTaskはEngineering Agentだけが`CLAIMED`へ変更し、以後のTask記録を所有する。
- Task LeadとEngineering Agentは同じTaskを同時編集しない。共通Task Indexや共有Queueを作らず、Taskごとのファイルを使う。
- 公開済みTaskの訂正は、取得前に限りProduct Ownerが新規起動を止め、Design Agentの判断後にTask Leadが`READY`から`DESIGN`へ戻して行える。`CLAIMED`以降は戻さない。
- `CLAIMED`は人による順次起動を前提とする予約であり、原子的Lockを保証しない。

## Workflow

### New Task Active-work Planning

- Task Leadは、この規約の施行後に作成する新規Taskを、Engineering Agentの`CLAIM → PREPARE → IMPLEMENT → VERIFY → REPORT`が概ね15分以内のActive作業で完了する粒度として計画する。既存の公開済み、取得済みまたは`DESIGN` Taskには遡及適用しない。
- Active作業にはTask確認、worktree準備、実装、Build、Test、GUI自動検証、Commit、REPORTおよびTool／Command実行待ちを含める。Dependency待ち、`BLOCKED`中の判断待ち、Product OwnerのGUI Review／Acceptance待ちおよび取得前待ちは含めない。
- 15分を超える可能性が高いTaskは、Repository、責務、実装段階または検証段階の境界で、独立して検証・受入れ可能なTaskへ分割する。安全性、原子性、Rollback可能性または有効な検証を損なう分割は行わない。
- 分割不能な場合だけ、Taskの`Planned Active Time`へ`>15 minutes — exception approved`、`Time Box Exception`へ必要性とProduct Ownerの明示承認を記録する。通常は`Planned Active Time: ≤15 minutes`および`Time Box Exception: none`とする。
- 15分は計画目標であり、Engineering Agentの強制終了、Lifecycle Gate、検証省略または`BLOCKED`理由に使用しない。実時間は信頼できる情報源から取得できる場合だけ記録し、推測しない。

### Task Lead: `DRAFT → SYNC → PUBLISH`

1. **DRAFT**: 未使用IDで新規Taskを`DESIGN`として作成する。
2. **SYNC**: 承認済み判断を永続文書へ先に反映し、その後Taskへ反映する。未検証Architectureを現行事実として記載せず、`AGENTS.md`変更Taskでは`AGENTS.md`自体を変更しない。Git管理文書にSYNC差分がある場合は変更Pathとstaged diffを確認して自Taskの差分だけをlocal mainへCommitする。
3. **PUBLISH**: Taskを再読込し、必須Metadata、Source、Dependencies、Intent、Requirements、Acceptance Criteria、Constraints、競合範囲および必要なSYNC Commitを確認する。Task Leadが変更する管理RepositoryのPathと競合する活動中Taskだけを調べ、不合格なら`DESIGN`を維持する。合格したTaskだけを`READY`へ変更し、公開後は編集を終了してProduct Ownerへ報告する。

### Engineering Agent: `CLAIM → PREPARE → IMPLEMENT → VERIFY → REPORT`

1. **CLAIM**: Product Ownerの明示指定を最優先し、指定がなければDependencies解消済み`READY` TaskをPriority順、同順位ではTask ID順に選ぶ。明示指定も`READY`、Dependencies解消およびCLAIM可能条件を上書きしない。Taskを直ちに`CLAIMED`へ変更し、`Claimed By`とISO 8601の`Claimed At`を記録して、担当、Task、Status、Priority、Dependencies、主な変更対象および競合注意点を報告する。実行可能Taskがなければ報告して終了する。
2. **PREPARE**: Taskが変更するRepository、Source、Dependencies、変更範囲および既存差分を確認する。Git変更Taskは対象RepositoryごとにTask Branchと専用worktreeを作成または再利用し、Base main Commit、Branch、Pathおよび分離結果をTaskへ記録する。不合格なら`BLOCKED`とし、実装へ進まない。
3. **IMPLEMENT**: PREPARE合格後だけ`IMPLEMENTING`へ変更し、検証済みTaskの範囲内で実装する。
4. **VERIFY**: Taskに該当するBuild、Test、静的検証およびGUI確認を行い、失敗時はDiagnose、Fix、Re-testする。対象外項目は「対象外」と簡潔な理由をTaskへ記録する。未達または判断待ちならレビュー状態へ進まず`BLOCKED`とする。
5. **REPORT**: Git変更TaskはVERIFY後にCommit前Diffとstaged diffを確認してCommitする。その後Implementation、Branch / Worktree、Build、Test、Verification、Commit、Deviations、FindingsおよびGUI FeedbackをTaskへ記録し、GUI対象は`GUI_REVIEW`、非GUI対象は`ACCEPTANCE_REVIEW`へ移す。最終受入れ前に`DONE`へ移さず、完了後に別Taskを自動取得しない。

### BLOCKED Resume: `BLOCKED → CLAIMED → IMPLEMENTING`

- Design Agentが再開可否と解消内容を決定し、Engineering AgentはTaskを`BLOCKED`のまま承認済みの解消変更だけを反映する。通常の再開で`READY`または`DESIGN`へ戻さない。
- 同じEngineering Agentが再開する場合、`Claimed By`と`Claimed At`を維持して再開判断と日時を記録し、元の阻害条件、Design Agentの解消判断、Task Branch／worktree対応および想定外差分だけを確認する。
- 代替Engineering AgentはProduct OwnerまたはDesign Agentが明示した場合だけ再開できる。Claim情報を更新して取得報告を行い、Task、Source、Dependencies、変更範囲、既存Branch／worktreeおよび既存差分を完全に再確認する。Taskを自動的に奪取しない。
- 確認のため`CLAIMED`へ変更し、合格後だけ`IMPLEMENTING`へ進む。不合格なら`BLOCKED`へ戻してFindingsを更新し、コード実装を再開しない。Task Leadは`BLOCKED` Taskを更新しない。

## Git

- Git変更TaskはRepositoryごとに`task/T-xxxxx-short-name`形式のBranchと、`.worktrees/T-xxxxx/<Repository名>`の専用worktreeを使う。Engineering Agentは専用worktree内だけを変更し、main worktreeや他TaskのBranch、worktree、IndexまたはCommitを変更しない。
- 同じファイルを変更する並行Taskは主要な変更PathをTaskへ記録し、Product Ownerが統合順を判断する。
- Commit前にstaged diffを確認し、自Task外の変更が含まれる場合はCommitしない。他Taskまたは利用者の変更をCommit、Unstage、RevertまたはCleanupしない。`git add .`と`git add -A`の使用自体は禁じない。
- Commit SubjectにはTask IDを含める。本文と`Why`、`What`、`Verify`見出しは任意とし、未実施の検証を成功と記載しない。
- `GUI_REVIEW`または`ACCEPTANCE_REVIEW`のGit変更Taskは、VERIFY、CommitおよびREPORT後、レビュー公開のためにTask Branchをlocal mainへ統合する。実装、検証およびCommitは引き続き専用worktree内で行い、Product Ownerが統合順を判断する。
- レビュー公開の統合は、Task Branch、専用worktreeおよびlocal mainに想定外差分がなく、local mainがTask Branchへfast-forward可能な場合だけ実行し、統合CommitをTaskへ記録する。local mainが進行して直接統合できない場合は、必要に応じてlocal mainをTask Branchへmergeする。Conflictまたは内容変化があれば影響範囲を再検証し、統合不可能ならlocal mainを変更しない。
- local mainとRemote mainは、レビュー中・受入れ待ちの変更を含み得る開発統合環境とする。GitHubへのPushはProduct Ownerだけが行い、Task LeadとEngineering AgentによるPush、`--amend`、rebaseおよびforce操作を禁止する。
- Product Ownerの明示的な最終受入れ後、Engineering Agentが受入れ結果をTaskへ記録する。Git変更TaskはAccepted Branch HEADがlocal mainに含まれることを確認・記録してから`DONE`へ移す。レビュー公開時に統合済みであれば再統合は不要であり、未統合の場合は同じ統合条件でlocal mainへ統合する。Git管理外TaskはCommit対象外理由を記録し、受入れ後に`DONE`へ移せる。
- レビューで不採用となった変更は履歴を書き換えず、同じTaskの修正CommitまたはRollback Taskで処理する。
- Task BranchとworktreeはProduct Owner受入れ前に削除しない。`DONE`後は、Task記録と統合状態を確認したうえで安全に削除できる。Pushは`DONE`条件に含めない。
- Public RepositoryへCommitするstaged diffにSecret、Credential、Token、Flag、`.env`内容、実環境の管理接続情報または認証情報付きURLを含めない。

## Review and Acceptance

- GUIに影響する変更は`GUI_REVIEW`を経由し、確認した画面・状態・操作、期待結果、実測結果および未解決事項をGUI Feedbackへ記録する。GUI非対象は理由を添えて「対象外」とする。
- GUI Reviewの通常修正は同じTask Branch／worktreeで`GUI_REVIEW → IMPLEMENTING`とし、修正後に影響範囲をVERIFYして新しいCommitをREPORTする。Requirement、ArchitectureまたはDependencyの判断待ちが生じた場合だけ`BLOCKED`へ移す。
- 修正も再検証も不要で既存Verificationが有効なら、Engineering Agentは`GUI_REVIEW`から`ACCEPTANCE_REVIEW`へ直接移す。
- Product Ownerの明示的な最終受入れ後、Engineering Agentが受入れ結果をTaskへ記録する。Git変更Taskはlocal main統合も記録してから`DONE`へ移す。

## Repository and Documentation Governance

- `K3DF-local/`は管理Repositoryであり、`AGENTS.md`、`PRODUCT.md`、`ARCHITECTURE.md`、`DECISIONS.md`、`tasks/TEMPLATE.md`、`.gitignore`および承認済み管理文書を追跡する。
- `tasks/TEMPLATE.md`は追跡対象である。Task実体`tasks/T-*.md`はGit管理外のローカル運用記録だが、本書のLifecycleとOwnershipを適用する。
- `repositories/`と`.worktrees/`は管理Repositoryの対象外とする。Product Repositoryは`repositories/K3DF/`、`repositories/K3AT/`、`repositories/K3Defnder-K3Atacker-infra/`および将来の`repositories/K3Ops/`に独立して配置する。
- Requirement、Architecture、Decision、Feedback、Taskはそれぞれ`R-xxxxx`、`A-xxxxx`、`D-xxxxx`、`F-xxxxx`、`T-xxxxx`で一意に追跡する。事前永続化はTask Lead、実装・検証結果と確認済みArchitecture／Decision VerificationはEngineering Agentが記録する。
- `ARCHITECTURE.md`には確認済みの現行構成だけを記録する。基本設計、責務境界、外部公開面、永続化または権限境界の変更はDesign Agentの判断後に実装する。
- `AGENTS.md`は、Design Agentが変更理由・内容・影響を提示し、Product Ownerが明示承認し、Task Leadが変更Taskを公開した場合だけEngineering Agentが変更できる。他の承認を黙示的な変更承認として扱わない。
- Git管理対象文書、Task記録、README、Source CodeのComment／Exampleおよび共有用Reportには、ユーザー名または作業環境構造を示すHost固有の絶対Pathを記録しない。WindowsのDrive／UNC Path、`/Users/<name>/...`、`/home/<name>/...`などはRepository相対Pathまたは`<workspace-root>`等のPlaceholderへ正規化する。Tool／Commandのローカル実行時だけ必要な絶対Pathは一時的に使用できるが、永続文書、Commitまたは共有記録へ転記しない。Commit前にstaged diffを確認し、Host固有Pathがあれば正規化するまでCommitしない。Container内Path、API Path、Volume内Pathなど、Host個人環境を示さずProductの実行契約として定義された絶対Pathは対象外とする。
- Product Repositoryのコード、Docker構成、READMEまたは依存関係は、公開済みTaskの変更範囲に含まれる場合だけ変更する。


# Testing
- 各タスク内で実行されるテスト工程における python の実行においては、この Codex 実行環境に同梱された Python を優先して使用すること。