#!/usr/bin/env python3
"""Refresh generated README blocks without rewriting manual content."""

from __future__ import annotations

import json
import os
import re
import ssl
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
CONFIG = Path(__file__).resolve().parent / "projects.json"
PROJECT_ASSETS = ROOT / "assets" / "projects"
USERNAME = "Deekshith-Reddy-20"
ACCENTS = ("#2563EB", "#06B6D4", "#7C3AED")
STATUS_COLORS = {
    "active": "#22C55E",
    "development": "#2563EB",
    "archived": "#94A3B8",
}
API = f"https://api.github.com/users/{USERNAME}/repos?per_page=100&sort=updated"
CTX = ssl.create_default_context()

STATUS_LABELS = {
    "active": "Active",
    "development": "Development",
    "archived": "Archived",
}


def replace_block(text: str, name: str, content: str) -> str:
    start = f"<!-- {name}:START -->"
    end = f"<!-- {name}:END -->"
    pattern = re.compile(
        re.escape(start) + r".*?" + re.escape(end),
        flags=re.DOTALL,
    )
    if not pattern.search(text):
        raise SystemExit(f"Missing markers for {name}")
    inner = content.strip("\n")
    replacement = f"{start}\n{inner}\n{end}"
    return pattern.sub(replacement, text, count=1)


def api_get(url: str) -> Any:
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": f"{USERNAME}-profile-readme",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(request, context=CTX, timeout=30) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        raise SystemExit(f"GitHub API error {exc.code} for {url}") from exc


def load_repos() -> dict[str, dict[str, Any]]:
    repos = api_get(API)
    return {item["name"]: item for item in repos}


def homepage_url(repo: dict[str, Any]) -> str | None:
    homepage = (repo.get("homepage") or "").strip()
    if homepage.startswith("http://") or homepage.startswith("https://"):
        lowered = homepage.lower()
        if "github.com/" + USERNAME.lower() in lowered:
            return None
        return homepage
    return None


def status_for(entry: dict[str, Any], repo: dict[str, Any] | None) -> str | None:
    if repo and repo.get("archived"):
        return "archived"
    return entry.get("status")


def wrap_text(text: str, width: int = 88) -> list[str]:
    words = text.split()
    lines: list[str] = []
    current: list[str] = []
    for word in words:
        trial = " ".join(current + [word])
        if len(trial) <= width:
            current.append(word)
        else:
            if current:
                lines.append(" ".join(current))
            current = [word]
    if current:
        lines.append(" ".join(current))
    return lines[:3]


def write_project_card(
    entry: dict[str, Any],
    repo: dict[str, Any] | None,
    accent: str,
) -> str:
    PROJECT_ASSETS.mkdir(parents=True, exist_ok=True)
    status = status_for(entry, repo)
    desc_lines = wrap_text(entry["description"])
    tech = " · ".join(entry.get("tech") or [])
    metrics_parts = []
    if repo:
        stars = int(repo.get("stargazers_count") or 0)
        forks = int(repo.get("forks_count") or 0)
        if stars:
            metrics_parts.append(f"{stars} stars")
        if forks:
            metrics_parts.append(f"{forks} forks")
    metrics = " · ".join(metrics_parts)
    status_dot = STATUS_COLORS.get(status or "", "")
    status_label = STATUS_LABELS.get(status or "", "")
    title = escape(entry["title"])
    desc_svg = "\n".join(
        f'<text x="36" y="{112 + index * 22}" font-family="Segoe UI, Inter, Arial, sans-serif" font-size="16" fill="#F8FAFC">{escape(line)}</text>'
        for index, line in enumerate(desc_lines)
    )
    bottom = tech if not metrics else f"{tech}  ·  {metrics}"
    status_svg = ""
    if status_label and status_dot:
        status_svg = (
            f'<circle cx="930" cy="46" r="5" fill="{status_dot}"/>'
            f'<text x="942" y="51" font-family="Segoe UI, Inter, Arial, sans-serif" font-size="13" fill="#94A3B8">{escape(status_label)}</text>'
        )
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1120 220" role="img" aria-label="{title}">
  <rect width="1120" height="220" rx="16" fill="#0B1628"/>
  <rect width="1120" height="220" rx="16" fill="none" stroke="{accent}" stroke-opacity="0.45" stroke-width="2"/>
  <rect x="0" y="28" width="6" height="164" rx="3" fill="{accent}"/>
  <text x="36" y="52" font-family="Segoe UI, Inter, Arial, sans-serif" font-size="13" letter-spacing="2.8" fill="{accent}">PROJECT</text>
  <text x="36" y="86" font-family="Segoe UI, Inter, Arial, sans-serif" font-size="28" font-weight="700" fill="#F8FAFC">{title}</text>
  {status_svg}
  {desc_svg}
  <text x="36" y="196" font-family="Segoe UI, Inter, Arial, sans-serif" font-size="15" fill="#06B6D4">{escape(bottom)}</text>
