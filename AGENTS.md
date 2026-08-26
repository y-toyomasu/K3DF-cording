# K3DF-local 開発憲法

このワークスペースでは、Humanが担う **Product Owner**、**Design Agent**、**Task Lead**、**Engineering Agent** の四者で開発を運用する。本書は開発プロセス上の最上位ルールであり、各サブプロジェクトにまたがる共通の作業規約である。個別Repositoryの規約と競合する場合は、本書を優先する。

## Roles

### Product Owner

- プロダクトの目的、優先順位、受入れ判断を担う。
- 要求、制約、フィードバックの情報源を明示する。
- Design Agentが整理した判断事項を決定する。
- 最終受入れを明示的に判断する。
- Engineering Agentの起動はProduct Ownerが行う。Task LeadはEngineering Agentを自動起動しない。
- 複数Engineering Agentを使用する場合、先行Agentの`CLAIMED`報告を確認してから次のAgentを起動する。
- Task LeadまたはEngineering Agentの報告を受け、並行実行の開始・停止を判断する。
- 複数TaskのTask Branchをlocal mainへ統合する順序を判断し、Engineering AgentのCommit報告、受入れ対象Commitおよびlocal main統合結果を確認する。
- GitHubへのPushはProduct Ownerだけが行う。Engineering AgentのGit Commitまたはlocal main統合を、自動PushまたはPush権限の委譲として扱わない。
- K3DF-local管理Repositoryの初回Bootstrapを手動で行う唯一のRoleとする。`.git`の移動・作成・初期化、初回Branch・Commit、`.gitignore`調整、Remote設定および初回Pushを管理し、Task LeadまたはEngineering AgentへBootstrapを委譲しない。

### Design Agent

- Requirement、Architecture、Decision、FeedbackならびにTaskのIntent、Requirements、Acceptance Criteria、Constraints、Dependencies、Priority、推奨CodexモデルおよびReasoning Effortを決定し、要求を実装可能な形に整理する。
- 要求間の競合、ユーザー体験、アーキテクチャ上の判断事項およびFeedbackを解釈・整理し、必要に応じてProduct Ownerに提案する。
- `BLOCKED` TaskのFindingsを分析し、再開可否と必要な変更内容を決定する。
- 実ファイルは変更しない。新規Taskの内容はDesign Agentが決定し、Task Leadが新規Taskファイルと承認済み永続ドキュメントへ反映する。
- 取得済みTaskの実ファイルおよびプロセス記録はEngineering Agentが更新し、Task Leadは更新しない。
- Engineering Agentへの指示はMarkdown形式で出力し、Taskの性質に応じた推奨CodexモデルおよびReasoning Effortを記載する。モデルとReasoning Effortは実行条件ではなく推奨であり、TaskのStatus、DependenciesまたはAcceptance Criteriaを上書きしない。

### Task Lead

- Design Agentが決定し、Product Ownerが必要な判断を承認した内容に基づき、新規Taskを`DESIGN`で作成する。
- 承認済み判断を該当する永続ドキュメントへ先に反映し、その後Taskへ反映する。
- Taskを公開する前に、Status、Source、Dependencies、Intent、Requirements、Acceptance Criteria、Constraints、Priority、推奨Codexモデル、Reasoning Effortおよび競合範囲をVALIDATEする。
- 公開条件を満たすTaskだけを`READY`へ変更する。
- 未使用の次Task IDを5桁ゼロ埋めで割り当てる。一度に活動するTask Leadは一つとする。
- `DESIGN` Taskと、そのTaskの事前SYNCに必要な承認済み永続ドキュメントだけを変更できる。
- コード実装、Build、Test、Verification、GUI ReviewまたはProduct Owner Acceptanceを行わない。
- Requirement、Architecture、Decision、Feedback、PriorityまたはAcceptance Criteriaを独断で決定・変更しない。
- Engineering Agentを自動起動せず、独立Task間の自動メッセージ連携を前提にしない。
- `CLAIMED`以降のTaskを変更しない。
- `IMPLEMENTING` Taskと同じ永続ドキュメントを同時編集しない。競合する場合はTaskを`DESIGN`のまま維持して報告する。
- 先行Taskが`GUI_REVIEW`または`ACCEPTANCE_REVIEW`であることだけを理由に、依存しない次Taskの作成・公開を停止しない。
- Product Ownerによる管理Repositoryの初回Bootstrapを実行しない。Bootstrap完了後はRepository境界と追跡・除外状態を読み取り確認し、管理RepositoryへSYNC差分がある場合だけ、定義された`COMMIT_SYNC`規則に従う。

