# Security Policy

## Supported versions

Until the project reaches 1.0, security fixes are provided for the latest
published release and the current default branch.

## Security properties

The inventory CLI is designed to be read-only. It must:

- stay within the requested project root and not follow directory symlinks or
  Windows junctions;
- avoid reading the contents of discovered context files;
- redact project and Git root paths unless absolute paths are explicitly
  requested;
- report scan truncation and filesystem walk errors;
- avoid network access, credential access, Git mutations, and external writes.

The Skill must preserve explicit approval boundaries for context writes, Git
mutations, remote publication, artifact upload, deployment, and task UI state.

## Reporting a vulnerability

Use GitHub private vulnerability reporting when it is enabled for the
repository. If no private channel is available, open a minimal issue asking the
maintainer to establish one, without including exploit details or sensitive
data.

Do not put credentials, private repository content, raw project memory,
absolute local paths, or personal data in a public issue.

Include the affected revision, platform, Python version, impact, reproduction
conditions, and a minimal synthetic proof of concept when safe to do so.
