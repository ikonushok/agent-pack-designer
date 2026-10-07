from __future__ import annotations

import importlib.util
import os
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = REPO_ROOT / "agent-pack-designer"
VALIDATE_SKILL_PATH = SKILL_ROOT / "scripts" / "validate_skill.py"
VALIDATE_PACK_PATH = SKILL_ROOT / "scripts" / "validate_pack.py"
VALIDATE_RELEASE_PATH = SKILL_ROOT / "scripts" / "validate_release_metadata.py"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load module from {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


validate_skill = load_module("validate_skill_edge_cases", VALIDATE_SKILL_PATH)
validate_pack = load_module("validate_pack_edge_cases", VALIDATE_PACK_PATH)
validate_release = load_module("validate_release_edge_cases", VALIDATE_RELEASE_PATH)


def write(root: Path, relative: str, content: str) -> None:
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def create_valid_mature_pack(root: Path) -> None:
    write(
        root,
        "AGENTS.md",
        """# AGENTS.md

## Working Rules

Load only one agent for the task. Do not skip checks.

## Validation

Review evidence before making claims.
Verdicts: PASS_WITH_RISKS, RETEST, HOLD, BLOCK.
""",
    )
    write(
        root,
        "agents/architect.md",
        """# Architect

Goal: primary workflow.
When to Use: implementation planning.
Inspect First: AGENTS.md and changed files.
Checklist: check scope and contracts.
Stop Rules: do not continue without evidence.
Output: scoped plan.
""",
    )
    write(
        root,
        "agents/risk_reviewer.md",
        """# Risk Reviewer

Goal: risk review.
When to Use: risk-sensitive changes.
Inspect First: changed files and tests.
Checklist: check evidence and residual risk.
Verdicts: PASS_WITH_RISKS, RETEST, HOLD, BLOCK.
Output: verdict.
""",
    )
    write(
        root,
        "agents/validation_reviewer.md",
        """# Validation Reviewer

Goal: validation evidence review.
Validation evidence levels: L0, L1, L2, L3, L4, L5.
Verdicts: PASS_WITH_RISKS, RETEST, HOLD, BLOCK.
Output: verdict.
""",
    )


class ReleaseMetadataTests(unittest.TestCase):
    def setUp(self) -> None:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        write(self.root, "VERSION", "0.4.0\n")
        write(self.root, "agent-pack-designer/VERSION", "0.4.0\n")
        self.write_readme("prepared")
        self.git_mock = patch.object(validate_release, "run_git", return_value=(0, ""))
        self.git_mock.start()
        self.addCleanup(self.git_mock.stop)

    def write_readme(self, status: str, version: str = "0.4.0") -> None:
        write(
            self.root,
            "README.md",
            f"Version: {version}\n\nCurrent release `v{version}`\n\n"
            f"{version} is {status} as the specification discovery release.\n",
        )

    def test_accepts_prepared_and_tagged_release_metadata(self) -> None:
        for status in ("prepared", "tagged"):
            with self.subTest(status=status):
                self.write_readme(status)
                self.assertEqual(validate_release.validate(self.root, False), [])

    def test_rejects_unknown_release_status(self) -> None:
        self.write_readme("planned")
        errors = validate_release.validate(self.root, False)
        self.assertTrue(any("missing release note" in error for error in errors))

    def test_rejects_stale_readme_version(self) -> None:
        self.write_readme("prepared", version="0.3.1")
        errors = validate_release.validate(self.root, False)
        self.assertTrue(any("missing release metadata" in error for error in errors))
        self.assertTrue(any("missing release note" in error for error in errors))

    def test_rejects_mismatched_installed_version(self) -> None:
        write(self.root, "agent-pack-designer/VERSION", "0.3.1\n")
        errors = validate_release.validate(self.root, False)
        self.assertTrue(any("must match root VERSION" in error for error in errors))

    def test_prepared_metadata_does_not_bypass_required_head_tag(self) -> None:
        errors = validate_release.validate(self.root, True)
        self.assertTrue(any("HEAD is not tagged" in error for error in errors))
        with patch.object(validate_release, "run_git", return_value=(0, "v0.4.0")):
            self.assertEqual(validate_release.validate(self.root, True), [])


class ValidatorEdgeCaseTests(unittest.TestCase):
    def test_skill_frontmatter_accepts_single_quoted_yaml_scalars(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            skill_root = Path(temporary) / "agent-pack-designer"
            shutil.copytree(SKILL_ROOT, skill_root)
            skill_md = skill_root / "SKILL.md"
            content = skill_md.read_text(encoding="utf-8")
            content = content.replace(
                "name: agent-pack-designer",
                "name: 'agent-pack-designer'",
                1,
            )
            skill_md.write_text(content, encoding="utf-8")

            errors, _warnings = validate_skill.validate_skill(skill_root)

            self.assertEqual([], errors)

    def test_mature_pack_reports_symlinked_role_files(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            create_valid_mature_pack(root)
            try:
                os.symlink("risk_reviewer.md", root / "agents/symlinked_reviewer.md")
            except (OSError, NotImplementedError) as exc:
                self.skipTest(f"symlinks are not available: {exc}")

            errors, _warnings = validate_pack.validate_existing_pack(root, require_claude=False)

            self.assertTrue(any("must not be a symlink" in error for error in errors), errors)

    def test_mature_pack_reports_broken_symlinked_role_files(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            create_valid_mature_pack(root)
            try:
                os.symlink("missing_reviewer.md", root / "agents/broken_reviewer.md")
            except (OSError, NotImplementedError) as exc:
                self.skipTest(f"symlinks are not available: {exc}")

            errors, _warnings = validate_pack.validate_existing_pack(root, require_claude=False)

            self.assertTrue(any("broken_reviewer.md must not be a symlink" in error for error in errors), errors)


if __name__ == "__main__":
    unittest.main()