### Engineering Agent

- 公開済みでDependencies解消済みの`READY` Taskを取得し、`CLAIMED`へ変更してから、定義済みの要求・設計・制約に従って実装、検証、記録する。
- 事実、結果、逸脱をTaskに残し、推測で要求または基本設計を確定しない。
- Design Agentが決定し、Task Leadが公開したTaskを唯一の実装指示として実ファイルへ反映する。
- Design Agentが取得済み`BLOCKED` Taskの再開可否と必要な変更内容を決定した後、Engineering Agentは承認済み変更だけを反映する。`BLOCKED`中は阻害条件の解消に必要な永続ドキュメント、Task内容およびプロセス記録だけを更新し、コード実装を再開しない。
- `BLOCKED` Taskは、元のEngineering Agent、またはProduct OwnerもしくはDesign Agentが明示的に再開担当とした代替Engineering Agentだけが、`BLOCKED Task Resume Sequence`に従って再開する。
- Git Repositoryを変更するTaskでは、Task専用Branchと専用Git worktreeを使用し、main worktreeまたは他TaskのBranch・worktree・Index・Commitを変更しない。
- VERIFY合格後、REPORT前に自Taskの変更だけをCommitし、Repository、Branch、Commit Hash、Subjectおよびworktree clean確認をTaskへ記録する。
- Product Ownerの最終受入れ後、受入れ対象Branchとlocal mainの統合条件を再確認し、fast-forward可能な場合だけlocal mainへ統合する。Engineering AgentはGitHubへPushしない。
- Product Ownerによる管理Repositoryの初回Bootstrapを実行しない。Bootstrap完了後に管理Repositoryの境界と追跡・除外状態を読み取り確認し、合格後だけ管理Repositoryを通常のTask Branch・worktree規則の対象にする。
- Product OwnerへRequirementまたはArchitectureの判断を直接求めない。判断が必要な場合は、次の順で対応する。
  1. Taskを`BLOCKED`にする。
  2. `Findings`に論点、影響範囲、確認済みの事実を記録する。
  3. Design Agentへ判断を委ねる。

## Task Lifecycle

Taskは`tasks/TEMPLATE.md`を基に作成し、常に次のいずれかの状態を持つ。

| Status | Meaning |
| --- | --- |
| `DESIGN` | Task LeadがTask内容、SYNC、依存関係または公開条件を整理中。Engineering Agentは取得できない。 |
| `READY` | Task LeadのSYNC、VALIDATE、および必要な場合の`COMMIT_SYNC`が完了し、公開された状態。Engineering Agentが取得できる。 |
| `CLAIMED` | Engineering Agentが初回取得したTask、または承認済み変更を反映した`BLOCKED` Taskについて、必要なTask Branch・worktreeの分離、再読込および実装前VALIDATEを行っている。コード実装はまだ開始していない。 |
| `IMPLEMENTING` | 取得後VALIDATEに合格したEngineering Agentが実装中。 |
| `GUI_REVIEW` | GUIを含む変更の視覚・操作確認待ちまたは確認中。 |
| `ACCEPTANCE_REVIEW` | 検証済みで、Product Ownerによる最終受入れ判断待ち。GUI・非GUIを問わない。 |
| `DONE` | Product Ownerの受入れ後、Engineering Agentが結果を記録して完了にした状態。 |
| `BLOCKED` | 取得済みTaskが必要な判断、依存関係または実行条件の不足により一時停止している。取得済みの所有権は維持される。 |

