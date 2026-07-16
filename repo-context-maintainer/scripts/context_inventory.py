#!/usr/bin/env python3
"""Inventory agent context surfaces in a project.

This script is intentionally read-only. It finds likely AGENTS.md files, Codex
skills, and project-memory candidates so an agent can update context explicitly.
"""

from __future__ import annotations

import argparse
import json
import os
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


def rel(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def should_skip_dir(path: Path, root: Path) -> bool:
    name = path.name.lower()
    if name in SKIP_DIRS:
        return True

    # Keep .codex and .agents visible because they often contain context.
    if name.startswith(".") and name not in {".codex", ".agents"}:
        return True

    parts = {part.lower() for part in path.relative_to(root).parts}
    return any(part in SKIP_DIRS for part in parts)


def iter_paths(root: Path, max_files: int) -> Iterable[Path]:
    seen = 0
    for current_root, dirs, files in os.walk(root):
        current = Path(current_root)
        dirs[:] = [
            directory
            for directory in dirs
            if not should_skip_dir(current / directory, root)
        ]

        for filename in files:
            seen += 1
            if seen > max_files:
                return
            yield current / filename


def inventory(root: Path, max_files: int) -> dict[str, object]:
    root = root.resolve()
    agents_files: list[str] = []
    skill_files: list[str] = []
    memory_candidates: list[str] = []

    for path in iter_paths(root, max_files):
        lower_name = path.name.lower()
        lower_parts = [part.lower() for part in path.parts]

        if lower_name == "agents.md":
            agents_files.append(rel(path, root))

        if lower_name == "skill.md":
            skill_files.append(rel(path, root))

        if lower_name in MEMORY_FILE_NAMES or lower_name.startswith("memory"):
            memory_candidates.append(rel(path, root))
            continue

        if any(part in MEMORY_DIR_NAMES for part in lower_parts):
            memory_candidates.append(rel(path, root))

    context_dirs = []
    for dirname in [".agents", ".codex", "skills"]:
        candidate = root / dirname
        if candidate.exists():
            context_dirs.append(rel(candidate, root))

    return {
        "root": str(root),
        "is_git_repo": (root / ".git").exists(),
        "context_dirs": sorted(context_dirs),
        "agents_files": sorted(agents_files),
        "skill_files": sorted(skill_files),
        "memory_candidates": sorted(set(memory_candidates)),
    }


def print_markdown(data: dict[str, object]) -> None:
    print(f"# Context Inventory: {data['root']}")
    print()
    print(f"- Git repository marker: {'yes' if data['is_git_repo'] else 'no'}")

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
        type=int,
        default=20000,
        help="Maximum files to inspect before stopping",
    )
    args = parser.parse_args()

    root = Path(args.root)
    if not root.exists():
        raise SystemExit(f"Root does not exist: {root}")
    if not root.is_dir():
        raise SystemExit(f"Root is not a directory: {root}")

    data = inventory(root, args.max_files)
    if args.json:
        print(json.dumps(data, indent=2, ensure_ascii=False))
    else:
        print_markdown(data)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
