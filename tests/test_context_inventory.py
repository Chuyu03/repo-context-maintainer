from __future__ import annotations

import argparse
import contextlib
import importlib.util
import io
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = REPOSITORY_ROOT / "repo-context-maintainer"
SCRIPT_PATH = SKILL_ROOT / "scripts" / "context_inventory.py"

SPEC = importlib.util.spec_from_file_location("context_inventory", SCRIPT_PATH)
if SPEC is None or SPEC.loader is None:  # pragma: no cover - import guard
    raise RuntimeError(f"Unable to load {SCRIPT_PATH}")
context_inventory = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = context_inventory
SPEC.loader.exec_module(context_inventory)


class InventoryTests(unittest.TestCase):
    def inventory_without_git(
        self,
        root: Path,
        max_files: int = 20_000,
        *,
        show_absolute_paths: bool = False,
    ) -> dict[str, object]:
        with mock.patch.object(
            context_inventory,
            "git_worktree_root",
            return_value=None,
        ):
            return context_inventory.inventory(
                root,
                max_files,
                show_absolute_paths=show_absolute_paths,
            )

    def test_truncation_reports_scanned_count(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            for name in ("c.txt", "a.txt", "b.txt"):
                (root / name).write_text(name, encoding="utf-8")

            data = self.inventory_without_git(root, max_files=2)

        self.assertEqual(data["scanned"], 2)
        self.assertEqual(data["max_files"], 2)
        self.assertTrue(data["truncated"])
        self.assertEqual(data["errors"], [])

    def test_exact_limit_is_not_truncated(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "a.txt").write_text("a", encoding="utf-8")
            (root / "b.txt").write_text("b", encoding="utf-8")

            data = self.inventory_without_git(root, max_files=2)

        self.assertEqual(data["scanned"], 2)
        self.assertFalse(data["truncated"])

    def test_walk_error_is_reported_without_absolute_root(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            (root / "AGENTS.md").write_text("# test", encoding="utf-8")

            def fake_walk(
                top: Path,
                *,
                onerror: object,
                followlinks: bool,
            ):
                self.assertFalse(followlinks)
                error = PermissionError(
                    13,
                    "Access denied",
                    str(Path(top) / "locked"),
                )
                onerror(error)
                yield str(top), [], ["AGENTS.md"]

            with mock.patch.object(context_inventory.os, "walk", fake_walk):
                data = self.inventory_without_git(root)

        self.assertEqual(data["scanned"], 1)
        self.assertEqual(data["agents_files"], ["AGENTS.md"])
        self.assertEqual(len(data["errors"]), 1)
        error = data["errors"][0]
        self.assertEqual(error["path"], "locked")
        self.assertEqual(error["errno"], 13)
        self.assertEqual(error["message"], "Access denied")
        self.assertNotIn(str(root), json.dumps(data))

    def test_max_files_must_be_positive(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            for invalid in (0, -1):
                with self.subTest(invalid=invalid):
                    with self.assertRaisesRegex(
                        ValueError,
                        "greater than zero",
                    ):
                        context_inventory.inventory(root, invalid)

        for invalid in ("0", "-2"):
            with self.subTest(cli_value=invalid):
                with self.assertRaises(argparse.ArgumentTypeError):
                    context_inventory.positive_int(invalid)

    def test_memory_candidates_ignore_ancestor_and_prefix_matches(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            ancestor = Path(temporary) / "memory"
            root = ancestor / "project"
            (root / "notes").mkdir(parents=True)
            (root / "notes.txt").write_text("ordinary", encoding="utf-8")
            (root / "memory_tools.py").write_text("ordinary", encoding="utf-8")
            (root / "MEMORY.md").write_text("memory", encoding="utf-8")
            memory_dir = root / "notes" / "project-memory"
            memory_dir.mkdir()
            (memory_dir / "facts.txt").write_text("fact", encoding="utf-8")

            data = self.inventory_without_git(root)

        self.assertEqual(
            data["memory_candidates"],
            ["MEMORY.md", "notes/project-memory/facts.txt"],
        )

    def test_unicode_paths_are_preserved_as_relative_utf8(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            agents = root / "项目" / "AGENTS.md"
            skill = root / "技能" / "SKILL.md"
            memory = root / "记忆" / "memory.md"
            for path in (agents, skill, memory):
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("内容", encoding="utf-8")

            data = self.inventory_without_git(root)

        self.assertEqual(data["agents_files"], ["项目/AGENTS.md"])
        self.assertEqual(data["skill_files"], ["技能/SKILL.md"])
        self.assertEqual(data["memory_candidates"], ["记忆/memory.md"])

    def test_git_worktree_and_marker_are_separate(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            (root / ".git").mkdir()
            completed = subprocess.CompletedProcess(
                args=[],
                returncode=0,
                stdout=str(root),
                stderr="",
            )
            with mock.patch.object(
                context_inventory.subprocess,
                "run",
                return_value=completed,
            ):
                data = context_inventory.inventory(root, 10)

        self.assertTrue(data["git_marker_present"])
        self.assertTrue(data["is_git_repo"])
        self.assertEqual(data["git_root"], "<project-root>")

    def test_missing_git_is_not_a_crash(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            with mock.patch.object(
                context_inventory.subprocess,
                "run",
                side_effect=FileNotFoundError("git unavailable"),
            ):
                data = context_inventory.inventory(root, 10)

        self.assertFalse(data["is_git_repo"])
        self.assertIsNone(data["git_root"])

    def test_default_json_schema_redacts_root(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            (root / "AGENTS.md").write_text("# test", encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(SCRIPT_PATH), str(root), "--json"],
                capture_output=True,
                check=False,
                encoding="utf-8",
                errors="strict",
                text=True,
            )

        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        expected_keys = {
            "schema_version",
            "root",
            "paths_redacted",
            "git_marker_present",
            "is_git_repo",
            "git_root",
            "max_files",
            "scanned",
            "truncated",
            "errors",
            "context_dirs",
            "agents_files",
            "skill_files",
            "memory_candidates",
        }
        self.assertEqual(set(data), expected_keys)
        self.assertEqual(data["schema_version"], 1)
        self.assertEqual(data["root"], "<project-root>")
        self.assertTrue(data["paths_redacted"])
        self.assertIsInstance(data["scanned"], int)
        self.assertIsInstance(data["truncated"], bool)
        self.assertIsInstance(data["errors"], list)
        self.assertNotIn(str(root), result.stdout)

    def test_absolute_paths_require_explicit_flag(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            data = self.inventory_without_git(
                root,
                show_absolute_paths=True,
            )

        self.assertEqual(data["root"], str(root))
        self.assertFalse(data["paths_redacted"])

    def test_missing_root_error_is_redacted_by_default(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            missing = Path(temporary) / "private" / "missing"
            with self.assertRaisesRegex(ValueError, "<project-root>") as caught:
                context_inventory.inventory(missing, 10)

        self.assertNotIn(str(missing), str(caught.exception))

    def test_symlinked_files_and_directories_are_not_followed(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            root = base / "root"
            outside = base / "outside"
            root.mkdir()
            outside.mkdir()
            (outside / "MEMORY.md").write_text("private", encoding="utf-8")
            try:
                (root / "linked-dir").symlink_to(
                    outside,
                    target_is_directory=True,
                )
                (root / "memory.md").symlink_to(outside / "MEMORY.md")
            except OSError as error:
                self.skipTest(f"symlinks unavailable: {error}")

            data = self.inventory_without_git(root)

        self.assertEqual(data["memory_candidates"], [])
        self.assertEqual(data["scanned"], 1)

    def test_markdown_output_surfaces_completeness(self) -> None:
        data = {
            "schema_version": 1,
            "root": "<project-root>",
            "paths_redacted": True,
            "git_marker_present": False,
            "is_git_repo": False,
            "git_root": None,
            "max_files": 1,
            "scanned": 1,
            "truncated": True,
            "errors": [
                {"path": "locked", "errno": 13, "message": "denied"}
            ],
            "context_dirs": [],
            "agents_files": [],
            "skill_files": [],
            "memory_candidates": [],
        }
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            context_inventory.print_markdown(data)

        rendered = output.getvalue()
        self.assertIn("Files scanned: 1 (limit: 1)", rendered)
        self.assertIn("Truncated: yes", rendered)
        self.assertIn("Walk errors: 1", rendered)
        self.assertIn("locked: denied (errno: 13)", rendered)


if __name__ == "__main__":
    unittest.main()