- `Source`には少なくとも一つの`Requirement`、`Architecture`、`Decision`または`Problem / Feedback`を記録する。Sourceが存在しないTaskは公開または実装してはならない。
- 新規Taskは`DESIGN`で作成し、Dependencies未解消または公開条件未達の場合は`DESIGN`のまま維持して`READY`にしない。
- `READY`へ移す前に、Intent、Requirements、Acceptance Criteria、Constraints、Dependencies、Priority、推奨CodexモデルおよびReasoning Effortを埋める。
- 管理RepositoryのGit管理対象文書をSYNCしたTaskは、Product Ownerによる初回Bootstrap完了後、Task Leadが自TaskのSYNC差分だけを`COMMIT_SYNC`してから`READY`へ移す。変更なしまたはCommit対象外の場合は理由を記録する。
- `ACCEPTANCE_REVIEW`へ移す前に、Build Result、Test Result、Verification Result、Deviations、Findingsを更新する。GUIを含む変更はGUI Feedbackも記録する。
- Git Repositoryを変更したTaskは、自Taskの変更がTask BranchへCommit済みで専用worktreeがcleanな場合だけ`GUI_REVIEW`または`ACCEPTANCE_REVIEW`へ移せる。
- Product Ownerが最終受入れを判断した後、Engineering Agentは受入れ結果をTaskへ記録し、受入れたTaskを`DONE`へ変更する。
- Git Repositoryを変更したTaskは、Product Ownerの最終受入れ後に受入れ済みTask Branchをlocal mainへ統合し、Integrated local main Commitを記録した場合だけ`DONE`へ変更できる。GitHubへのPushは`DONE`条件に含めない。
- Git管理外ファイルだけを変更するTaskは、Commit対象外理由を記録し、従来どおりProduct Ownerの最終受入れ後に`DONE`へ変更する。
- 取得済みTaskの要求または設計の判断待ちは`BLOCKED`とし、Engineering Agentは独断で回避しない。
- `BLOCKED`は未取得Taskへ戻った状態ではない。通常の再開では`READY`または`DESIGN`へ戻さず、承認済み変更の反映後に`CLAIMED`へ遷移して再読込と再VALIDATEを行う。
- `CLAIMED`は人によるEngineering Agentの順次起動を前提とする運用上の予約であり、原子的Lockを保証しない。

## Task File Ownership

- Task Leadは新規Taskを`DESIGN`として作成・更新し、`READY`への変更をTaskの公開とする。
- `READY`公開後、Task LeadはそのTaskの編集を終了する。公開済み`READY` Taskの通常内容は変更せず、Engineering Agentだけが`CLAIMED`へ遷移できる。
- `CLAIMED`以降のTask記録は、取得したEngineering Agentが更新する。Task Leadは別IDの`DESIGN` Taskを作成できる。
- Task LeadとEngineering Agentは同じTaskファイルを同時編集しない。共通Task Indexまたは共有Queueファイルを作らず、Taskごとのファイルを使用する。
- 公開済み`READY` Taskの訂正が必要な場合、Product OwnerはEngineering Agentの新規起動を停止する。Design Agentの判断後、Task Leadは取得処理が進行していないことを確認した場合に限り、例外として`READY`から`DESIGN`へ戻せる。
- すでに`CLAIMED`のTaskをTask Leadが`DESIGN`または`READY`へ戻してはならない。
- `CLAIMED` Agentが停止した場合、Product OwnerまたはDesign Agentが代替Engineering Agentを再開担当として明示する必要があり、別Engineering Agentが自動的にTaskを奪取してはならない。
- `BLOCKED` Taskの所有権は元のEngineering Agentが維持する。Task Leadは`BLOCKED` Taskを更新、公開または再取得しない。
- 代替Engineering Agentは、Product OwnerまたはDesign Agentから再開担当として明示された場合だけ`BLOCKED` Taskを再開できる。元Agentから自動的にTaskを奪取してはならない。

## Design Agent Entry Point

Design Agentは対話開始時に、必要に応じて以下を参照する。

- `PRODUCT.md`
- `ARCHITECTURE.md`
- `DECISIONS.md`
- `tasks/`

Product Ownerとの対話からRequirement、Architecture、Decision、FeedbackおよびTask候補を整理し、新規TaskのIntent、Requirements、Acceptance Criteria、Constraints、Dependencies、Priority、推奨CodexモデルおよびReasoning Effortを決定する。実ファイルへの反映はTask Leadへ委ねる。

Design Agentは、先行Taskが`GUI_REVIEW`または`ACCEPTANCE_REVIEW`であることだけを理由に、次Taskの設計を停止してはならない。次Taskが先行TaskのGUI FeedbackまたはProduct Ownerの受入判断に依存する場合は、その依存関係をDependenciesとして決定し、解消まで公開不可とする。依存しない場合は、先行Taskのレビューまたは受入れ完了をDependenciesへ追加しない。

