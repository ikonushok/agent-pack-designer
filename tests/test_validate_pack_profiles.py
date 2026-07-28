from __future__ import annotations

import importlib.util
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = REPO_ROOT / "agent-pack-designer" / "scripts" / "validate_pack.py"
STARTER_PACK = REPO_ROOT / "agent-pack-designer" / "assets" / "starter-pack"


def load_validator():
    spec = importlib.util.spec_from_file_location("validate_pack", VALIDATOR_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load validator from {VALIDATOR_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


validator = load_validator()


def write(root: Path, relative: str, content: str) -> None:
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def create_valid_agents_pack(root: Path) -> None:
    write(
        root,
        "AGENTS.md",
        """# AGENTS.md

## Working Rules

Load only the agent needed for the task. Do not bypass validation.

## Validation

Use PASS_WITH_RISKS, RETEST, HOLD, and BLOCK verdicts.
""",
    )
    write(
        root,
        "agents/architect.md",
        """# Architect

Goal: own the primary workflow.
## When to Use
Use for implementation planning.
## Inspect First
Inputs: AGENTS.md and changed files.
## Checklist
Check scope and contracts.
## Stop Rules
Do not continue without evidence.
## Output
Output a scoped plan.
""",
    )
    write(
        root,
        "agents/risk_reviewer.md",
        """# Risk Reviewer

Goal: review project risk.
## When to Use
Use after risk-sensitive changes.
## Inspect First
Inputs: changed files and tests.
## Checklist
Check evidence and residual risk.
## Stop Rules
Do not accept unsupported claims.
## Output
Output a verdict.
""",
    )
    write(
        root,
        "agents/validation_reviewer.md",
        """# Validation Reviewer

Validation evidence levels: L0, L1, L2, L3, L4, L5.
Verdicts: PASS_WITH_RISKS, RETEST, HOLD, BLOCK.
""",
    )
    write(root, "agents/task_spec_short.md", "Goal: scoped work\nValidation target: L1\n")


def create_materialized_generated_pack(root: Path) -> None:
    shutil.copytree(STARTER_PACK, root, dirs_exist_ok=True)
    replacements = {
        "{{PROJECT_NAME}}": "profile-regression-project",
        "{{SOURCE_OF_TRUTH_FILES}}": "README.md and tests/",
        "{{PRIMARY_FILES}}": "src/ and tests/",
        "{{PRIMARY_WORKFLOW_TRIGGER}}": "the main project workflow",
        "{{RISK_AREA}}": "public contracts",
        "{{RISK_TRIGGER}}": "public API or validation changes",
        "{{RISK_FILES}}": "src/, tests/, and README.md",
        "{{DEFAULT_VALIDATION}}": "L1",
        "{{RISK_VALIDATION}}": "L2",
    }
    for path in root.rglob("*.md"):
        content = path.read_text(encoding="utf-8")
        for source, target in replacements.items():
            content = content.replace(source, target)
        path.write_text(content, encoding="utf-8")


class ExistingPackProfileRegressionTests(unittest.TestCase):
    def test_claude_agent_directory_is_a_valid_role_source(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            write(
                root,
                "AGENTS.md",
                "# AGENTS.md\n\n## Working Rules\nLoad only one agent. Do not skip checks.\n\n## Validation\nReview evidence.\n",
            )
            write(root, "CLAUDE.md", "# CLAUDE.md\n\nUse .claude/agents based on the task.\n")
            write(
                root,
                ".claude/agents/architect.md",
                "# Architect\n\nGoal: primary workflow.\nUse for design.\nInputs: AGENTS.md.\nCheck scope.\nDo not overreach.\nOutput: plan.\n",
            )
            write(
                root,
                ".claude/agents/validation-reviewer.md",
                "# Validation Reviewer\n\nGoal: review evidence.\nUse before release.\nInputs: commands.\nCheck L0 L1 L2 L3 L4 L5.\nDo not overclaim.\nOutput: verdict.\n",
            )

            errors, _warnings = validator.validate_existing_pack(root, require_claude=True)

            self.assertEqual([], errors)

    def test_intentional_starter_placeholders_are_not_active_pack_errors(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            create_valid_agents_pack(root)
            write(
                root,
                "assets/starter-pack/AGENTS.md",
                "# AGENTS.md\n\nProject: {{PROJECT_NAME}}\n",
            )

            errors, _warnings = validator.validate_existing_pack(root, require_claude=False)

            self.assertEqual([], errors)

    def test_customer_report_does_not_change_audit_result(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            create_valid_agents_pack(root)

            before = validator.validate_existing_pack(root, require_claude=False)
            write(
                root,
                "reports/customer/audit.md",
                "Observed literal template token {{PROJECT_NAME}} in a starter-pack example.\n",
            )
            after = validator.validate_existing_pack(root, require_claude=False)

            self.assertEqual(before, after)
            self.assertEqual([], after[0])

    def test_functional_validation_reviewer_alias_is_discovered(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            create_valid_agents_pack(root)
            (root / "agents/validation_reviewer.md").unlink()
            write(
                root,
                ".claude/agents/evidence-reviewer.md",
                "# Evidence Reviewer\n\nGoal: validation evidence review.\nChecks: L0 L1 L2 L3 L4 L5.\nOutput: verdict.\n",
            )

            errors, _warnings = validator.validate_existing_pack(root, require_claude=False)

            self.assertEqual([], errors)

    def test_agents_heading_alone_is_not_routing_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            create_valid_agents_pack(root)
            write(
                root,
                "AGENTS.md",
                "# AGENTS.md\n\n## Working Rules\nDo not skip checks.\n\n## Validation\nReview evidence.\n",
            )

            _errors, warnings = validator.validate_existing_pack(root, require_claude=False)

            self.assertTrue(any("routing or load-only guidance" in warning for warning in warnings))


class ProfileContractTests(unittest.TestCase):
    def test_generated_pack_scans_active_pack_files_but_not_reports(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            create_materialized_generated_pack(root)
            write(
                root,
                "reports/customer/audit.md",
                "A report may discuss {{PROJECT_NAME}} without modifying the generated pack.\n",
            )

            valid_errors, _warnings = validator.validate_pack(root, require_claude=True)
            self.assertEqual([], valid_errors)

            agents_md = root / "AGENTS.md"
            agents_md.write_text(
                agents_md.read_text(encoding="utf-8") + "\nUnresolved: {{PROJECT_NAME}}\n",
                encoding="utf-8",
            )
            invalid_errors, _warnings = validator.validate_pack(root, require_claude=True)
            self.assertTrue(any("unresolved template token" in error for error in invalid_errors))

    def test_generated_pack_scans_claude_agent_files(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            create_materialized_generated_pack(root)
            write(
                root,
                ".claude/agents/validation-reviewer.md",
                "# Validation Reviewer\n\nUnresolved: {{PROJECT_NAME}}\n",
            )

            errors, _warnings = validator.validate_pack(root, require_claude=True)

            self.assertTrue(
                any(".claude/agents/validation-reviewer.md" in error for error in errors),
                errors,
            )

    def test_repository_matches_designer_profile(self) -> None:
        self.assertIsNone(validator.profile_applicability(REPO_ROOT, validator.PROFILE_DESIGNER))
        errors, _warnings = validator.validate_skill_designer_repository(REPO_ROOT, require_claude=True)
        self.assertEqual([], errors)

    def test_designer_profile_does_not_require_local_workspace_agents(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            shutil.copytree(REPO_ROOT / "agent-pack-designer", root / "agent-pack-designer")

            errors, _warnings = validator.validate_skill_designer_repository(root, require_claude=True)

            self.assertEqual([], errors)

    def test_designer_profile_never_executes_target_validator(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            skill_root = Path(temporary) / "agent-pack-designer"
            shutil.copytree(REPO_ROOT / "agent-pack-designer", skill_root)
            target_validator = skill_root / "scripts/validate_skill.py"
            target_validator.write_text("raise RuntimeError('target code executed')\n", encoding="utf-8")

            errors, _warnings = validator.validate_installable_skill(skill_root)

            self.assertEqual([], errors)

    def test_missing_target_validator_is_a_profile_failure(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            skill_root = Path(temporary) / "agent-pack-designer"
            shutil.copytree(REPO_ROOT / "agent-pack-designer", skill_root)
            (skill_root / "scripts/validate_skill.py").unlink()

            errors, _warnings = validator.validate_installable_skill(skill_root)

            self.assertIn("missing required file: scripts/validate_skill.py", errors)

    def test_designer_repository_rejects_generated_profile_but_allows_mature_audit(self) -> None:
        generated = validator.profile_applicability(REPO_ROOT, validator.PROFILE_GENERATED)
        mature = validator.profile_applicability(REPO_ROOT, validator.PROFILE_MATURE)

        self.assertEqual(validator.VERDICT_NOT_APPLICABLE, generated[0])
        self.assertIsNone(mature)

    def test_multiple_skill_packages_are_inconclusive(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            for name in ["skill-one", "skill-two"]:
                write(root, f"{name}/SKILL.md", "---\nname: example\ndescription: example\n---\n")
                (root / name / "assets/starter-pack").mkdir(parents=True)

            result = validator.profile_applicability(root, validator.PROFILE_DESIGNER)

            self.assertEqual(validator.VERDICT_INCONCLUSIVE, result[0])

    def test_verdict_vocabulary_is_exposed(self) -> None:
        self.assertEqual(
            {"PASS", "PASS_WITH_RISKS", "FAIL", "NOT_APPLICABLE", "INCONCLUSIVE", "TOOL_ERROR"},
            {
                validator.VERDICT_PASS,
                validator.VERDICT_PASS_WITH_RISKS,
                validator.VERDICT_FAIL,
                validator.VERDICT_NOT_APPLICABLE,
                validator.VERDICT_INCONCLUSIVE,
                validator.VERDICT_TOOL_ERROR,
            },
        )

    def test_cli_profile_mismatch_is_not_applicable(self) -> None:
        completed = subprocess.run(
            [
                sys.executable,
                "-B",
                str(VALIDATOR_PATH),
                "--profile",
                validator.PROFILE_GENERATED,
                str(REPO_ROOT),
            ],
            check=False,
            capture_output=True,
            text=True,
        )

        self.assertEqual(2, completed.returncode)
        self.assertIn("RESULT: NOT_APPLICABLE generated-pack", completed.stdout)

    def test_cli_missing_path_is_tool_error(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            missing = Path(temporary) / "missing"
            completed = subprocess.run(
                [sys.executable, "-B", str(VALIDATOR_PATH), str(missing)],
                check=False,
                capture_output=True,
                text=True,
            )

        self.assertEqual(2, completed.returncode)
        self.assertIn("RESULT: TOOL_ERROR generated-pack", completed.stdout)

    def test_cli_report_is_idempotent_inside_target(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            create_valid_agents_pack(root)
            report = root / "reports/customer/audit.md"
            command = [
                sys.executable,
                "-B",
                str(VALIDATOR_PATH),
                "--profile",
                validator.PROFILE_MATURE,
                "--report-md",
                str(report),
                str(root),
            ]

            first = subprocess.run(command, check=False, capture_output=True, text=True)
            first_content = report.read_text(encoding="utf-8")
            second = subprocess.run(command, check=False, capture_output=True, text=True)
            second_content = report.read_text(encoding="utf-8")

        self.assertEqual(0, first.returncode)
        self.assertEqual(0, second.returncode)
        self.assertEqual(first_content, second_content)

    def test_cli_designer_profile_writes_self_audit_report(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            report = Path(temporary) / "designer-audit.md"
            completed = subprocess.run(
                [
                    sys.executable,
                    "-B",
                    str(VALIDATOR_PATH),
                    "--profile",
                    validator.PROFILE_DESIGNER,
                    "--report-md",
                    str(report),
                    str(REPO_ROOT),
                ],
                check=False,
                capture_output=True,
                text=True,
            )
            content = report.read_text(encoding="utf-8")

        self.assertEqual(0, completed.returncode)
        self.assertIn(f"Profile: `{validator.PROFILE_DESIGNER}`", content)
        self.assertIn("Starter-pack template placeholders are intentional", content)
        self.assertIn("Materialized starter-pack check: `PASS L2`", content)
        self.assertNotIn("unresolved template token", content)

    def test_cli_report_write_failure_is_tool_error(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            create_valid_agents_pack(root)
            blocked_parent = root / "not-a-directory"
            blocked_parent.write_text("file", encoding="utf-8")
            completed = subprocess.run(
                [
                    sys.executable,
                    "-B",
                    str(VALIDATOR_PATH),
                    "--profile",
                    validator.PROFILE_MATURE,
                    "--report-md",
                    str(blocked_parent / "audit.md"),
                    str(root),
                ],
                check=False,
                capture_output=True,
                text=True,
            )

        self.assertEqual(2, completed.returncode)
        self.assertIn("RESULT: TOOL_ERROR mature-existing-pack", completed.stdout)


if __name__ == "__main__":
    unittest.main()
