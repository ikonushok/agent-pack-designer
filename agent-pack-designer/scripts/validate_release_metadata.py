#!/usr/bin/env python3
"""Validate release metadata across VERSION, README, and git tags."""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path


VERSION_RE = re.compile(r"^\d+\.\d+\.\d+$")


def run_git(root: Path, args: list[str]) -> tuple[int, str]:
    completed = subprocess.run(
        ["git", *args],
        cwd=root,
        check=False,
        capture_output=True,
        text=True,
    )
    return completed.returncode, completed.stdout.strip()


def validate(root: Path, require_head_tag: bool) -> list[str]:
    errors: list[str] = []
    version_path = root / "VERSION"
    skill_version_path = root / "agent-pack-designer" / "VERSION"
    readme_path = root / "README.md"

    try:
        version = version_path.read_text(encoding="utf-8").strip()
    except OSError as exc:
        return [f"could not read VERSION: {exc}"]

    if not VERSION_RE.match(version):
        errors.append(f"VERSION must be semantic X.Y.Z, got: {version!r}")

    try:
        skill_version = skill_version_path.read_text(encoding="utf-8").strip()
    except OSError as exc:
        errors.append(f"could not read agent-pack-designer/VERSION: {exc}")
    else:
        if skill_version != version:
            errors.append(
                "agent-pack-designer/VERSION must match root VERSION: "
                f"expected {version!r}, got {skill_version!r}"
            )

    try:
        readme = readme_path.read_text(encoding="utf-8")
    except OSError as exc:
        return [f"could not read README.md: {exc}"]

    expected_version_line = f"Version: {version}"
    expected_release_line = f"Current release `v{version}`"
    expected_release_note = f"{version} is tagged as"

    for expected in [expected_version_line, expected_release_line, expected_release_note]:
        if expected not in readme:
            errors.append(f"README.md missing release metadata: {expected}")

    code, tags_output = run_git(root, ["tag", "--points-at", "HEAD"])
    if code != 0:
        errors.append("could not inspect git tags at HEAD")
        tags: list[str] = []
    else:
        tags = [line for line in tags_output.splitlines() if line]

    expected_tag = f"v{version}"
    release_tags = [tag for tag in tags if tag.startswith("v")]
    if require_head_tag and expected_tag not in release_tags:
        if release_tags:
            errors.append(f"HEAD tags {release_tags} do not include expected {expected_tag}")
        else:
            errors.append(f"HEAD is not tagged with expected release tag {expected_tag}")
    if expected_tag in release_tags and len(release_tags) > 1:
        errors.append(f"HEAD has multiple release tags: {release_tags}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate release metadata consistency.")
    parser.add_argument("root", nargs="?", default=".", help="Repository root")
    parser.add_argument(
        "--require-head-tag",
        action="store_true",
        help="Require HEAD to be tagged with v<VERSION>.",
    )
    args = parser.parse_args()

    root = Path(args.root).expanduser().resolve()
    errors = validate(root, args.require_head_tag)
    for error in errors:
        print(f"ERROR: {error}")
    if errors:
        print("RESULT: FAIL release metadata")
        return 1
    print("RESULT: PASS release metadata")
    return 0


if __name__ == "__main__":
    sys.exit(main())