Design Agentは`BLOCKED` TaskのFindingsを分析し、再開可否と阻害条件の解消に必要な変更内容を決定する。GUI Review後は、実装修正または再検証が必要か、既存Verificationを有効として`ACCEPTANCE_REVIEW`への状態遷移だけを行えるかも決定する。取得済みTaskの承認済み変更はEngineering Agentが反映する。

## Task Lead Entry Point

Task Leadは開始時に次を確認する。

- `AGENTS.md`
- `PRODUCT.md`
- `ARCHITECTURE.md`
- `DECISIONS.md`
- `tasks/`
- 関係RepositoryのStatusおよび既存差分

Task Leadは未使用Task IDと、一度に活動するTask Leadが一つであることを確認する。`IMPLEMENTING` Taskと永続ドキュメントの変更範囲が競合する場合、新規Taskを`DESIGN`のまま維持してProduct Ownerへ報告する。管理Repositoryの初回Bootstrap後は、Repository境界、追跡対象、除外対象、現在BranchおよびWorking Treeを読み取り確認し、`tasks/TEMPLATE.md`が追跡対象、`tasks/T-*.md`がGit管理外であることを確認してから通常運用へ進む。不合格の場合は管理Repositoryを変更せず報告する。

Git Repositoryを変更する新規Taskでは、既存Task Branchとworktreeの一覧も確認し、想定Repositoryおよび競合範囲をTaskへ記録する。Task LeadはBranchまたはworktreeを作成しない。

## Engineering Agent Entry Point

Engineering Agentは作業開始時に`AGENTS.md`と`tasks/`を確認し、1回の起動につき1件のTaskだけを取得する。管理Repositoryの初回Bootstrap後は、Repository境界、追跡対象、除外対象、現在BranchおよびWorking Treeを読み取り確認し、`tasks/TEMPLATE.md`が追跡対象、`tasks/T-*.md`がGit管理外であることを確認する。不合格の場合は管理Repositoryを変更せず、取得済みTaskを`BLOCKED`にしてFindingsへ記録する。

取得対象はDependencies解消済みの`READY` Taskだけとする。Product Ownerが実装対象を明示指定した場合はそのTaskを最優先するが、指定は`READY`、Dependencies解消またはCLAIM可能である条件を上書きしない。

指定がない場合はDependencies解消済みの`READY` Taskを選択する。複数ある場合はPriorityが高い順、同一PriorityではTask IDの昇順とする。実行可能な`READY` Taskがなければ、その旨を報告して終了する。

Task選択後、Taskを再読込して直ちに`CLAIMED`へ変更し、`Claimed By`へEngineering Agent識別名、`Claimed At`へISO 8601形式の時刻を記録する。`CLAIMED`変更後、コード実装前にProduct Ownerへ次を報告する。

- Engineering Agent
- Claimed Task
- Status
- Priority
- Dependencies
- 主な変更対象
- 並行実行時の競合注意点

取得報告後は応答を待たず、TaskとSource文書の再読込およびVALIDATEを継続する。1件のREPORT完了後、別Taskを自動取得しない。

Git Repositoryを変更するTaskでは、取得報告後、RELOAD前にISOLATEを行う。対象RepositoryごとにTask専用Branchと専用worktreeを作成または同一Taskの既存分離環境を再利用し、Base main Commit、Task Branch、Worktree pathおよびIsolation resultをTaskへ記録する。管理Repository変更Taskでは、Product Ownerによる初回BootstrapとRepository境界確認が完了している場合だけISOLATEする。Git管理外のTask実体だけを変更するTaskでは、ISOLATE対象外理由を記録する。

## Traceability

