# Repo Context Maintainer

An installable Codex Skill for evidence-based repository closeout, Git change
organization, and durable project-context maintenance. It keeps inspection,
context edits, local commits, remote pushes, tags, Releases, and task UI actions
behind distinct authorization boundaries.

The repository also includes a read-only inventory CLI that finds likely
`AGENTS.md`, Skill, and project-memory surfaces without reading their contents.

## Highlights

- Separates repository summary, context proposals, approved edits, Git writes,
  and public publication.
- Distinguishes pre-existing worktree changes from changes made in the current
  task.
- Routes durable information to `AGENTS.md`, reusable Skills, or project memory.
- Uses GitHub integrations only when available; an integration is not a hard
  dependency and remote success always requires readback.
- Redacts project and Git root paths from inventory output by default.
- Reports inventory scan limits and filesystem errors instead of silently
  treating partial evidence as complete.
- Uses only the Python standard library at runtime.

## Repository Layout

```text
repo-context-maintainer/
  SKILL.md
  agents/openai.yaml
  references/
  scripts/context_inventory.py
tests/
```

## Install the Skill

Copy the `repo-context-maintainer` directory into your Codex Skills directory.
For example, place it at:

```text
$CODEX_HOME/skills/repo-context-maintainer
```

Restart or reload Codex as required by your client. Installation does not grant
permission to commit, push, publish, change task state, or write project memory.

## Inventory CLI

Python 3.11 or 3.12 is supported.

```powershell
python repo-context-maintainer/scripts/context_inventory.py C:\path\to\project
python repo-context-maintainer/scripts/context_inventory.py C:\path\to\project --json
```

Default output uses `<project-root>` and `<git-root>` placeholders. Reveal local
absolute roots only for private diagnostics:

```powershell
python repo-context-maintainer/scripts/context_inventory.py C:\path\to\project --show-absolute-paths
```

Use `--max-files` with a positive integer to bound the scan. Always inspect the
`scanned`, `truncated`, and `errors` fields. A truncated scan or any walk error is
incomplete evidence. Directory symlinks and Windows junctions are not followed,
and linked files are not classified as context surfaces.

The tool inventories paths only. It does not open discovered context files,
modify the project, initialize Git, or contact GitHub.

## Development and Validation

```powershell
python -m compileall -q repo-context-maintainer tests
python -m unittest discover -s tests -v
```

The CI workflow runs the same checks on Windows and Linux with Python 3.11 and
3.12 under read-only repository permissions.

## Security and Privacy

Read [SECURITY.md](SECURITY.md) before reporting a vulnerability. Do not include
credentials, private repository content, absolute local paths, or raw project
memory in public reports.

This project is licensed under the [MIT License](LICENSE).

---

# Repo Context Maintainer（中文）

这是一个可安装的 Codex Skill，用于基于证据完成仓库收尾、整理 Git 变更，以及维护可长期复用的项目上下文。它严格区分只读检查、上下文写入、本地提交、远程推送、Tag、Release 与任务界面操作，不把一次授权扩展成其他操作权限。

仓库同时提供只读清单 CLI，用于发现可能存在的 `AGENTS.md`、Skill 和项目记忆表面，但不会读取这些文件的正文。

## 主要特点

- 分离项目总结、上下文提案、已批准编辑、Git 写入和公开发布。
- 区分任务开始前已有的工作树改动与本轮新增改动。
- 按用途将持久信息路由到 `AGENTS.md`、可复用 Skill 或项目记忆。
- GitHub 集成仅在能力可用时采用，不构成硬依赖；远程写入必须回读确认。
- 清单输出默认隐藏项目根目录与 Git 根目录的绝对路径。
- 明确报告扫描数量、截断状态和文件系统错误，避免把不完整清单误当成完整结果。
- 运行时仅依赖 Python 标准库。

## 安装

将 `repo-context-maintainer` 目录复制到 Codex Skills 目录，例如：

```text
$CODEX_HOME/skills/repo-context-maintainer
```

根据客户端要求重新加载 Codex。安装 Skill 不代表授权 commit、push、发布、改变任务状态或写入项目记忆。

## 使用清单 CLI

支持 Python 3.11–3.12：

```powershell
python repo-context-maintainer/scripts/context_inventory.py D:\path\to\project
python repo-context-maintainer/scripts/context_inventory.py D:\path\to\project --json
```

默认输出用 `<project-root>` 和 `<git-root>` 占位。仅在输出保持私密且确有诊断需要时，显式加入 `--show-absolute-paths`。

`--max-files` 必须是正整数。使用结果时必须检查 `scanned`、`truncated` 和 `errors`；出现截断或遍历错误时，结果不能证明某类上下文不存在。工具不会跟随目录符号链接或 Windows junction，也不会把链接文件分类为上下文表面。

该工具只盘点路径，不读取发现文件的内容、不修改项目、不初始化 Git，也不连接 GitHub。

## 开发验证

```powershell
python -m compileall -q repo-context-maintainer tests
python -m unittest discover -s tests -v
```

CI 以只读仓库权限在 Windows 和 Linux 的 Python 3.11、3.12 上运行同样的检查。

安全问题请参阅 [SECURITY.md](SECURITY.md)。公开报告中不要包含凭据、私有仓库内容、本机绝对路径或原始项目记忆。

本项目采用 [MIT License](LICENSE)。
