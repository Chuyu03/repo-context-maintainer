---
name: repo-context-maintainer
description: '整理 Git/GitHub 版本维护、任务收尾和项目上下文维护流程。Use when the user asks to review or summarize Git changes, generate a Conventional Commits commit message, prepare or perform an explicitly requested local commit, push to GitHub, prepare release notes, organize APK release materials, publish a GitHub tag or Release, update AGENTS.md, update or audit Codex Skills, capture durable project memory, or decide whether context should be updated after project work while preserving strict Git and publication safety boundaries. Use also for final-turn prompts such as "对话完结，总结优化和改动，提炼项目记忆，检查 Skill 是否需要优化，有 Git 则准备 commit/push", "Repo 管理", or context-maintenance closeout requests to run an interactive closeout flow: summarize completed work, inspect context surfaces, propose or apply only approved context changes, then organize Git changes and request confirmation before any staging, commit, or publication.'
---

# Repo & Context Maintainer

## Core Rule

Treat the project working tree as the source of truth, Git/VSCode Source Control as the version record, and GitHub as the public publishing surface. Default to non-mutating analysis unless the user explicitly asks to commit, push, tag, or create a release.

For task-end closeout, keep context maintenance and version maintenance as separate layers: first summarize completed work and durable learnings, then inspect and propose context changes across `AGENTS.md`, Skills, and project memory, then apply only context changes the user has approved with concrete scope, then prepare Git scope and commit message. Do not let a closeout prompt override confirmation gates for context writes, `git add`, `git commit`, `git push`, tags, releases, PRs, deployments, or other public operations.

Treat Thread/task lifecycle management as work-summary, context-maintenance, and version-closeout language only. It never authorizes archiving, hiding, closing, deleting, moving, or otherwise changing a task/thread in the Codex UI. Even when the user mentions a UI lifecycle action, first explain the exact UI effect and obtain fresh explicit confirmation for that specific task and action; never infer permission from closeout wording, task completion, a default-flow request, or past behavior.

When detailed release conventions, commit types, branch names, or APK publication rules are needed, read `references/workflow.md`.

When deciding whether to update `AGENTS.md`, Skills, or project memory, read `references/context-update-policy.md` before making non-trivial proposals or edits.

## Start Every Task

1. Confirm the project absolute path with the shell's current working directory.
2. If the directory is a Git repository, run only the needed read-only Git inspection commands first:
   - `git status`
   - `git diff`
   - `git diff --staged`
   - `git log --oneline -n 5`
   - `git branch`
   - `git remote -v`
3. If the directory is not a Git repository, state that Git inspection is not applicable and do not initialize Git unless the user explicitly asks.
4. Record the pre-task working tree state before making any requested edits. Distinguish changes that existed before the task from files changed during the task.
5. For context-maintenance work, inspect existing context artifacts before proposing changes. Prefer running `scripts/context_inventory.py` against the target project with the active Python executable. If `python` is not on PATH, use the available bundled or environment Python.

## Mode Selection

Use the safest matching mode from the user's wording.

### Conversation Closeout Repo Management

Use this mode when the user says "对话结束。利用 repo-context-maintainer Skill 做 Repo 管理。", "对话结束，做 Repo 管理", "对话完结，总结优化和改动，提炼项目记忆，检查 Skill 是否需要优化，有 Git 则准备 commit/push", or an equivalent final-turn task closeout request.

Treat that phrasing as an explicit request to start the interactive closeout review, not as blanket permission to mutate Git or publish to GitHub:

For repeated closeout in the same thread, first look for the latest prior `repo-context-maintainer` closeout summary in the visible conversation. If found, treat it as the closeout baseline: use earlier content only for background and de-duplication, and make the primary closeout scope the turns after that baseline. Do not repeat already-captured summaries, Git scope notes, or context-update proposals unless later turns materially refine, correct, or invalidate them. If the prior closeout is not visible or the boundary is ambiguous, state the limitation and ask for the previous closeout summary only when the boundary affects correctness.