- 要求、設計、決定、問題・Feedbackから、Task、実装、検証結果までをたどれるようにする。
- Traceability IDは、Requirementを`R-xxxxx`、Architectureを`A-xxxxx`、Decisionを`D-xxxxx`、Feedbackを`F-xxxxx`、Taskを`T-xxxxx`とする。`xxxxx`は5桁ゼロ埋めの数字であり、各IDはワークスペース内で一意とする。
- TaskのSourceには、該当するTraceability IDと、`PRODUCT.md`、`ARCHITECTURE.md`、`DECISIONS.md`または問題・Feedbackの参照先を記録する。
- Requirement、DecisionおよびFeedbackの事前永続化はTask LeadがSYNCで行う。
- 実装で追加・変更したファイル、Build、Test、検証、既知の未解決事項、確認済みArchitectureおよびDecision VerificationはEngineering AgentがREPORTで記録する。
- Git Repositoryを変更するTaskは、RepositoryごとにBase main Commit、Task Branch、Worktree path、Isolation result、Task Commit Hash、Commit Subject、worktree clean確認、Accepted Branch HEADおよびIntegrated local main Commitを記録する。Git管理外TaskはCommit対象外理由を記録する。
- GitHubへのPushはProduct Owner管理であることをTaskへ記録し、Engineering AgentはPush結果を`DONE`条件にしない。
- 未検証の将来構成を`ARCHITECTURE.md`へ記載しない。
- 推奨CodexモデルとReasoning Effortは実行条件ではなく、Task LeadがTaskへ反映する推奨値とする。

## Architecture Governance

- `ARCHITECTURE.md`は確認済みの現行構成を記録する。推測、将来案、未確認の内部仕様を事実として書かない。
- 基本設計レベルの変更は`DECISIONS.md`に、変更内容、背景・理由、検討した選択肢、影響、検証を記録する。
- 既存Architectureと矛盾しうる変更、責務境界の変更、外部公開面・データ永続化・権限境界の変更は、Design Agentの判断を経てから実装する。
- 判断が未確定の場合、取得済みTaskをEngineering Agentが`BLOCKED`にしてDesign Agentへ委ねる。

## Task Lead Preparation Sequence

Task Leadは`DRAFT` → `SYNC` → `VALIDATE` → `COMMIT_SYNC` → `PUBLISH`の順序で進める。特に`SYNC` → `VALIDATE` → `COMMIT_SYNC` → `PUBLISH`は省略または入替えできない。管理Repositoryの初回Bootstrap前はTask LeadがBootstrapまたはCommitを行わず、`COMMIT_SYNC`対象外理由を記録する。

1. **DRAFT**: 未使用Task IDで新規Taskを`DESIGN`として作成する。
2. **SYNC**: 承認済み判断を永続ドキュメントへ先に反映し、その後Taskへ反映する。`ARCHITECTURE.md`へ未検証の構成を現行事実として追加しない。`AGENTS.md`変更Taskでは、Task Leadは`AGENTS.md`自体をSYNC対象として変更しない。
3. **VALIDATE**: Taskを再読込し、Status、Source、Dependencies、Intent、Requirements、Acceptance Criteria、Constraints、Priority、推奨Codexモデル、Reasoning Effort、公開条件および競合範囲を検証する。不適格なら`DESIGN`のまま維持する。
4. **COMMIT_SYNC**: Product Ownerによる管理Repositoryの初回Bootstrap完了後、Git管理対象の永続文書に自TaskのSYNC差分がある場合だけ、Task Leadが自身の変更Pathを明示的にStageしてlocal mainへCommitする。`AGENTS.md`、Task実体、`repositories/`、`.worktrees/`、個人メモ、他Taskまたは利用者の変更を含めず、`git add .`、`git add -A`および無差別なWildcardを使用しない。Commit後に管理RepositoryがcleanであることとCommit HashをTaskへ記録する。変更なし、Bootstrap前またはCommit対象外では理由を記録する。Commit失敗、競合または想定外差分がある場合はPUBLISHへ進まない。Task LeadはPushしない。
5. **PUBLISH**: 条件を満たすTaskだけを`READY`へ変更する。公開後はそのTaskの編集を終了し、Product OwnerへTask IDと並行実行上の注意点を報告する。

## Engineering Agent Execution Sequence

Engineering Agentは`CLAIM` → `ISOLATE` → `RELOAD` → `VALIDATE` → `IMPLEMENT` → `VERIFY` → `COMMIT` → `REPORT`の順序で進める。Task LeadによるSYNC後も、Engineering AgentのISOLATE、RELOADおよびVALIDATEを省略できない。Git管理外ファイルだけを変更するTaskはISOLATEとCOMMITの対象外理由を記録し、空Commitを作成しない。

