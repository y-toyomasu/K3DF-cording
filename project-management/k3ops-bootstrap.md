# K3Ops Repository Bootstrap Guide

## 対象者と目的

この手順はProduct Owner専用の一回限りのBootstrap手順です。管理Repository rootから見た`repositories/K3Ops`を独立Git Repositoryとして初期化し、Engineering AgentがTask Branchと専用worktreeを作成できるcleanな`main`と初期Commitを用意します。Task LeadとEngineering AgentはこのBootstrapを実行しません。

## 事前条件

- Windows PowerShellを使用し、管理Repository rootへ移動済みとします。
- Gitが利用可能であることを確認します。
- 対象Pathが存在しないことを確認します。
- 対象Pathが既に存在する、空でない、またはGit Repositoryである場合は停止します。削除、上書きまたは再初期化は行いません。
- Docker Desktop起動はT-00020の実装検証には必要ですが、Git Bootstrap自体の必須条件ではありません。

## 実行手順

1. Gitが認識する管理Repository rootと、そこからの対象Pathを変数へ設定します。

   ```powershell
   $ManagementRoot = (git rev-parse --show-toplevel).Trim()
   $K3OpsPath = Join-Path $ManagementRoot 'repositories\K3Ops'
   ```

   `git rev-parse`が失敗する、または`$ManagementRoot`が空文字の場合は停止します。

2. 対象Pathの存在を確認します。

   ```powershell
   Test-Path -LiteralPath $K3OpsPath
   ```

   結果が`False`であることを確認します。`True`なら停止します。

3. Directoryを作成します。

   ```powershell
   New-Item -ItemType Directory -Path $K3OpsPath
   ```

4. `main`を指定してGitを初期化します。

   ```powershell
   git -C $K3OpsPath init -b main
   ```

5. Git identityを確認します。

   ```powershell
   git -C $K3OpsPath config user.name
   git -C $K3OpsPath config user.email
   ```

   値が空ならBootstrapを止め、Product Ownerが自身の正しいIdentityを設定してから再開します。本手順では架空のNameまたはEmailを提示しません。

6. 空の初期Commitを作成します。

   ```powershell
   git -C $K3OpsPath commit --allow-empty -m "chore: bootstrap K3Ops repository"
   ```

7. Bootstrap結果を検証します。

   ```powershell
   git -C $K3OpsPath branch --show-current
   git -C $K3OpsPath status --short --branch
   git -C $K3OpsPath rev-parse HEAD
   ```

   期待結果は次のとおりです。

   - `branch --show-current`が`main`を返す。
   - `status`が`## main`であり、追跡差分がない。
   - `rev-parse HEAD`が初期Commit Hashを返す。

## 完了後

- Product OwnerはTask Leadへ「K3Ops Bootstrap完了」、Repository Path、Branch `main`、初期Commit Hashおよびclean確認を報告します。
- Remote作成、Push、アプリFile作成、Task Branch、worktree、依存導入およびDocker Buildは行いません。
- T-00020が`READY`公開されるまでK3Ops Repositoryへ追加変更しません。

## 異常時

- Directoryが既存、Git init失敗、Identity未設定、Commit失敗、Branchが`main`でない、またはstatusがdirtyの場合は停止します。
- `rm`、`Remove-Item`、`git reset --hard`、既存Repositoryの再初期化などの破壊的な復旧を行いません。
- Error全文と実行済み段階を報告し、判断を待ちます。