1. Summarize the completed work: what changed, what was verified, what remains, and what was pre-existing when known.
2. Extract durable learnings from evidence in the dialogue. Treat the user's explicit requirements, preferences, constraints, and confirmed decisions as authoritative evidence about intent; require verification for technical behavior and results. Ignore transient logs, one-off implementation details, secrets, and speculative conclusions.
3. Inspect context surfaces when the closeout includes project memory, `AGENTS.md`, Skill optimization, durable lessons, or equivalent wording. Run the context inventory script when available, read existing `AGENTS.md` or Skill files as needed, and group findings by surface. Treat a missing project `AGENTS.md` or project-memory entry as an eligible initialization case, not as a reason to skip that surface.
4. Propose context changes first unless the user has already approved the same concrete edits in the current conversation. Apply only approved updates, and follow the active memory policy exactly for project-memory writes.
5. Inspect relevant existing Skills when the dialogue exposes a reusable workflow gap. Patch only the relevant Skill when that exact Skill update was approved; otherwise propose the Skill change and wait.
6. Propose a new Skill only when the workflow is clearly reusable and distinct from existing Skills. Do not force a Skill idea for ordinary project notes or one-off preferences.
7. Organize current Git changes and recommend a Conventional Commits scope/message. Do not commit during this step.
8. Ask the user to confirm or edit the exact file scope and commit message before running `git add` or `git commit`.
9. Require separate explicit approval before `git push`, tag creation, GitHub Release operations, PR creation, deployment, or any other public operation. If publication was not approved, stop after the local preparation or approved local commit and report the next step.

Keep the flow interactive. Do not skip the message confirmation. Do not create tags or GitHub Releases during this flow unless the user explicitly asks for tag or Release creation and confirms that publication layer.

### Context Maintenance Proposal

Use this mode when the user asks to create or revise `AGENTS.md`, update a Skill, capture durable project memory, audit whether context should be updated, or run a context-maintenance closeout without already approving exact edits.

Procedure:

1. Identify the target project root and requested context scope.
2. Run read-only inventory when possible: `python /path/to/repo-context-maintainer/scripts/context_inventory.py /path/to/project`.
3. Inspect existing `AGENTS.md`, relevant Skill files, and project-memory candidates before proposing changes. Record missing `AGENTS.md` or project-memory surfaces as candidates that may be initialized when the dialogue contains suitable durable project context.
4. Read `references/context-update-policy.md` for surface-selection rules.
5. Report inspected surfaces, durable learnings worth capturing, proposed changes grouped by `AGENTS.md`, Skill, and project memory, skipped updates, and approval needed.
6. Stop after the proposal unless the user has already approved the same concrete changes.

### Approved Context Update

Use this mode only after the user approves exact context changes.

Procedure:

1. Reconfirm the project root and current baseline before editing.
2. Make only the approved edits to `AGENTS.md`, relevant Skill files, or the active platform's allowed project-memory update location. If an approved target surface does not exist, create it in the standard effective location instead of skipping it solely because it is new.
3. Do not create hooks, background automation, global installs, unrelated project code, or new Skills unless explicitly included in the approved scope.
4. Validate by rereading changed files, rerunning inventory when useful, and running the Skill validator when a Skill changed and a validator is available.
5. Report what changed, what was skipped, and why for each context surface.

### 1. Organize Changes, Do Not Commit

Use this mode for requests such as "整理本轮变更", "给我一个 commit message", "review current Git changes", or any ambiguous version-maintenance request.

Procedure:

1. Inspect status and diffs with read-only Git commands.
2. Summarize changed files by purpose and risk.
3. Separate staged, unstaged, untracked, and pre-existing changes when the information is available.
4. Recommend one Conventional Commits message, plus alternatives only when the change clearly spans multiple commit types.
5. Do not run `git add`, `git commit`, `git push`, tag commands, GitHub Release operations, or destructive cleanup.

### 2. Commit Current Changes

Use this mode only when the user explicitly asks to commit, submit, or record the current changes.

Procedure:

1. Re-run status and diff checks immediately before any mutation.
2. Confirm the intended scope from the user's request. If unrelated or pre-existing changes are mixed in and scope is unclear, ask one concise question before staging.
3. Stage only files in the approved scope.
4. Commit with a Conventional Commits message that matches the actual diff.
5. Do not push unless the user explicitly asks for push or GitHub publication.
6. Report the exact commit command result and the new Git status.

### 3. Publish to GitHub

Use this mode only when the user explicitly asks to push, publish, create a tag, draft or create a GitHub Release, or prepare GitHub-facing release notes.

Procedure:

