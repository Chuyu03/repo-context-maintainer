#!/usr/bin/env python3
"""Inventory agent context surfaces in a project.

This script is intentionally read-only. It finds likely AGENTS.md files, Codex
skills, and project-memory candidates so an agent can update context explicitly.
"""

from __future__ import annotations

import argparse
import json
import os
import stat
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable


SKIP_DIRS = {
    ".git",
    ".hg",
    ".svn",
    "node_modules",
    "dist",
    "build",
    "out",
    ".next",
    ".nuxt",
    ".venv",
    "venv",
    "__pycache__",
}

MEMORY_FILE_NAMES = {
    "memory.md",
    "memories.md",
    "project-memory.md",
    "project_memory.md",
}

MEMORY_DIR_NAMES = {
    "memory",
    "memories",
    "project-memory",
    "project_memory",
}


@dataclass
class ScanState:
    """Mutable scan evidence shared with the path iterator."""

    scanned: int = 0
    truncated: bool = False
    errors: list[dict[str, object]] = field(default_factory=list)


def rel(path: Path, root: Path) -> str:
    """Return a stable project-relative path without leaking an outside path."""

    try:
        relative = path.relative_to(root)
    except ValueError:
        return "<outside-project>"
    return relative.as_posix() or "."


def display_error_path(
    filename: object,
    root: Path,
    show_absolute_paths: bool,
) -> str:
    if not filename:
        return "<unknown>"

    path = Path(os.fsdecode(filename))
    if not path.is_absolute():
        path = root / path

    if show_absolute_paths:
        return str(path.resolve(strict=False))
    return rel(path, root)


def record_walk_error(
    error: OSError,
    root: Path,
    state: ScanState,
    show_absolute_paths: bool,
) -> None:
    """Record a sanitized os.walk error without embedding a private path."""

    message = error.strerror or error.__class__.__name__
    state.errors.append(
        {
            "path": display_error_path(
                error.filename,
                root,
                show_absolute_paths,
            ),
            "errno": error.errno,
            "message": message,
        }
    )


def should_skip_dir(path: Path, root: Path) -> bool:
    name = path.name.lower()
    if name in SKIP_DIRS:
        return True

    # Keep .codex and .agents visible because they often contain context.
    if name.startswith(".") and name not in {".codex", ".agents"}:
        return True

    parts = {part.lower() for part in path.relative_to(root).parts}
    return any(part in SKIP_DIRS for part in parts)


def is_link_like(path: Path) -> bool:
    """Reject links and Windows junctions so the scan stays inside the root."""

    if path.is_symlink():
        return True
    is_junction = getattr(path, "is_junction", None)
    if is_junction and is_junction():
        return True
    try:
        attributes = path.lstat().st_file_attributes
    except (AttributeError, OSError):
        return False
    reparse_point = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0)
    return bool(reparse_point and attributes & reparse_point)


def iter_paths(
    root: Path,
    max_files: int,
    state: ScanState | None = None,
    *,
    show_absolute_paths: bool = False,
) -> Iterable[Path]:
    if max_files <= 0:
        raise ValueError("max_files must be greater than zero")

    scan_state = state if state is not None else ScanState()

    def onerror(error: OSError) -> None:
        record_walk_error(
            error,
            root,
            scan_state,
            show_absolute_paths,
        )

    for current_root, dirs, files in os.walk(
        root,
        onerror=onerror,
        followlinks=False,
    ):
        current = Path(current_root)
        dirs[:] = sorted(
            directory
            for directory in dirs
            if not is_link_like(current / directory)
            if not should_skip_dir(current / directory, root)
        )

        for filename in sorted(files):
            if scan_state.scanned >= max_files:
                scan_state.truncated = True
                return
            scan_state.scanned += 1
            path = current / filename
            if not is_link_like(path):
                yield path


def git_worktree_root(root: Path) -> str | None:
    try:
        result = subprocess.run(
            ["git", "-C", str(root), "rev-parse", "--show-toplevel"],
            capture_output=True,
            check=False,
            encoding="utf-8",
            errors="replace",
            text=True,
        )
    except OSError:
        return None

    if result.returncode != 0:
        return None

    git_root = result.stdout.strip()
    return git_root or None


