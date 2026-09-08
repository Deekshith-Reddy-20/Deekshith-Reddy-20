#!/usr/bin/env python3
"""Validate the profile README before publish."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
ASSETS = ROOT / "assets"
CONFIG = ROOT / "scripts" / "projects.json"
WORKFLOW = ROOT / ".github" / "workflows" / "update-readme.yml"

MARKERS = ("PROJECTS", "STATS", "LANGUAGES")
REQUIRED_ASSETS = (
    "banner.svg",
    "divider.svg",
    "card-frontend.svg",
    "card-python.svg",
    "card-ai.svg",
    "card-automation.svg",
    "btn-github.svg",
    "btn-linkedin.svg",
    "btn-portfolio.svg",
    "btn-email.svg",
    "footer.svg",
)
SECRET_PATTERNS = (
    r"ghp_[A-Za-z0-9]{20,}",
    r"github_pat_[A-Za-z0-9_]{20,}",
    r"sk-[A-Za-z0-9]{20,}",
    r"AKIA[0-9A-Z]{16}",
)
FORBIDDEN_CLAIMS = (
    "future ai",
    "salary",
    "hired at",
    "certified by",
    "1m users",
    "million users",
)


def fail(message: str) -> None:
    raise SystemExit(f"VALIDATION FAILED: {message}")


def main() -> None:
    text = README.read_text(encoding="utf-8")
    config = json.loads(CONFIG.read_text(encoding="utf-8"))

    if not WORKFLOW.exists():
        fail("missing GitHub Actions workflow")

    for name in MARKERS:
        start = f"<!-- {name}:START -->"
        end = f"<!-- {name}:END -->"
        if start not in text or end not in text:
            fail(f"missing {name} markers")
        if text.index(start) > text.index(end):
            fail(f"{name} markers are out of order")

    for asset in REQUIRED_ASSETS:
        path = ASSETS / asset
        if not path.exists():
            fail(f"missing asset {asset}")
        svg = path.read_text(encoding="utf-8")
        if "<svg" not in svg or "</svg>" not in svg:
            fail(f"invalid SVG {asset}")
        if "javascript:" in svg.lower() or "<script" in svg.lower():
            fail(f"script detected in {asset}")

    for pattern in SECRET_PATTERNS:
        if re.search(pattern, text):
            fail("possible secret detected in README")

    lowered = text.lower()
    for claim in FORBIDDEN_CLAIMS:
        if claim in lowered:
            fail(f"unverified claim found: {claim}")

    for entry in config["featured"] + config.get("additional", []):
        repo = entry["repo"]
        if repo not in text and entry["title"] not in text:
            # Generated block may be empty before first update.
            if "<!-- PROJECTS:START -->\n<!-- PROJECTS:END -->" in text.replace("\r\n", "\n"):
                continue
            if entry["title"] not in text:
                fail(f"featured project missing from README: {entry['title']}")

    unsupported = ("<script", "onclick=", "<style")
    for token in unsupported:
        if token in lowered:
            fail(f"unsupported HTML token: {token}")

    for path in (ASSETS / "projects").glob("*.svg"):
        svg = path.read_text(encoding="utf-8")
        if "<svg" not in svg or "</svg>" not in svg:
            fail(f"invalid SVG {path.name}")
        if "<script" in svg.lower():
            fail(f"script detected in {path.name}")

    print("Validation passed.")
    print(f"README bytes: {README.stat().st_size}")
    print(f"Assets: {len(list(ASSETS.glob('*.svg')))} SVG files")
    print(f"Featured projects in config: {len(config['featured'])}")


if __name__ == "__main__":
    main()