1. **CLAIM**: Dependencies解消済みの`READY` Taskを`CLAIMED`へ変更し、`Claimed By`と`Claimed At`を記録して取得情報を報告する。
2. **ISOLATE**: Git Repositoryを変更するTaskは、対象Repositoryごとにlocal mainのCommit Hashを記録し、`task/T-xxxxx-short-name`形式のTask専用Branchと、ワークスペース直下の`.worktrees/T-xxxxx/<Repository名>`を標準配置とする専用Git worktreeを作成する。同じTaskの既存Branch・worktreeは再利用できるが、他Taskと衝突する場合は実装へ進まない。複数Repositoryを変更する場合は、各Branch名へ同じTask IDを含める。
3. **RELOAD**: Task、Source文書、対象Repository、Base main Commit、Task Branch、Worktree pathおよびWorking TreeをファイルとGitから再読込する。
4. **VALIDATE**: Status `CLAIMED`、Task LeadのSYNC記録、Source、Dependencies、Requirements、Acceptance Criteria、Constraints、作業差分、およびTaskの変更対象とBranch・worktreeの対象Repositoryが一致することを確認する。不合格ならコード実装へ進まず、Taskを`BLOCKED`にしてFindingsへ事実、影響範囲および判断待ちの論点を記録し、Design Agentへ委ねる。
5. **IMPLEMENT**: VALIDATE合格後だけ`IMPLEMENTING`へ変更する。VALIDATE済みTaskを唯一の実装指示とし、Git RepositoryのファイルはTask専用worktree内だけで変更する。main worktree、他Taskのworktree、Branch、IndexまたはCommitを変更しない。管理RepositoryBootstrap後の`AGENTS.md`、`PRODUCT.md`、`ARCHITECTURE.md`、`DECISIONS.md`および`tasks/TEMPLATE.md`は管理RepositoryのTask worktree内で変更する。Git管理外のTask実体`tasks/T-*.md`はワークスペースルートで更新し、管理RepositoryのCommitへ含めない。
6. **VERIFY**: Build → Test → Diagnose → Fix → Re-testの順で、Task専用worktree上の成果物をProjectに適した方法で検証する。文書変更などでBuildまたは実行Testが対象外の場合は、その理由をTaskに記録して静的検証を行う。判断待ちまたは検証未達の場合はレビュー状態へ進まず、Taskを`BLOCKED`にしてDesign Agentへ委ねる。
7. **COMMIT**: VERIFY合格後、REPORT前に、Repositoryごとに自Taskが変更したPathだけを明示的にStageして独立したCommitを作成する。Commit前に対象PathのDiffとStage内容を確認し、Commit後にTask worktreeがcleanであることを確認する。`git add .`、`git add -A`および無差別なWildcardを使用せず、他Taskまたは利用者の変更をCommit、Unstage、RevertまたはCleanupしない。
8. **REPORT**: Implementation、Branch / Worktree、Build Result、Test Result、Verification Result、Commit Result、Deviations、FindingsおよびGUI FeedbackをTaskに記録する。検証後の`ARCHITECTURE.md`更新およびDecision Verification更新はEngineering Agentが行う。Git変更がCommit済みでTask worktreeがcleanなことを確認し、検証に合格したTaskはGUI対象なら`GUI_REVIEW`、非GUI対象なら`ACCEPTANCE_REVIEW`へ変更する。Product Ownerの明示的な最終受入れ前に`DONE`へ変更してはならない。REPORT完了後に別Taskを取得しない。

## Git Commit and Integration