1. Verify the local branch, latest commits, remotes, and current status.
2. Require explicit authorization before each publication layer:
   - push branch
   - create or push tag
   - create or update GitHub Release
3. Keep commit, tag, and release as distinct steps in the explanation and final output.
4. Use the GitHub plugin when GitHub PR, issue, release, or remote metadata context is needed. Use local `git` or `gh` only when appropriate and authorized.
5. For APK or app release requests, organize artifact names, version notes, README updates, and release notes, but do not upload or publish artifacts without explicit instruction.

## Context Maintenance Rules

- Treat `AGENTS.md` as repository-local operating guidance for future agents: pre-edit checks, validation commands, directories to avoid, local workflows, and repo-specific user preferences.
- Treat Skills as reusable workflows with triggers, ordered steps, validation rules, references, scripts, templates, or assets.
- Treat project memory as durable cross-session facts, decisions, pitfalls, and verified workflows. Classify memory writes before proposing or applying them: general global memory is highest caution; project-scoped memory stored in a global/platform memory system is medium caution and must be tightly scoped to the named project; project-local `AGENTS.md` rules are lower caution but still require review and narrow edits.
- Allow every project to have its own `AGENTS.md` and project-scoped memory. Their absence is not evidence that creation would be redundant; initialize either surface when approved or permitted and when the dialogue contains durable project-specific content. Do not create empty boilerplate.
- Prioritize context that is clearly established in the dialogue: explicit user requirements and confirmed decisions are valid durable evidence without requiring a real-world rehearsal, while claims about technical behavior or outcomes still require verification or clear uncertainty labeling.
- Follow the active memory write policy; if it requires append-only notes or explicit approval, do not bypass it.
- Prefer concise, evidence-based context. Do not store secrets, credentials, private tokens, raw logs, personal data, or unverified claims.
- Replace or remove context only when it is stale, misleading, duplicated in the same surface, unsafe, obsolete, or contradicted by verified evidence.
- Keep Skill bodies concise. Move detailed policy, examples, or templates into directly linked files under `references/` when they would otherwise bloat `SKILL.md`.
- If a context update affects `AGENTS.md`, a Skill, or project memory, final reporting must include a per-surface summary that states what was added, changed, deleted, or intentionally skipped.

## Git Safety Boundaries

- Default allowed Git commands are inspection-only: `git status`, `git diff`, `git diff --staged`, `git log --oneline -n 5`, `git branch`, and `git remote -v`.
- Do not run `git add`, `git commit`, `git push`, `git pull`, `git merge`, `git rebase`, `git reset`, `git clean`, `git checkout`, `git switch`, tag commands, or GitHub Release operations unless the user explicitly asks for that action.
- Do not modify `.git/`.
- Do not modify `.env`, `.env.local`, secrets, certificates, keystores, tokens, or private config files.
- Do not modify dependency or lock files unless the current task requires dependency changes. Explain any required dependency file change in the final output.
- Do not delete files unless explicitly requested or required for the task. Explain required deletions.
- Do not run whole-project formatting unless the user explicitly requests it.

## Failure Handling

If any command fails, report:

- the exact command
- the stage where it failed
- the key error text
- the likely cause
- whether it appears related to the current changes

Stop before the next mutating step if the failure affects safety, scope, or publication correctness.

## Final Output Format

Match the user's requested language and output shape. If no stricter format was requested, answer the user's main question first, then include the engineering handoff details:

1. 项目绝对路径
2. 本轮实际修改、新增或删除的文件，使用绝对路径；如果没有修改业务文件，也明确说明
3. 每个文件具体改了什么，以及修改目的
4. 验证命令与结果；如果失败，说明失败命令、关键报错、可能原因、是否与本轮修改有关
5. 当前 Git 状态；区分本轮修改与修改前已存在的未提交内容
6. 公众平台、外部服务与费用核查；说明是否执行发布、上传、部署、外部写入或付费操作
7. 建议的 commit message，只给建议，不要自动 commit，使用 Conventional Commits 风格
8. 如果本轮涉及项目记忆、`AGENTS.md` 或 Skill，说明检查了哪些上下文表面、实际改了什么、跳过了什么以及原因，并按 `AGENTS.md`、Skill、project memory 分组

If the task changes pages, APIs, scripts, app launch behavior, release artifacts, or user-visible behavior, also include:

- 如何本地运行或打开
- 我下一步应该如何手动验证
