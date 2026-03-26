#!/usr/bin/env python3
"""
Scrape Claude Code and Claude Platform API docs into JSON files.
Each file: {url, title, section, slug, content, headings, order}
"""

import json
import re
import time
import urllib.request
import urllib.error
from pathlib import Path

# ── Claude Code docs (code.claude.com) ────────────────────────────────────────
# Section mapping based on doc topic groupings
CODE_SECTION_MAP = {
    "overview": "Getting Started",
    "quickstart": "Getting Started",
    "desktop-quickstart": "Getting Started",
    "how-claude-code-works": "Getting Started",
    "setup": "Installation & Setup",
    "terminal-config": "Installation & Setup",
    "troubleshooting": "Installation & Setup",
    "devcontainer": "Installation & Setup",
    "authentication": "Authentication & Security",
    "security": "Authentication & Security",
    "permissions": "Authentication & Security",
    "sandboxing": "Authentication & Security",
    "data-usage": "Authentication & Security",
    "zero-data-retention": "Authentication & Security",
    "legal-and-compliance": "Authentication & Security",
    "interactive-mode": "Features & Usage",
    "commands": "Features & Usage",
    "cli-reference": "Features & Usage",
    "common-workflows": "Features & Usage",
    "fast-mode": "Features & Usage",
    "voice-dictation": "Features & Usage",
    "keybindings": "Features & Usage",
    "scheduled-tasks": "Features & Usage",
    "output-styles": "Features & Usage",
    "checkpointing": "Features & Usage",
    "memory": "Configuration & Customization",
    "settings": "Configuration & Customization",
    "env-vars": "Configuration & Customization",
    "model-config": "Configuration & Customization",
    "statusline": "Configuration & Customization",
    "vs-code": "IDE & Editor Integration",
    "jetbrains": "IDE & Editor Integration",
    "chrome": "IDE & Editor Integration",
    "desktop": "IDE & Editor Integration",
    "remote-control": "IDE & Editor Integration",
    "slack": "IDE & Editor Integration",
    "features-overview": "Extensibility & Integration",
    "skills": "Extensibility & Integration",
    "plugins": "Extensibility & Integration",
    "plugins-reference": "Extensibility & Integration",
    "discover-plugins": "Extensibility & Integration",
    "plugin-marketplaces": "Extensibility & Integration",
    "mcp": "Extensibility & Integration",
    "hooks-guide": "Extensibility & Integration",
    "hooks": "Extensibility & Integration",
    "sub-agents": "Extensibility & Integration",
    "tools-reference": "Extensibility & Integration",
    "channels": "Extensibility & Integration",
    "channels-reference": "Extensibility & Integration",
    "headless": "CI/CD & Automation",
    "github-actions": "CI/CD & Automation",
    "gitlab-ci-cd": "CI/CD & Automation",
    "agent-teams": "Team & Enterprise",
    "analytics": "Team & Enterprise",
    "costs": "Team & Enterprise",
    "code-review": "Team & Enterprise",
    "monitoring-usage": "Team & Enterprise",
    "network-config": "Team & Enterprise",
    "server-managed-settings": "Team & Enterprise",
    "third-party-integrations": "Team & Enterprise",
    "claude-code-on-the-web": "Cloud Platforms",
    "amazon-bedrock": "Cloud Platforms",
    "google-vertex-ai": "Cloud Platforms",
    "microsoft-foundry": "Cloud Platforms",
    "llm-gateway": "Cloud Platforms",
    "best-practices": "Advanced Topics",
    "changelog": "Advanced Topics",
}