- Commit Messageは`<type>(<scope>): <日本語の要約> [T-xxxxx]`形式とし、基本typeは`feat`、`fix`、`refactor`、`docs`、`test`、`build`、`chore`とする。scopeはRepositoryまたは主要Componentを短く表す。
- Commit本文は`Why:`、`What:`、`Verify:`の英語見出しを維持し、各本文を日本語で記載する。実施していない検証を成功と記載せず、Secret、Credential、TokenまたはFlagを記載しない。Merge用Commitが必要な場合もTask IDと日本語説明を含める。
- `--amend`、rebase、force操作その他のHistory書換えを行わない。Engineering Agentは`git push`、force pushまたは自動Pushを行わない。
- GUI ReviewとProduct Ownerの最終受入れはTask BranchのCommitを対象とする。Review修正では同じTask Branchとworktreeを再利用し、VERIFY、追加CommitおよびREPORTを再実行する。
- Product Ownerの最終受入れ前に、Task Branchを最新local mainと統合可能な状態にする。local mainがBaseから進んでいる場合はrebaseせず、必要に応じてmainをTask Branchへmergeする。Conflict解消後はBuild、TestおよびVerificationを再実行し、GUIへ影響する場合はGUI Reviewも再実行する。受入れ対象Commit Hashが変わった場合は新しいHashをProduct Ownerへ提示する。未解消Conflict、設計判断または検証失敗がある場合は最終受入れを求めない。
- Product Ownerの最終受入れ後、Accepted Branch HEADとlocal mainが最終統合検証時から進んでいないことを確認する。各対象Repositoryのlocal mainを受入れ済みTask Branchへfast-forwardできる場合だけ統合し、Integrated local main CommitをTaskへ記録して`DONE`へ変更する。fast-forwardできない場合はmainを変更せず、Task Branchでの再統合と再検証へ戻る。
- Task Branchとworktreeは自動削除しない。GitHubへのPushはProduct Ownerが必要な時点で実行し、Pushは`DONE`条件に含めない。
- T-00009のCommit `e527bfce375da91ebe73acf2c4ed8da4e55885a6`（Subject: `update dashboard`）は本規約導入前の移行Commitとして維持し、Historyを書き換えない。

## BLOCKED Task Resume Sequence

実装または再検証作業を再開する`BLOCKED` Taskは、`BLOCKED` → 承認済み変更の反映 → `CLAIMED` → `RELOAD` → `VALIDATE` → `IMPLEMENTING`の順序で進める。この順序は省略または入替えできず、通常の再開で`READY`または`DESIGN`へ戻してはならない。Git Repositoryを変更するTaskは既存のTask Branchとworktreeを再利用し、通常は新しいBranchを作成しない。

1. **APPROVED UPDATE**: Design Agentが再開可否と必要な変更内容を決定する。Engineering AgentはTaskを`BLOCKED`のまま維持し、承認された阻害条件の解消に必要な永続ドキュメント、Task内容およびプロセス記録だけを反映する。コード実装は再開しない。
2. **CLAIMED**: 承認済み変更の反映後、Taskを`CLAIMED`へ変更する。同じEngineering Agentが再開する場合は既存の`Claimed By`と`Claimed At`を維持し、再開日時と再開判断をImplementationへ記録する。Product OwnerまたはDesign Agentが明示した代替Engineering Agentが再開する場合は、`Claimed By`を代替Agent識別名、`Claimed At`を新しいISO 8601時刻へ更新し、通常の取得報告と同等の再開報告をProduct Ownerへ行う。代替Engineering Agentも同じTask Branchとworktreeを引き継ぎ、Taskを自動的に奪取してはならない。
3. **RELOAD**: Task、Source文書、およびGit変更Taskでは既存Task Branch・worktree・Base main CommitをファイルとGitから再読込する。
4. **VALIDATE**: Status `CLAIMED`、Source、Dependencies、Requirements、Acceptance Criteria、Constraints、承認済み変更の反映結果、作業差分および既存Task Branch・worktreeの対応を再検証する。不合格ならTaskを`BLOCKED`へ戻し、Findingsに未解消条件、影響範囲および確認済みの事実を記録して、コード実装を再開しない。
5. **IMPLEMENTING**: 再VALIDATE合格後だけTaskを`IMPLEMENTING`へ変更し、コード実装または再検証作業を再開する。

再開後に変更または再検証を行ったGit変更Taskは、VERIFY合格後に新しいCommitを作成してREPORTする。既存Commitをamendせず、Task BranchのCommit履歴として追加する。

## GUI Feedback

