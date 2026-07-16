# Context Update Policy

Use this reference when deciding whether and how to update `AGENTS.md`, Skills, or project memory during repo closeout or explicit context-maintenance work.

## Operating Model

Use a two-phase workflow:

1. Read-only assessment: inspect current context surfaces and produce a concrete proposal.
2. Approved update: edit only the context surfaces and exact scope the user approved.

Do not write context updates during assessment. A generic closeout request starts the review; it is not blanket approval for context writes unless the user has already approved the same concrete changes in the current conversation.

## Surface Selection

Update `AGENTS.md` when the information is repository-local operating guidance:

- Required pre-edit or pre-release checks.
- Validation commands and known environment constraints.
- Directories, generated outputs, or archives to avoid.
- Repo-specific launch, build, release, or closeout workflows.
- User preferences that should affect every future task in this repository.

Update a Skill when the information is procedural and reusable:

- The user wants a repeatable workflow.
- Future requests should trigger specialized behavior by name or description.
- The workflow needs ordered steps, validation, bundled scripts, references, templates, or examples.
- The change improves an existing Skill without creating unrelated behavior.

Update project memory when the information is durable across sessions:

- Stable project facts or user preferences.
- Verified environment fixes likely to recur.
- Important decisions and evidence.
- Known pitfalls future agents should check early.

Prefer project memory for facts that should be discoverable even when future work starts outside the repository checkout.

## Missing-Surface Initialization

Treat a missing `AGENTS.md` or project-scoped memory entry as an initialization case, not as evidence that the surface is unnecessary. Each project may maintain its own repository-local instructions and project-scoped memory.

When the relevant write is approved or permitted by the active policy:

- Create `AGENTS.md` at the target project's effective root when the dialogue contains durable project-local operating rules, constraints, validation steps, or user preferences.
- Create the first project-scoped memory entry in the active platform's allowed location when the dialogue contains durable project facts, confirmed decisions, recurring pitfalls, or verified workflows.
- Do not skip creation solely because related reusable guidance also exists in a Skill. Store the project-specific fact or constraint in the project surface and the reusable procedure in the Skill; avoid verbatim duplication when a concise surface-specific formulation is enough.
- Do not create an empty placeholder or generic boilerplate. A new surface must contain concrete project-specific context supported by the dialogue.

## Evidence Standard

Prioritize context that the dialogue clearly establishes:

- Treat the user's explicit requirements, preferences, constraints, corrections, and confirmed decisions as authoritative evidence about the user's intent. These do not require a completed real-world rehearsal before being recorded as requirements or decisions.
- Treat observed command results, validated fixes, and successfully exercised workflows as verified technical experience.
- Do not turn a requested design or intended workflow into a claim that it has already been technically verified. Record it as a requirement or decision, and verify behavior separately when that distinction matters.
- Exclude transient logs, speculative conclusions, superseded assumptions, and details that are not useful in future project work.

## Caution Levels

Use different caution levels for different context surfaces.

### 1. General global memory: highest caution

Use this for rules or preferences that apply across many projects, many future tasks, or the user's general agent behavior.

Write or update only when:

- The user explicitly asks for that global memory update, or
- The agent judges the memory is important and broadly reusable, then explains why, shows the exact proposed content, and receives user approval.

Do not silently promote a project-specific lesson into general global memory.

### 2. Project-scoped memory in global/platform storage: medium caution

Use this for durable facts that describe a specific named project, workspace, or repository but are stored in a global or platform memory system for future retrieval.

This does not need the same highest caution as general global memory, but it must:

- Be clearly scoped to the project name, path, or repository.
- Avoid wording that could affect unrelated projects.
- Be verified, concise, and non-sensitive.
- Follow the active platform memory write policy and any approval requirements.

If a project-scoped memory could change behavior in other projects, treat it as general global memory instead.

### 3. Project-local rules: lower caution, still narrow

Use `AGENTS.md` or project-local Skill files for rules that should apply inside the current project only.

This is less sensitive than global memory because it is local, visible, and easier to review, but still:

- Inspect existing files first.
- Keep edits narrowly tied to the approved task.
- Avoid broad global preferences unless they are necessary for this project.
- Do not add secrets, raw logs, or speculative claims.

## Replacing or Removing Context

Replace existing context only when it is stale, misleading, duplicated in the same surface, unsafe, obsolete, or contradicted by verified project evidence.

Remove context only when removal is explicitly approved or required because the current text is unsafe or actively harmful. Explain the reason in the proposal and final report.

When uncertain, propose a short scoped addition instead of rewriting a whole file.

## Memory Safety

Follow the active platform memory policy first.

Write project memory only when the user explicitly approves it or the platform policy already permits the write. If the platform requires append-only update notes, write a small note there instead of editing generated memory registries directly.

Never store:

- Secrets, tokens, private keys, certificates, passwords, or private config values.
- Personal data not needed for future project work.
- Raw logs when a concise durable summary is enough.
- Claims that have not been verified or are not clearly labeled as uncertain.

## Good Context

Good context is short, project-specific, supported by explicit user intent or verified project evidence, actionable by a future agent, and easy to update or remove later.

Weak context is a task transcript, a generic coding preference, a TODO with no durable lesson, or a guess about the user's intent.

## Proposal Shape

Use this shape before editing:

```text
Project path:
Inspected:
Captured:
Proposed changes:
- AGENTS.md:
- Skill:
- Project memory:
Skipped:
Approval needed:
```

If no context update is justified, say so and explain why.

## Update Report Shape

Use this shape after approved edits:

```text
1. Project absolute path:
2. Files changed, added, or deleted:
3. Context surface summary:
   - AGENTS.md:
   - Skill:
   - Project memory:
4. File-by-file details and purpose:
5. Validation commands and results:
6. Current Git status:
7. Suggested commit message:
```

For skipped surfaces, include the reason. If the update changes a page, API, script, app launch flow, or user-visible behavior, also include local run/open instructions and manual verification steps.
