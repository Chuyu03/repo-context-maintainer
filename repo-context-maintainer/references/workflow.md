# Git and Release Workflow Reference

Use this reference when choosing commit types, branch names, tag and release boundaries, or APK publication notes.

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

## APK and Release Notes

When organizing Android APK or app release materials:

- Verify the version name, version code, build variant, and artifact path when available.
- Keep APK file names traceable with app name, version, build type, and date when the project convention allows it.
- Release notes should separate user-visible changes, fixes, known issues, and verification performed.
- README changes should only document stable user-facing setup, installation, or release instructions.
- Do not upload APKs, attach artifacts, publish releases, or overwrite release notes without explicit instruction.
