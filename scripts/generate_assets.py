"""Generate GitHub-compatible SVG assets for the profile README."""

from __future__ import annotations

from pathlib import Path

ASSETS = Path(__file__).resolve().parents[1] / "assets"
NAVY = "#07111F"
NAVY_2 = "#0B1628"
BLUE = "#2563EB"
CYAN = "#06B6D4"
PURPLE = "#7C3AED"
WHITE = "#F8FAFC"
MUTED = "#94A3B8"
LINE = "#1E293B"


def write(name: str, content: str) -> None:
    ASSETS.mkdir(parents=True, exist_ok=True)
    path = ASSETS / name
    path.write_text(content.strip() + "\n", encoding="utf-8")
    print(f"wrote {path}")


def banner() -> str:
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 400" role="img" aria-label="Deekshith Reddy — Frontend Developer, Python Developer, AI Enthusiast">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="{NAVY}"/>
      <stop offset="55%" stop-color="{NAVY_2}"/>
      <stop offset="100%" stop-color="{NAVY}"/>
    </linearGradient>
    <linearGradient id="accent" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="{BLUE}"/>
      <stop offset="55%" stop-color="{CYAN}"/>
      <stop offset="100%" stop-color="{PURPLE}"/>
    </linearGradient>
    <linearGradient id="glow" x1="0.2" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="{BLUE}" stop-opacity="0.22"/>
      <stop offset="50%" stop-color="{CYAN}" stop-opacity="0.08"/>
      <stop offset="100%" stop-color="{PURPLE}" stop-opacity="0.16"/>
    </linearGradient>
    <pattern id="grid" width="36" height="36" patternUnits="userSpaceOnUse">
      <path d="M 36 0 L 0 0 0 36" fill="none" stroke="{LINE}" stroke-width="0.7"/>
    </pattern>
  </defs>
  <rect width="1280" height="400" rx="18" fill="url(#bg)"/>
  <rect width="1280" height="400" rx="18" fill="url(#grid)" opacity="0.42"/>
  <circle cx="1080" cy="70" r="150" fill="url(#glow)"/>
  <circle cx="1180" cy="330" r="110" fill="{PURPLE}" opacity="0.08"/>
  <circle cx="90" cy="320" r="90" fill="{BLUE}" opacity="0.08"/>
  <path d="M1040 86 L1118 124 L1040 162 Z" fill="none" stroke="{CYAN}" stroke-width="1.4" opacity="0.55"/>
  <circle cx="1118" cy="124" r="4" fill="{CYAN}"/>
  <circle cx="1040" cy="86" r="3" fill="{BLUE}"/>
  <rect x="96" y="108" width="72" height="3" rx="1.5" fill="url(#accent)"/>
  <text x="96" y="86" font-family="Segoe UI, Inter, Arial, sans-serif" font-size="15" letter-spacing="4.5" fill="{CYAN}">SOFTWARE DEVELOPER</text>
  <text x="96" y="178" font-family="Segoe UI, Inter, Arial, sans-serif" font-size="56" font-weight="700" letter-spacing="1.5" fill="{WHITE}">DEEKSHITH REDDY</text>
  <text x="96" y="224" font-family="Segoe UI, Inter, Arial, sans-serif" font-size="20" fill="{MUTED}">Frontend Developer  ·  Python Developer  ·  AI Enthusiast</text>
  <text x="96" y="278" font-family="Segoe UI, Inter, Arial, sans-serif" font-size="18" fill="{WHITE}">Building clean digital experiences, intelligent applications,</text>
  <text x="96" y="306" font-family="Segoe UI, Inter, Arial, sans-serif" font-size="18" fill="{WHITE}">and practical AI-powered solutions.</text>
  <rect x="96" y="346" width="220" height="3" rx="1.5" fill="url(#accent)"/>
  <rect x="1" y="1" width="1278" height="398" rx="18" fill="none" stroke="{LINE}" stroke-width="2"/>