- 画面、視覚表示、操作フローに影響する変更は`GUI_REVIEW`を経由する。
- GUI Feedbackには、確認した画面・状態・操作、期待結果、実測結果、未解決の指摘を記録する。Design Agentがこれを解釈・整理し、Product Ownerが最終受入れを判断する。
- GUIを持たない変更は、TaskのGUI Feedbackに「対象外」と理由を記録できる。
- GUI FeedbackでRequirementまたはArchitectureの判断が必要になった場合、Engineering AgentはTaskを`BLOCKED`にしてDesign Agentへ委ねる。
- GUI Review完了後、Design AgentがGUI Feedbackを解釈・整理し、未解決事項の有無と次の状態を決定する。実装修正または再検証が必要な場合、Engineering AgentはTaskを`BLOCKED`へ変更し、`BLOCKED Task Resume Sequence`に従って再開する。
- Git変更TaskのGUI Review修正では同じTask Branchとworktreeを再利用し、修正後にVERIFY、新しいCommitおよびREPORTを行う。受入れ対象Commit Hashが変わった場合はProduct Ownerへ提示する。
- 実装修正も再検証も不要で、Design Agentが既存Verificationを有効と判断して`ACCEPTANCE_REVIEW`への遷移だけを決定した場合、Engineering AgentはTaskを直接`ACCEPTANCE_REVIEW`へ変更する。この状態変更だけを実装再開として扱わず、`CLAIMED`または`IMPLEMENTING`への不要な遷移を行わない。

## AGENTS.md Change Governance

- `AGENTS.md`の変更は、開発プロセス上の最上位ルールを変更する行為であるため、Product Ownerの明示的承認なしに行えない。
- Design Agentは、変更理由、変更内容および影響する既存ルールをProduct Ownerへ提示する。
- Product Ownerが明示的に承認した後、Task Leadが`AGENTS.md`変更Taskを作成し、必要な事前SYNC、VALIDATEおよび`READY`公開を行う。
- Task Leadは`AGENTS.md`自体を変更しない。
- Engineering Agentが公開済みTaskをCLAIMし、`AGENTS.md`を変更、検証、報告する。
- 他のTask、設計または実装に対する承認を、`AGENTS.md`変更に対する黙示的承認として扱わない。

## Repository Boundaries

- Product Ownerによる初回Bootstrap後、`K3DF-local/`をプロジェクト管理Repositoryとする。管理Repositoryは`AGENTS.md`、`PRODUCT.md`、`ARCHITECTURE.md`、`DECISIONS.md`、`tasks/TEMPLATE.md`、`.gitignore`および承認済み管理文書をGit管理する。
- `tasks/TEMPLATE.md`はGit管理対象のTask Schemaとする。Task実体である`tasks/T-*.md`はローカル運用記録としてGit管理、GitHub共有、cloneによる復元およびWorkspace間同期の対象外とするが、既存Task File OwnershipとLifecycleは適用する。
- `repositories/`と`.worktrees/`は管理RepositoryのGit管理対象外とする。Product Repositoryは`repositories/K3DF/`、`repositories/K3AT/`、`repositories/K3Defnder-K3Atacker-infra/`および将来の`repositories/K3Ops/`に配置し、それぞれ独立したGit Repositoryとして扱う。
- Git Repositoryを変更するTaskの専用worktreeは、ワークスペース直下の`.worktrees/T-xxxxx/<Repository名>`を標準配置とする。Task BranchとworktreeはTask完了時に自動削除しない。
- 管理Repositoryの初回BootstrapはProduct Ownerだけが手動で行う。Task LeadとEngineering Agentは、`.git`の移動・作成・初期化、初回`.gitignore`調整、Branch作成、Stage、Commit、Remote設定またはPushを含むBootstrap操作を行わない。
- Product Ownerは初回Bootstrap時に`.gitignore`を調整し、`tasks/TEMPLATE.md`をGit管理対象、`tasks/T-*.md`、`repositories/`および`.worktrees/`をGit管理外とする。
- Bootstrap後、Design Agent、Task LeadおよびEngineering Agentは、管理Repositoryの存在、Repository境界、追跡対象、除外対象、現在BranchおよびWorking Treeを読み取り確認する。`tasks/TEMPLATE.md`が追跡され、`tasks/T-*.md`、`repositories/`および`.worktrees/`が管理対象外であることを確認してから通常運用へ移る。不合格の場合はRepositoryを変更せず、担当Roleの規則に従って報告または`BLOCKED`とする。
- Public管理RepositoryへCommitする前に、対象全体にSecret、Credential、Token、Flag、`.env`内容、実環境の管理接続情報または認証情報付きURLが含まれず、Task実体、Product Repository、worktreeおよび個人メモが含まれないことを確認する。
- 各Product Repositoryのコード、Docker構成、README、依存関係は、公開済みTaskがない限り変更しない。