# All Claude Code slugs (from llms.txt)
CODE_SLUGS = [
    "agent-teams", "amazon-bedrock", "analytics", "authentication", "best-practices",
    "changelog", "channels", "channels-reference", "checkpointing", "chrome",
    "claude-code-on-the-web", "cli-reference", "code-review", "commands",
    "common-workflows", "costs", "data-usage", "desktop", "desktop-quickstart",
    "devcontainer", "discover-plugins", "env-vars", "fast-mode", "features-overview",
    "github-actions", "gitlab-ci-cd", "google-vertex-ai", "headless", "hooks",
    "hooks-guide", "how-claude-code-works", "interactive-mode", "jetbrains",
    "keybindings", "legal-and-compliance", "llm-gateway", "mcp", "memory",
    "microsoft-foundry", "model-config", "monitoring-usage", "network-config",
    "output-styles", "overview", "permissions", "plugin-marketplaces", "plugins",
    "plugins-reference", "quickstart", "remote-control", "sandboxing",
    "scheduled-tasks", "security", "server-managed-settings", "settings", "setup",
    "skills", "slack", "statusline", "sub-agents", "terminal-config",
    "third-party-integrations", "tools-reference", "troubleshooting",
    "voice-dictation", "vs-code", "zero-data-retention",
]

# ── Claude Platform/API docs (platform.claude.com) ────────────────────────────
PLATFORM_PAGES = [
    # Getting Started
    ("get-started", "Getting Started", "en/get-started"),
    ("intro-to-claude", "Getting Started", "en/docs/intro-to-claude"),
    # Models
    ("models-overview", "Models", "en/about-claude/models/overview"),
    ("model-deprecations", "Models", "en/about-claude/model-deprecations"),
    # Build with Claude
    ("working-with-messages", "Building with Claude", "en/build-with-claude/working-with-messages"),
    ("text-generation", "Building with Claude", "en/build-with-claude/text-generation"),
    ("vision", "Building with Claude", "en/build-with-claude/vision"),
    ("extended-thinking", "Building with Claude", "en/build-with-claude/extended-thinking"),
    ("adaptive-thinking", "Building with Claude", "en/build-with-claude/adaptive-thinking"),
    ("effort", "Building with Claude", "en/build-with-claude/effort"),
    ("context-windows", "Building with Claude", "en/build-with-claude/context-windows"),
    ("structured-outputs", "Building with Claude", "en/build-with-claude/structured-outputs"),
    ("citations", "Building with Claude", "en/build-with-claude/citations"),
    ("pdf-support", "Building with Claude", "en/build-with-claude/pdf-support"),
    ("files", "Building with Claude", "en/build-with-claude/files"),
    ("batch-processing", "Building with Claude", "en/build-with-claude/batch-processing"),
    ("prompt-caching", "Building with Claude", "en/build-with-claude/prompt-caching"),
    ("compaction", "Building with Claude", "en/build-with-claude/compaction"),
    ("context-editing", "Building with Claude", "en/build-with-claude/context-editing"),
    ("search-results", "Building with Claude", "en/build-with-claude/search-results"),
    ("data-residency", "Building with Claude", "en/build-with-claude/data-residency"),
    # Prompt Engineering
    ("prompt-engineering-overview", "Prompt Engineering", "en/docs/build-with-claude/prompt-engineering/overview"),
    ("claude-prompting-best-practices", "Prompt Engineering", "en/docs/build-with-claude/prompt-engineering/claude-prompting-best-practices"),
    # Tools & Agents
    ("tool-use-overview", "Tools & Agents", "en/docs/build-with-claude/tool-use/overview"),
    ("web-search-tool", "Tools & Agents", "en/agents-and-tools/tool-use/web-search-tool"),
    ("web-fetch-tool", "Tools & Agents", "en/agents-and-tools/tool-use/web-fetch-tool"),
    ("code-execution-tool", "Tools & Agents", "en/agents-and-tools/tool-use/code-execution-tool"),
    ("computer-use-tool", "Tools & Agents", "en/agents-and-tools/tool-use/computer-use-tool"),
    ("memory-tool", "Tools & Agents", "en/agents-and-tools/tool-use/memory-tool"),
    ("mcp-connector", "Tools & Agents", "en/agents-and-tools/mcp-connector"),
    # API Reference
    ("api-overview", "API Reference", "en/api/overview"),
    ("client-sdks", "API Reference", "en/api/client-sdks"),
    ("messages-api", "API Reference", "en/api/messages"),
    ("versioning", "API Reference", "en/api/versioning"),
    ("errors", "API Reference", "en/api/errors"),
    ("rate-limits", "API Reference", "en/api/rate-limits"),
    # Console / Workbench
    ("workbench", "Console & Workbench", "en/docs/test-and-evaluate/workbench/overview"),
    ("prompt-generator", "Console & Workbench", "en/docs/test-and-evaluate/prompt-library/overview"),
    # Embeddings
    ("embeddings", "Other Capabilities", "en/docs/build-with-claude/embeddings"),
]


