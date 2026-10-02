# Operating Modes

Use the safest mode that matches the request. Authorization for one mode or
mutation does not authorize another.

## Repository Closeout

Use when the user asks to close out completed repository work, summarize a
development session, or prepare version maintenance.

1. If an earlier closeout summary is visible in the same task, use it as the
   de-duplication baseline and focus on later work.
2. Summarize what changed, what was verified, what remains, and which changes
   predated the task.
3. Extract durable, evidence-backed learnings. Ignore transient logs, secrets,
   and speculation.
4. Inspect `AGENTS.md`, relevant Skills, and project-memory candidates when the
   request includes context maintenance. A missing surface is an initialization
   candidate, not automatic permission to create it.
5. Propose context changes by surface. Apply only changes already approved at
   that concrete scope.
6. Organize the Git diff and propose a Conventional Commit message. Stop before
   staging unless staging is explicitly authorized.
7. Keep branch push, tag, Release, PR, asset upload, and deployment behind
   separate publication approvals.

## Context Maintenance Proposal

Use when the user wants to create, revise, or audit `AGENTS.md`, a Skill, or
project memory but has not approved exact edits.

1. Identify the project root and requested surfaces.
2. Run `scripts/context_inventory.py <project-root>` and inspect its completeness
   fields. Do not treat truncated or error-bearing output as complete.
3. Read existing relevant context and
   [context-update-policy.md](context-update-policy.md).
4. Report what was inspected, what should be captured, proposed changes grouped
   by surface, intentionally skipped updates, and the approval needed.
5. Stop after the proposal.

## Approved Context Update

Use only after exact context edits are approved.

1. Reconfirm the root and Git baseline.
2. Change only the approved surfaces. Create a missing standard surface only if
   creation was included in the approval and there is concrete content for it.
3. Do not install Skills globally, add hooks or automation, or change unrelated
   project code.
4. Rerun inventory when useful and validate every changed Skill or instruction
   file.
5. Report changes and intentional skips by context surface.

## Organize Changes Without Committing

1. Inspect status and relevant staged and unstaged diffs.
2. Group files by purpose and risk; separate staged, unstaged, untracked, and
   pre-existing work.
3. Recommend one Conventional Commit message, or a split only when changes have
   genuinely independent intent.
4. Do not mutate Git.

## Commit Authorized Changes

1. Re-run status and diff immediately before mutation.
2. Confirm the exact approved scope. If unrelated or pre-existing changes are
   inseparable and scope is unclear, ask one concise question.
3. Stage only that scope and re-read the staged diff.
4. Commit with a message matching the actual diff.
5. Do not push without separate authorization. Report the commit and new status.

## Publish to GitHub

1. Verify branch, commits, remote, status, and the exact public payload.
2. Detect an available GitHub capability as described in `SKILL.md`; absence of
   a connector is not permission to install one or request credentials.
3. Obtain separate authorization for branch push, tag creation/push, Release
   creation/update, asset upload, PR creation, and deployment.
4. Read back every remote mutation. Keep commit, tag, and Release outcomes
   distinct in the report.
