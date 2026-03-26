#!/usr/bin/env python3
"""
Generate CLAUDE_COURSE.md from scraped doc JSONs.
Reads all JSON files, organizes by module, and calls Claude API to generate
a structured power-user course (Concepts → Exercises → Quiz).
"""

import json
import os
import pathlib
import anthropic

BASE = pathlib.Path(__file__).parent
CODE_DIR = BASE / "claude-code-docs"
CONSOLE_DIR = BASE / "claude-console-docs"

# ── Module plan ───────────────────────────────────────────────────────────────
# Each module: (title, description, code_slugs, console_slugs)
MODULES = [
    (
        "Mental Model — What Claude Actually Is",
        "Understand how Claude works as an AI model, the product landscape (Console vs Code), and the recommended path for developers.",
        ["overview", "how-claude-code-works"],
        ["intro-to-claude", "get-started"],
    ),
    (
        "Models — Choosing the Right Tool",
        "Compare Opus, Sonnet, and Haiku. Understand context windows, thinking modes, and when to use each model.",
        ["model-config", "fast-mode"],
        ["models-overview", "model-deprecations", "context-windows", "adaptive-thinking", "extended-thinking", "effort"],
    ),
    (
        "The Console & API — Your First Integration",
        "Use the Workbench to prototype prompts, make your first API call, and understand the Messages API structure.",
        [],
        ["workbench", "prompt-generator", "working-with-messages", "text-generation", "api-overview", "client-sdks", "messages-api", "versioning", "errors", "rate-limits"],
    ),
    (
        "Prompt Engineering",
        "Write prompts that work. Understand system prompts, turn structure, and Anthropic's best practices.",
        [],
        ["prompt-engineering-overview", "claude-prompting-best-practices", "structured-outputs", "citations"],
    ),
    (
        "Claude Code — Setup & First Session",
        "Install Claude Code, log in, configure your terminal, and run your first coding session.",
        ["quickstart", "setup", "desktop-quickstart", "terminal-config", "authentication", "interactive-mode", "commands"],
        [],
    ),
    (
        "Memory — Teaching Claude About Your Project",
        "Use CLAUDE.md files and auto memory to give Claude persistent context about your codebase and preferences.",
        ["memory", "settings", "env-vars"],
        [],
    ),
    (
        "Everyday Workflows",
        "Explore codebases, fix bugs, write tests, refactor code, and use Git — all the daily driver workflows.",
        ["common-workflows", "checkpointing", "output-styles", "voice-dictation"],
        [],
    ),
    (
        "Permissions & Security",
        "Control what Claude can access. Understand permission modes, sandboxing, and enterprise security.",
        ["permissions", "security", "sandboxing", "data-usage", "zero-data-retention"],
        [],
    ),
    (
        "Tools & Tool Use",
        "Let Claude take actions: web search, code execution, file management, computer use, and custom client-side tools.",
        ["tools-reference"],
        ["web-search-tool", "web-fetch-tool", "code-execution-tool", "computer-use-tool", "memory-tool", "tool-use-overview"],
    ),
    (
        "MCP — Connecting Claude to Your Tools",
        "Extend Claude with the Model Context Protocol. Connect databases, APIs, and internal systems.",
        ["mcp"],
        ["mcp-connector"],
    ),
    (
        "Hooks & Automation",
        "Run shell commands automatically on events. Format code, send notifications, validate commands.",
        ["hooks-guide", "hooks", "scheduled-tasks"],
        [],
    ),
    (
        "Skills, Plugins & Subagents",
        "Build reusable skills, create plugins, and orchestrate specialized subagents for complex tasks.",
        ["skills", "plugins", "plugins-reference", "discover-plugins", "plugin-marketplaces", "sub-agents", "features-overview"],
        ["prompt-generator"],
    ),
    (
        "IDE Integration",
        "Use Claude Code in VS Code, JetBrains, the Desktop app, Chrome, and via Remote Control.",
        ["vs-code", "jetbrains", "desktop", "desktop-quickstart", "chrome", "remote-control"],
        [],
    ),
    (
        "Cost & Performance Optimization",
        "Reduce costs with prompt caching, batch processing, context management, and smart model selection.",
        ["costs"],
        ["prompt-caching", "batch-processing", "compaction", "context-editing", "token-counting", "files"],
    ),
    (
        "CI/CD & Headless Automation",
        "Run Claude Code in GitHub Actions, GitLab CI, and programmatically via the Agent SDK.",
        ["headless", "github-actions", "gitlab-ci-cd"],
        [],
    ),
    (
        "Agent Teams & Channels",
        "Orchestrate multiple Claude Code sessions. Push external events into sessions via channels.",
        ["agent-teams", "channels", "channels-reference"],
        [],
    ),
    (
        "Team & Enterprise Deployment",
        "Analytics, code review automation, monitoring, network config, and server-managed settings.",
        ["analytics", "code-review", "monitoring-usage", "network-config", "server-managed-settings",
         "third-party-integrations", "devcontainer", "slack", "amazon-bedrock", "google-vertex-ai",
         "microsoft-foundry", "llm-gateway", "claude-code-on-the-web"],
        [],
    ),
    (
        "Power User Mastery",
        "Best practices, advanced patterns, vision, embeddings, and what's next.",
        ["best-practices"],
        ["vision", "pdf-support", "search-results", "embeddings", "data-residency"],
    ),
]