def inventory(
    root: Path,
    max_files: int,
    *,
    show_absolute_paths: bool = False,
) -> dict[str, object]:
    if max_files <= 0:
        raise ValueError("max_files must be greater than zero")
    root_label = str(root) if show_absolute_paths else "<project-root>"
    if not root.exists():
        raise ValueError(f"root does not exist: {root_label}")
    if not root.is_dir():
        raise ValueError(f"root is not a directory: {root_label}")

    root = root.resolve()
    git_root = git_worktree_root(root)
    state = ScanState()
    agents_files: list[str] = []
    skill_files: list[str] = []
    memory_candidates: list[str] = []

    for path in iter_paths(
        root,
        max_files,
        state,
        show_absolute_paths=show_absolute_paths,
    ):
        lower_name = path.name.lower()
        try:
            relative_path = path.relative_to(root)
        except ValueError:
            continue
        relative_parent_parts = [
            part.lower() for part in relative_path.parent.parts
        ]

        if lower_name == "agents.md":
            agents_files.append(rel(path, root))

        if lower_name == "skill.md":
            skill_files.append(rel(path, root))

        if lower_name in MEMORY_FILE_NAMES:
            memory_candidates.append(rel(path, root))
            continue

        if any(part in MEMORY_DIR_NAMES for part in relative_parent_parts):
            memory_candidates.append(rel(path, root))

    context_dirs = []
    for dirname in [".agents", ".codex", "skills"]:
        candidate = root / dirname
        if candidate.is_dir() and not is_link_like(candidate):
            context_dirs.append(rel(candidate, root))

    if git_root is None:
        displayed_git_root = None
    elif show_absolute_paths:
        displayed_git_root = str(Path(git_root).resolve(strict=False))
    elif Path(git_root).resolve(strict=False) == root:
        displayed_git_root = "<project-root>"
    else:
        displayed_git_root = "<git-root>"

    return {
        "schema_version": 1,
        "root": str(root) if show_absolute_paths else "<project-root>",
        "paths_redacted": not show_absolute_paths,
        "git_marker_present": (root / ".git").exists(),
        "is_git_repo": git_root is not None,
        "git_root": displayed_git_root,
        "max_files": max_files,
        "scanned": state.scanned,
        "truncated": state.truncated,
        "errors": state.errors,
        "context_dirs": sorted(context_dirs),
        "agents_files": sorted(agents_files),
        "skill_files": sorted(skill_files),
        "memory_candidates": sorted(set(memory_candidates)),
    }


def print_markdown(data: dict[str, object]) -> None:
    print(f"# Context Inventory: {data['root']}")
    print()
    print(f"- Schema version: {data['schema_version']}")
    print(f"- Paths redacted: {'yes' if data['paths_redacted'] else 'no'}")
    print(f"- Git marker present: {'yes' if data['git_marker_present'] else 'no'}")
    print(f"- Git worktree: {'yes' if data['is_git_repo'] else 'no'}")
    print(f"- Git root: {data['git_root'] or 'none'}")
    print(f"- Files scanned: {data['scanned']} (limit: {data['max_files']})")
    print(f"- Truncated: {'yes' if data['truncated'] else 'no'}")
    print(f"- Walk errors: {len(data['errors'])}")

    for key, title in [
        ("context_dirs", "Context directories"),
        ("agents_files", "AGENTS.md files"),
        ("skill_files", "Skill files"),
        ("memory_candidates", "Memory candidates"),
    ]:
        values = data[key]
        print()
        print(f"## {title}")
        if values:
            for value in values:
                print(f"- {value}")
        else:
            print("- none found")

    print()
    print("## Scan errors")
    errors = data["errors"]
    if errors:
        for error in errors:
            errno = error["errno"] if error["errno"] is not None else "unknown"
            print(
                f"- {error['path']}: {error['message']} "
                f"(errno: {errno})"
            )
    else:
        print("- none")


def positive_int(value: str) -> int:
    try:
        parsed = int(value)
    except ValueError as error:
        raise argparse.ArgumentTypeError("must be an integer") from error
    if parsed <= 0:
        raise argparse.ArgumentTypeError("must be greater than zero")
    return parsed


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", default=".", help="Project root to inspect")
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit JSON instead of Markdown",
    )
    parser.add_argument(
        "--max-files",
        type=positive_int,
        default=20000,
        help="Maximum files to inspect before stopping",
    )
    parser.add_argument(
        "--show-absolute-paths",
        action="store_true",
        help="Include absolute project and Git roots in output",
    )
    args = parser.parse_args()

    root = Path(args.root)
    root_label = str(root) if args.show_absolute_paths else "<project-root>"
    if not root.exists():
        raise SystemExit(f"Root does not exist: {root_label}")
    if not root.is_dir():
        raise SystemExit(f"Root is not a directory: {root_label}")

    data = inventory(
        root,
        args.max_files,
        show_absolute_paths=args.show_absolute_paths,
    )
    if args.json:
        print(json.dumps(data, indent=2, ensure_ascii=False))
    else:
        print_markdown(data)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