def fetch(url: str):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=15) as r:
            return r.read().decode("utf-8", errors="replace")
    except Exception as e:
        print(f"  ERROR fetching {url}: {e}")
        return None


def extract_headings(md: str) -> list[str]:
    return [m.group(1).strip() for m in re.finditer(r"^#{1,4}\s+(.+)$", md, re.MULTILINE)]


def clean_content(md: str) -> str:
    # Strip frontmatter
    md = re.sub(r"^---\n.*?\n---\n", "", md, flags=re.DOTALL)
    # Strip MDX/JSX components
    md = re.sub(r"<[A-Z][^>]*>.*?</[A-Z][^>]*>", "", md, flags=re.DOTALL)
    md = re.sub(r"<[A-Z][^/]*/?>", "", md)
    # Collapse whitespace
    md = re.sub(r"\n{3,}", "\n\n", md)
    return md.strip()


def extract_title(md: str, fallback: str) -> str:
    m = re.search(r"^#\s+(.+)$", md, re.MULTILINE)
    return m.group(1).strip() if m else fallback


def scrape_code_docs(out_dir: Path):
    out_dir.mkdir(exist_ok=True)
    print(f"\n── Claude Code docs → {out_dir}")
    for i, slug in enumerate(CODE_SLUGS):
        url = f"https://code.claude.com/docs/en/{slug}.md"
        print(f"  [{i+1}/{len(CODE_SLUGS)}] {slug}")
        content = fetch(url)
        if not content:
            continue
        title = extract_title(content, slug)
        clean = clean_content(content)
        headings = extract_headings(content)
        section = CODE_SECTION_MAP.get(slug, "Claude Code")
        doc = {
            "url": f"https://code.claude.com/docs/en/{slug}",
            "title": title,
            "section": section,
            "slug": slug,
            "content": clean,
            "headings": headings,
            "order": i,
        }
        (out_dir / f"{slug}.json").write_text(json.dumps(doc, indent=2, ensure_ascii=False))
        time.sleep(0.3)
    print(f"  Done — {len(list(out_dir.glob('*.json')))} files written")


def scrape_platform_docs(out_dir: Path):
    out_dir.mkdir(exist_ok=True)
    print(f"\n── Platform/API docs → {out_dir}")
    for i, (slug, section, path) in enumerate(PLATFORM_PAGES):
        url = f"https://platform.claude.com/docs/{path}.md"
        print(f"  [{i+1}/{len(PLATFORM_PAGES)}] {slug}")
        content = fetch(url)
        if not content:
            # Try without .md
            url2 = f"https://platform.claude.com/docs/{path}"
            content = fetch(url2)
            if not content:
                continue
        title = extract_title(content, slug)
        clean = clean_content(content)
        headings = extract_headings(content)
        doc = {
            "url": f"https://platform.claude.com/docs/{path}",
            "title": title,
            "section": section,
            "slug": slug,
            "content": clean,
            "headings": headings,
            "order": i,
        }
        (out_dir / f"{slug}.json").write_text(json.dumps(doc, indent=2, ensure_ascii=False))
        time.sleep(0.3)
    print(f"  Done — {len(list(out_dir.glob('*.json')))} files written")


if __name__ == "__main__":
    base = Path(__file__).parent
    scrape_code_docs(base / "claude-code-docs")
    scrape_platform_docs(base / "claude-console-docs")
    print("\nAll done.")