</svg>'''


def divider() -> str:
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 28" role="img" aria-hidden="true">
  <rect width="1280" height="28" fill="none"/>
  <rect x="140" y="12" width="1000" height="1.5" rx="1" fill="{LINE}"/>
  <rect x="500" y="10" width="280" height="5" rx="2.5" fill="{CYAN}" opacity="0.85"/>
  <rect x="580" y="10" width="120" height="5" rx="2.5" fill="{BLUE}"/>
</svg>'''


def card(title: str, subtitle: str, accent: str) -> str:
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 560 170" role="img" aria-label="{title}: {subtitle}">
  <defs>
    <linearGradient id="cardbg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="{NAVY_2}"/>
      <stop offset="100%" stop-color="{NAVY}"/>
    </linearGradient>
  </defs>
  <rect width="560" height="170" rx="16" fill="url(#cardbg)"/>
  <rect width="560" height="170" rx="16" fill="none" stroke="{accent}" stroke-opacity="0.45" stroke-width="2"/>
  <rect x="0" y="24" width="6" height="122" rx="3" fill="{accent}"/>
  <text x="40" y="78" font-family="Segoe UI, Inter, Arial, sans-serif" font-size="15" letter-spacing="3.2" fill="{accent}">{title}</text>
  <text x="40" y="118" font-family="Segoe UI, Inter, Arial, sans-serif" font-size="24" font-weight="700" fill="{WHITE}">{subtitle}</text>
</svg>'''


def button(label: str, accent: str) -> str:
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 220 56" role="img" aria-label="{label}">
  <rect x="1" y="1" width="218" height="54" rx="12" fill="{NAVY_2}" stroke="{accent}" stroke-width="2"/>
  <text x="110" y="35" text-anchor="middle" font-family="Segoe UI, Inter, Arial, sans-serif" font-size="16" font-weight="700" letter-spacing="1.4" fill="{WHITE}">{label}</text>
</svg>'''


def footer() -> str:
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 140" role="img" aria-label="Thanks for visiting">
  <rect width="1280" height="140" rx="16" fill="{NAVY}"/>
  <rect x="160" y="28" width="960" height="1.5" fill="{LINE}"/>
  <rect x="560" y="26" width="160" height="5" rx="2.5" fill="{CYAN}"/>
  <text x="640" y="74" text-anchor="middle" font-family="Segoe UI, Inter, Arial, sans-serif" font-size="22" font-weight="700" fill="{WHITE}">Thanks for visiting my profile.</text>
  <text x="640" y="106" text-anchor="middle" font-family="Segoe UI, Inter, Arial, sans-serif" font-size="16" fill="{MUTED}">Let's build something meaningful.</text>
</svg>'''


def heading_bar(label: str) -> str:
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 720 54" role="img" aria-label="{label}">
  <rect width="720" height="54" fill="none"/>
  <rect x="0" y="24" width="28" height="6" rx="3" fill="{CYAN}"/>
  <text x="42" y="34" font-family="Segoe UI, Inter, Arial, sans-serif" font-size="22" font-weight="700" fill="{WHITE}">{label}</text>
</svg>'''


def main() -> None:
    write("banner.svg", banner())
    write("divider.svg", divider())
    write("card-frontend.svg", card("FRONTEND", "Modern UI / UX", BLUE))
    write("card-python.svg", card("PYTHON", "Development", CYAN))
    write("card-ai.svg", card("AI / ML", "Intelligent Apps", PURPLE))
    write("card-automation.svg", card("AUTOMATION", "Smart Workflows", BLUE))
    write("btn-github.svg", button("GITHUB", BLUE))
    write("btn-linkedin.svg", button("LINKEDIN", CYAN))
    write("btn-portfolio.svg", button("PORTFOLIO", PURPLE))
    write("btn-email.svg", button("EMAIL", CYAN))
    write("footer.svg", footer())


if __name__ == "__main__":
    main()
