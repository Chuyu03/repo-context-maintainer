# Git and Release Workflow Reference

Use this reference when choosing commit types, branch names, or tag and release
boundaries. For optional platform-specific artifact examples, read
`platform-examples.md` only when relevant.

## Conventional Commits Types

| Type | Use for |
| --- | --- |
| `feat` | New user-facing behavior, new workflow, new capability |
| `fix` | Bug fix, broken behavior correction, regression fix |
| `refactor` | Internal code restructuring without behavior change |
| `test` | Test additions, test fixes, test infrastructure |
| `docs` | Documentation-only changes |
| `build` | Build system, packaging, dependency, CI, or release artifact pipeline changes |
| `chore` | Maintenance that does not fit the above, including metadata or housekeeping |

Prefer one commit type that reflects the primary user-visible purpose. If unrelated changes are mixed together, recommend separate commits instead of forcing one broad message.

## Branch Naming

- `feature/<short-topic>` for new capabilities.
- `fix/<short-topic>` for bug fixes.
- `release/<version-or-date>` for release preparation.

Keep branch names lowercase, concise, and hyphen-separated. Do not create or switch branches unless the user explicitly asks.

## Commit, Tag, and GitHub Release Boundaries

- Commit records a local project state.
- Tag marks a specific commit as a version point.
- GitHub Release publishes notes and optional artifacts around a tag.

Do not collapse these layers in the explanation. A push does not imply a tag. A tag does not imply a GitHub Release. A release does not imply uploading artifacts unless the user explicitly asks.

## Release Notes and Artifacts

- Separate user-visible changes, fixes, known issues, and verification.
- Document only stable setup, installation, and release behavior in a README.
- Verify an artifact's version, variant, source revision, path, and digest when
  those facts are available and material.
- Do not upload, replace, or delete artifacts without explicit authorization for
  that exact public payload.
