from __future__ import annotations

import re
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = REPOSITORY_ROOT / "repo-context-maintainer"


class RepositoryTests(unittest.TestCase):
    def test_text_files_are_utf8_without_bom(self) -> None:
        extensions = {".md", ".py", ".yaml", ".yml"}
        for path in REPOSITORY_ROOT.rglob("*"):
            if not path.is_file() or ".git" in path.parts:
                continue
            if path.suffix.lower() not in extensions and path.name not in {
                "LICENSE",
                ".gitignore",
            }:
                continue
            with self.subTest(path=path.relative_to(REPOSITORY_ROOT)):
                raw = path.read_bytes()
                self.assertFalse(raw.startswith(b"\xef\xbb\xbf"))
                raw.decode("utf-8", errors="strict")

    def test_skill_frontmatter_and_openai_metadata(self) -> None:
        skill = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertTrue(skill.startswith("---\n"))
        frontmatter = skill.split("---", 2)[1]
        self.assertRegex(frontmatter, r"(?m)^name: repo-context-maintainer$")
        self.assertRegex(frontmatter, r"(?m)^description: \S.+$")

        metadata = (SKILL_ROOT / "agents" / "openai.yaml").read_text(
            encoding="utf-8"
        )
        self.assertIn('display_name: "Repo & Context Maintainer"', metadata)
        self.assertIn("$repo-context-maintainer", metadata)

    def test_local_markdown_links_resolve_inside_repository(self) -> None:
        pattern = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
        for markdown in REPOSITORY_ROOT.rglob("*.md"):
            if ".git" in markdown.parts:
                continue
            text = markdown.read_text(encoding="utf-8")
            for target in pattern.findall(text):
                if target.startswith(("http://", "https://", "mailto:", "#")):
                    continue
                relative_target = target.split("#", 1)[0]
                resolved = (markdown.parent / relative_target).resolve()
                with self.subTest(
                    source=markdown.relative_to(REPOSITORY_ROOT),
                    target=target,
                ):
                    self.assertTrue(resolved.is_relative_to(REPOSITORY_ROOT))
                    self.assertTrue(resolved.exists())

    def test_ci_is_read_only_and_pins_official_actions(self) -> None:
        workflow = (REPOSITORY_ROOT / ".github" / "workflows" / "ci.yml").read_text(
            encoding="utf-8"
        )
        self.assertIn("permissions:\n  contents: read", workflow)
        self.assertIn("persist-credentials: false", workflow)
        self.assertIn("timeout-minutes:", workflow)
        self.assertNotIn("pull_request_target", workflow)
        self.assertNotIn("self-hosted", workflow)
        self.assertNotIn("${{ secrets.", workflow)
        actions = re.findall(r"(?m)^\s*uses:\s+([^@\s]+)@([^\s#]+)", workflow)
        self.assertTrue(actions)
        for action, revision in actions:
            with self.subTest(action=action):
                self.assertTrue(action.startswith("actions/"))
                self.assertRegex(revision, r"^[0-9a-f]{40}$")


if __name__ == "__main__":
    unittest.main()