def load_docs(slugs: list, doc_dir: pathlib.Path) -> list[dict]:
    docs = []
    for slug in slugs:
        p = doc_dir / f"{slug}.json"
        if p.exists():
            docs.append(json.loads(p.read_text()))
    return docs


def build_module_context(code_slugs: list, console_slugs: list) -> str:
    parts = []
    for doc in load_docs(code_slugs, CODE_DIR):
        parts.append(f"[Claude Code — {doc['title']}]\n{doc['content'][:6000]}")
    for doc in load_docs(console_slugs, CONSOLE_DIR):
        parts.append(f"[Claude Console/API — {doc['title']}]\n{doc['content'][:6000]}")
    return "\n\n---\n\n".join(parts)


def generate_module(client: anthropic.Anthropic, module_num: int, title: str, description: str, context: str) -> str:
    print(f"  Generating module {module_num}: {title}...")

    prompt = f"""You are writing one module of a comprehensive power-user course on Claude (Anthropic's AI).

This module is:
Module {module_num} — {title}
Topic: {description}

Here is the official documentation for this module:
<docs>
{context}
</docs>

Write this module following EXACTLY this format:

## Module {module_num} — {title}

### Concepts

[3-6 key concepts the reader must understand. Be concrete and specific. Use the actual feature names, parameters, and behaviors from the docs. Where a concept applies specifically to one product, mark it with [Claude Code] or [Console/API].]

### Exercises

[4-6 hands-on tasks the reader can do right now. Be specific — exact commands, exact UI steps, exact API calls. Mark product-specific steps with [Claude Code] or [Console/API]. Skip steps that require enterprise access or paid features the reader may not have.]

### Quiz

[4-5 questions testing the key concepts. Mix recall and application questions. Do NOT include answers inline — put them in an Answers section below.]

### Answers

[Numbered answers matching the quiz questions above.]

---

Rules:
- Be concrete, not vague. Use actual command names, parameter names, file paths.
- Don't pad with generic advice. Every sentence should teach something specific.
- Keep Concepts to what's truly essential for this module — don't repeat things covered in earlier modules.
- Exercises must be doable. Don't say "create a project" without saying what kind.
- Total length: 400-700 words."""

    message = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=2000,
        messages=[{"role": "user", "content": prompt}],
    )
    return message.content[0].text


def main():
    api_key = os.environ.get("ANTHROPIC_COURSE_KEY") or os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise EnvironmentError("Set ANTHROPIC_COURSE_KEY or ANTHROPIC_API_KEY in your environment.")
    client = anthropic.Anthropic(api_key=api_key)

    # Build checklist
    checklist = "\n".join(
        f"- [ ] Module {i} — {title}" for i, (title, _, _, _) in enumerate(MODULES)
    )

    header = f"""# Claude Power User Course
### Complete Interactive Training — Console Through Code
> Sources: {len(list(CODE_DIR.glob('*.json')))} Claude Code doc pages + {len(list(CONSOLE_DIR.glob('*.json')))} Claude Platform/API doc pages
> Format: Read → Do → Quiz. Work through modules in order.

---

## How This Course Works

Each module follows the same pattern:
1. **Concepts** — what you need to understand
2. **Exercises** — hands-on tasks to run right now
3. **Quiz** — answer from memory before checking answers
4. **Answers** — at the bottom of each quiz section

Product callouts:
- **[Claude Code]** — tasks specific to the Claude Code CLI/app
- **[Console/API]** — tasks specific to platform.claude.com or the API

Progress tracker:

{checklist}

---

"""

    modules_text = []
    for i, (title, description, code_slugs, console_slugs) in enumerate(MODULES):
        context = build_module_context(code_slugs, console_slugs)
        if not context.strip():
            print(f"  Skipping module {i} — no docs loaded")
            continue
        text = generate_module(client, i, title, description, context)
        modules_text.append(text)

    out = header + "\n\n".join(modules_text)
    out_path = BASE / "CLAUDE_COURSE.md"
    out_path.write_text(out)
    print(f"\nWrote {out_path} ({len(out):,} chars, ~{len(out)//5} words)")


if __name__ == "__main__":
    main()
