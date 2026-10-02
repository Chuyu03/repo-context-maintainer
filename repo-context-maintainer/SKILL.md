---
name: repo-context-maintainer
description: Close out repository work, review Git changes, prepare Conventional Commits, coordinate explicitly authorized commits or GitHub publication, and maintain AGENTS.md, Codex Skills, or project memory. Use for repository closeout and context-maintenance requests that require strict separation between inspection, local Git writes, public writes, and task UI actions.
---

# Repo & Context Maintainer

## Operating Contract

Treat the working tree as the source of truth, Git as the version record, and
GitHub as an optional publication surface. Begin read-only. A closeout request
starts review and preparation; it does not authorize context writes, Git
mutations, publication, deployment, or task/thread UI changes.

Keep these layers separate:

1. summarize completed work and durable evidence;
2. inspect and propose context updates;
3. apply only concretely approved context updates;
4. prepare Git scope and a Conventional Commit message;
5. perform each authorized Git or publication layer separately.

Read [references/modes.md](references/modes.md) for the matching operating mode.
Read [references/context-update-policy.md](references/context-update-policy.md)
before non-trivial context proposals or edits. Read
[references/workflow.md](references/workflow.md) for commit, branch, tag, and
release conventions. Read
[references/platform-examples.md](references/platform-examples.md) only when a
platform-specific release artifact needs special handling.

## Establish the Baseline

1. Confirm the absolute project root.
2. If it is a Git repository, run only the read-only Git checks needed for the
   request, such as `git status`, `git diff`, `git diff --staged`,
   `git log --oneline -n 5`, `git branch`, and `git remote -v`.
3. If it is not a Git repository, say that Git inspection is not applicable.
   Never initialize one unless the user explicitly authorizes that action.
4. Record pre-existing staged, unstaged, and untracked changes before editing.
   Do not attribute them to the current task or mix them into a later commit.
5. For context work, run `scripts/context_inventory.py <project-root>` when
   practical. Its output redacts absolute root paths by default. Relative paths
   and file names may still be sensitive; review the output before sharing. Treat
   `truncated: yes` or any scan error as incomplete evidence, not as proof that
   a context surface is absent. Use `--show-absolute-paths` only when the user
   needs local path detail and the output will remain private.

## Context Boundaries

- `AGENTS.md` holds repository-local operating guidance.
- A Skill holds a reusable procedure, its triggers, checks, and resources.
- Project memory holds concise, durable cross-session facts and decisions.

Use explicit user requirements as evidence of intent. Require observed or
verified evidence for claims about technical behavior. Do not store secrets,
personal data, raw logs, or speculation. Follow the active platform's memory
write policy; a closeout request alone is not memory-write approval.

Task lifecycle wording does not authorize archiving, hiding, deleting, moving,
or otherwise changing a task/thread in the UI. Explain the exact effect and
obtain fresh confirmation for that specific UI action.

## Git and Publication Gates

- Inspection is the default. Do not run `git add`, `git commit`, `git push`,
  `git pull`, `git merge`, `git rebase`, `git reset`, `git restore`,
  `git clean`, `git checkout`, `git switch`, or tag commands without the
  matching explicit authorization.
- Before staging or committing, show the exact scope, distinguish pre-existing
  work, and propose a message. A commit is local; a push is public or remote.
- Require separate authorization for pushing a branch, creating or pushing a
  tag, creating or changing a Release, uploading assets, opening a PR, or
  deploying.
- Do not modify `.git/`, secrets, private configuration, dependency locks, or
  unrelated files unless the requested work specifically requires it.

When remote GitHub metadata or an authorized GitHub action is needed, detect
available capabilities first. Prefer a dedicated GitHub connector when present;
otherwise use an already available authenticated browser or an approved local
CLI. Do not require a plugin installation, solicit credentials, or claim a
remote action succeeded without readback. If no safe capability is available,
prepare exact manual steps and stop at the relevant gate.

## Validation and Handoff

Validate changed context files with the smallest relevant checks. When this
Skill changes, run the bundled inventory tests and the available Skill
validator, then check UTF-8, YAML/frontmatter, and linked resources.

Report the project path, file-by-file changes, verification, current Git state,
pre-existing changes, skipped context surfaces, external actions, and a
suggested commit message. For failures, include the command, stage, key error,
likely cause, and whether it affects safety or the current changes.