</svg>
'''
    slug = re.sub(r"[^a-z0-9-]+", "-", entry["repo"].lower()).strip("-")
    path = PROJECT_ASSETS / f"{slug}.svg"
    path.write_text(svg, encoding="utf-8")
    return f"assets/projects/{slug}.svg"


def project_block(entry: dict[str, Any], repo: dict[str, Any] | None, index: int) -> str:
    url = (
        repo["html_url"]
        if repo
        else f"https://github.com/{USERNAME}/{entry['repo']}"
    )
    demo = homepage_url(repo) if repo else None
    card = write_project_card(entry, repo, ACCENTS[index % len(ACCENTS)])
    demo_html = ""
    if demo:
        demo_html = f' · <a href="{demo}"><strong>Live Demo</strong></a>'
    return f"""<p align="center">
  <a href="{url}"><img src="{card}" alt="{entry['title']}" width="100%" /></a>
</p>
<p align="center">
  <a href="{url}"><strong>View Project</strong></a>{demo_html}
</p>"""


def render_projects(config: dict[str, Any], repos: dict[str, dict[str, Any]]) -> str:
    blocks = [
        project_block(entry, repos.get(entry["repo"]), index)
        for index, entry in enumerate(config["featured"])
    ]
    extra_lines = []
    for entry in config.get("additional", []):
        repo = repos.get(entry["repo"])
        url = repo["html_url"] if repo else f"https://github.com/{USERNAME}/{entry['repo']}"
        extra_lines.append(
            f"- **[{entry['title']}]({url})** — {entry['description']}"
        )
    extra = "\n".join(extra_lines)
    return "\n".join(blocks) + (
        "\n\n<details>\n<summary><strong>More repositories</strong></summary>\n\n"
        f"{extra}\n\n</details>"
    )


def render_stats() -> str:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d%H")
    stats = (
        "https://github-readme-stats.vercel.app/api"
        f"?username={USERNAME}&show_icons=true&hide_border=true"
        "&bg_color=07111F&title_color=06B6D4&icon_color=2563EB"
        "&text_color=F8FAFC&ring_color=7C3AED&hide=issues"
        f"&cache_seconds=1800&v={stamp}"
    )
    streak = (
        "https://streak-stats.demolab.com"
        f"?user={USERNAME}&hide_border=true&background=07111F"
        "&ring=2563EB&fire=06B6D4&currStreakNum=F8FAFC&sideNums=F8FAFC"
        "&currStreakLabel=06B6D4&sideLabels=94A3B8&dates=94A3B8"
        f"&stroke=1E293B&v={stamp}"
    )
    return f"""<p align="center">
  <img src="{stats}" alt="GitHub statistics for {USERNAME}" />
</p>
<p align="center">
  <img src="{streak}" alt="GitHub streak for {USERNAME}" />
</p>"""


def render_languages() -> str:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d%H")
    langs = (
        "https://github-readme-stats.vercel.app/api/top-langs/"
        f"?username={USERNAME}&layout=compact&hide_border=true"
        "&bg_color=07111F&title_color=06B6D4&text_color=F8FAFC"
        f"&langs_count=6&v={stamp}"
    )
    graph = (
        "https://github-readme-activity-graph.vercel.app/graph"
        f"?username={USERNAME}&bg_color=07111F&color=94A3B8"
        "&line=2563EB&point=06B6D4&area=true&hide_border=true"
        "&area_color=2563EB&custom_title=Contribution%20activity"
        f"&v={stamp}"
    )
    return f"""<p align="center">
  <img src="{langs}" alt="Most used languages" />
</p>
<p align="center">
  <img src="{graph}" alt="Contribution activity graph" />
</p>"""


def main() -> None:
    config = json.loads(CONFIG.read_text(encoding="utf-8"))
    repos = load_repos()
    text = README.read_text(encoding="utf-8")
    original = text
    text = replace_block(text, "PROJECTS", render_projects(config, repos))
    text = replace_block(text, "STATS", render_stats())
    text = replace_block(text, "LANGUAGES", render_languages())
    if text != original:
        README.write_text(text, encoding="utf-8", newline="\n")
        print("README generated sections updated.")
    else:
        print("README generated sections already current.")


if __name__ == "__main__":
    main()
