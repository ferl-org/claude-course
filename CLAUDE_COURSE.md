# Claude Power User Course
### Complete Interactive Training — Console Through Code
> Sources: 67 Claude Code doc pages + 39 Claude Platform/API doc pages
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

- [ ] Module 0 — Mental Model — What Claude Actually Is
- [ ] Module 1 — Models — Choosing the Right Tool
- [ ] Module 2 — The Console & API — Your First Integration
- [ ] Module 3 — Prompt Engineering
- [ ] Module 4 — Claude Code — Setup & First Session
- [ ] Module 5 — Memory — Teaching Claude About Your Project
- [ ] Module 6 — Everyday Workflows
- [ ] Module 7 — Permissions & Security
- [ ] Module 8 — Tools & Tool Use
- [ ] Module 9 — MCP — Connecting Claude to Your Tools
- [ ] Module 10 — Hooks & Automation
- [ ] Module 11 — Skills, Plugins & Subagents
- [ ] Module 12 — IDE Integration
- [ ] Module 13 — Cost & Performance Optimization
- [ ] Module 14 — CI/CD & Headless Automation
- [ ] Module 15 — Agent Teams & Channels
- [ ] Module 16 — Team & Enterprise Deployment
- [ ] Module 17 — Power User Mastery

---

## Module 0 — Mental Model — What Claude Actually Is

### Concepts

1. **Claude is a language model, not a program.** Claude doesn't execute code internally or remember past conversations. It receives text, reasons about it, and produces text. Everything it does — coding, analysis, search — flows from this loop of reading and generating tokens.

2. **Two product surfaces, one model underneath.** The **Console/API** (console.anthropic.com) gives you direct HTTP access to Claude models via the Messages API — you send structured requests, you get structured responses. **Claude Code** is an agentic harness built on top of those same models: it wraps Claude in a tool-use loop with file operations, shell execution, web search, and code intelligence so it can act autonomously inside your development environment.

3. **The agentic loop [Claude Code].** Claude Code works in three blended phases: **gather context** (read files, search code), **take action** (edit files, run commands), and **verify results** (run tests, check output). Each tool call returns information that feeds the next decision. You can interrupt at any point. This loop is what turns a text-generating model into a coding agent.

4. **Tools are what make Claude agentic [Claude Code].** Without tools, Claude only produces text. Claude Code gives Claude five categories of tools: file operations, search, execution (shell commands, git), web access, and code intelligence. Claude chooses which tools to invoke based on your prompt and what it learns at each step.

5. **Multiple models, switchable at runtime.** Claude Code defaults to Sonnet for most tasks. Opus provides stronger reasoning for complex architectural work. You switch mid-session with `/model` or at launch with `claude --model <name>`. The Console/API lets you specify the model per request in the `model` parameter.

6. **Shared configuration across surfaces [Claude Code].** Your `CLAUDE.md` files, settings, and MCP servers work identically whether you run Claude Code in the terminal, VS Code, JetBrains, the desktop app, or the web. The underlying engine is the same.

### Exercises

1. **[Console/API]** Create a free Anthropic Console account at console.anthropic.com. Navigate to **Settings → API Keys** and generate a key. Store it in an environment variable: `export ANTHROPIC_API_KEY=sk-ant-...`

2. **[Console/API]** Make your first API call using curl:
   ```bash
   curl https://api.anthropic.com/v1/messages \
     -H "x-api-key: $ANTHROPIC_API_KEY" \
     -H "anthropic-version: 2023-06-01" \
     -H "content-type: application/json" \
     -d '{"model":"claude-sonnet-4-20250514","max_tokens":128,"messages":[{"role":"user","content":"What are you?"}]}'
   ```
   Read the JSON response. Note the `model`, `content`, and `usage` fields.

3. **[Claude Code]** Install and launch Claude Code in a project directory:
   ```bash
   npm install -g @anthropic-ai/claude-code
   cd ~/any-existing-project
   claude
   ```
   Ask it: `What does this project do?` Watch Claude choose tools (file reads, search) without you telling it which files to open.

4. **[Claude Code]** While still in the session, run `/model` to see available models. Switch to a different model and ask the same question. Compare the depth of reasoning.

5. **[Claude Code]** Interrupt Claude mid-task. Ask it to `refactor the largest file in this project`, then press **Ctrl+C** while it's working. Note that you re-enter the loop — Claude stops and waits for your next instruction.

### Quiz

1. What is the fundamental difference between the Console/API and Claude Code?
2. Name the three phases of the Claude Code agentic loop.
3. If Claude Code had no tools available, what could it still do?
4. You want Claude to use stronger reasoning for a complex architecture decision in Claude Code. What do you do?
5. Where does Claude Code read persistent, project-specific instructions from?

### Answers

1. The Console/API gives direct HTTP access to Claude models (you send messages, you get responses). Claude Code wraps those same models in an agentic harness with tools, context management, and an execution environment so Claude can act autonomously on your codebase.
2. Gather context, take action, verify results — blended together and repeated until the task is complete.
3. Only respond with text. Tools are what let Claude read files, run commands, search, and edit code.
4. Switch to Opus using `/model` during the session or launch with `claude --model opus`.
5. `CLAUDE.md` files in your project (and/or home directory).

## Module 1 — Models — Choosing the Right Tool

### Concepts

1. **Three model tiers, one family.** Claude Opus 4.6 is the most intelligent (best for complex reasoning/agents, $5/$25 per MTok, moderate latency). Claude Sonnet 4.6 is the balanced workhorse ($3/$15 per MTok, fast latency). Claude Haiku 4.5 is the speed/cost leader ($1/$5 per MTok, fastest latency). All three accept text+image input and support extended thinking.

2. **Context windows.** Opus 4.6 and Sonnet 4.6 have a native 1M-token context window. Haiku 4.5 and all legacy models have 200k tokens. In Claude Code, you can explicitly request the 1M window with the aliases `sonnet[1m]` or `opus[1m]`. Previous thinking blocks are automatically stripped from context in multi-turn conversations—you don't pay for them twice.

3. **Thinking modes.** Opus 4.6 uses *adaptive thinking* (`thinking.type: "adaptive"`)—Claude decides when and how deeply to reason. Sonnet 4.6 supports both adaptive and manual thinking (`type: "enabled"` with `budget_tokens`). Haiku 4.5 supports manual extended thinking only, not adaptive. Manual mode on Opus 4.6 is deprecated.

4. **Effort parameter.** Controls total token spend (text, tool calls, *and* thinking) across all models. Four levels: `low`, `medium`, `high` (default), `max` (Opus 4.6 only). For Sonnet 4.6, Anthropic recommends `medium` as the practical default for most workloads.

5. **`opusplan` hybrid mode.** [Claude Code] Uses Opus for planning/architecture, then automatically switches to Sonnet for code execution—combining Opus reasoning quality with Sonnet cost efficiency.

6. **Fast mode.** [Claude Code] Toggle with `/fast`—same Opus 4.6 model, 2.5× faster, at $30/$150 per MTok. Costs are extra-usage only, not included in subscription rate limits. Best enabled at session start to avoid repricing the full cached context.

### Exercises

1. **[Claude Code] Switch models mid-session.** Start a session with `claude --model haiku`. Ask it to explain a regex. Then run `/model sonnet` and ask the same question. Compare response depth and latency.

2. **[Claude Code] Try `opusplan`.** Run `claude --model opusplan`. Prompt: "Plan and implement a Python function that converts Roman numerals to integers, with tests." Observe the status indicator switching from Opus (planning) to Sonnet (writing code).

3. **[Console/API] Compare effort levels.** Send the same prompt—"List 5 edge cases for a URL parser and explain each"—three times using `effort: "low"`, `"medium"`, and `"high"`. Compare token counts in the `usage` object of each response.

4. **[Console/API] Enable adaptive thinking.** Send a request to `claude-opus-4-6` with `thinking: {"type": "adaptive"}` and `effort: "medium"`. Try a simple question ("What is 2+2?") and a hard one ("Prove that the square root of 2 is irrational"). Note whether thinking blocks appear in each response.

5. **[Claude Code] Check your default model.** Run `/model` with no arguments to see your current model. Then run `claude --model opus` and verify with `/model` again. Understand that Pro subscribers default to Sonnet 4.6; Max subscribers default to Opus 4.6.

### Quiz

1. You need to process 500k tokens of log files in a single prompt. Which current models support this natively, and which require a special configuration?

2. What is the key behavioral difference between setting `effort: "low"` and enabling fast mode in Claude Code?

3. In a multi-turn conversation with extended thinking enabled, are previous turns' thinking tokens counted against your context window on subsequent requests?

4. You want Opus-level planning quality but Sonnet-level cost for implementation. What single Claude Code model alias achieves this?

5. Why does Anthropic recommend enabling fast mode at the *start* of a session rather than mid-conversation?

### Answers

1. Opus 4.6 and Sonnet 4.6 have a native 1M-token context window—no special config needed via API. Haiku 4.5 and legacy models are capped at 200k. In Claude Code, use `sonnet[1m]` or `opus[1m]` aliases to explicitly request the 1M window.

2. `effort: "low"` reduces quality/depth (fewer tokens, less thinking, fewer tool calls). Fast mode keeps identical quality at full effort but reduces *latency* at higher per-token cost.

3. No. The API automatically strips thinking blocks from previous turns before calculating context usage. You are billed for thinking tokens only once, when generated.

4. `opusplan`.

5. Switching mid-conversation reprices the *entire* existing conversation context at the higher fast-mode uncached input rate ($30/MTok), making it significantly more expensive than if fast mode had been on from the start.

## Module 2 — The Console & API — Your First Integration

### Concepts

1. **The Workbench** [Console/API]: Located at `platform.claude.com/workbench`, the Workbench lets you prototype prompts in a browser GUI before writing code. You can set a system prompt, add user/assistant message turns, adjust model selection and `max_tokens`, then run the prompt and inspect the full response object — including `stop_reason`, token usage, and model output.

2. **Messages API structure** [Console/API]: Every API call is a `POST` to `https://api.anthropic.com/v1/messages`. The request body requires three fields: `model` (e.g., `"claude-sonnet-4-20250514"`), `max_tokens` (integer cap on output length), and `messages` (an array of `{role, content}` objects alternating between `"user"` and `"assistant"`). There is no `"system"` role in messages — use the top-level `system` parameter instead.

3. **Stateless multi-turn conversations**: The API has no session memory. To continue a conversation, you resend the entire message history each time. You can also inject synthetic `assistant` messages that Claude never actually produced — the API treats them identically to real responses.

4. **Prefilling (putting words in Claude's mouth)**: If the last message in your `messages` array has `role: "assistant"`, Claude continues from that text rather than starting a new turn. Combine with `"max_tokens": 1` to force constrained outputs like a single multiple-choice letter. **Note:** Claude Opus 4.6 does not support prefilling — it returns a 400 error.

5. **Authentication headers**: Every request requires three headers: `x-api-key` (your key from `platform.claude.com/settings/keys`), `anthropic-version: 2023-06-01`, and `content-type: application/json`. The Python and TypeScript SDKs send these automatically.

6. **Response anatomy**: The response JSON contains `id`, `role` (`"assistant"`), `content` (array of blocks, typically `{type: "text", text: "..."}`), `model`, `stop_reason` (`"end_turn"` or `"max_tokens"`), and `usage` with `input_tokens` and `output_tokens` counts.

### Exercises

1. **Explore the Workbench** [Console/API]: Go to `platform.claude.com/workbench`. Set the system prompt to `"You are a concise Unix tutor."` Add a user message: `"Explain what pipe does in one sentence."` Click Run. Note the `input_tokens`, `output_tokens`, and `stop_reason` in the response panel.

2. **Generate an API key** [Console/API]: Navigate to `platform.claude.com/settings/keys`. Create a new key. Copy it and store it as the environment variable `ANTHROPIC_API_KEY` in your shell: `export ANTHROPIC_API_KEY="sk-ant-..."`

3. **Make your first API call with curl** [Console/API]: Run this in your terminal:
   ```bash
   curl https://api.anthropic.com/v1/messages \
     -H "x-api-key: $ANTHROPIC_API_KEY" \
     -H "anthropic-version: 2023-06-01" \
     -H "content-type: application/json" \
     -d '{"model":"claude-sonnet-4-20250514","max_tokens":50,"messages":[{"role":"user","content":"What is the capital of Japan?"}]}'
   ```
   Verify you get a JSON response with `"stop_reason": "end_turn"`.

4. **Make the same call with the Python SDK** [Console/API]: Install with `pip install anthropic`, then run:
   ```python
   from anthropic import Anthropic
   client = Anthropic()
   msg = client.messages.create(
       model="claude-sonnet-4-20250514",
       max_tokens=100,
       messages=[{"role":"user","content":"What is the capital of Japan?"}],
   )
   print(msg.content[0].text, "|", msg.usage)
   ```

5. **Test prefilling** [Console/API]: In the Workbench, add a user message `"Is Python interpreted or compiled? Answer: ("` and an assistant message containing just `"` (empty or a single open token). Observe how Claude continues from the prefilled text. Then try the same structure via curl with `"max_tokens": 1`.

6. **Simulate a multi-turn conversation** [Console/API]: Using the SDK, send a `messages` array with three entries — user, assistant (synthetic), user — and confirm Claude responds coherently to the third turn despite never having produced the second.

### Quiz

1. What three fields are required in every Messages API request body?
2. How do you provide a system prompt in the Messages API — as a message with `role: "system"` or another way?
3. If you want Claude to continue from text you supply, where in the `messages` array do you place it and what `role` does it use?
4. You receive a response with `"stop_reason": "max_tokens"`. What does this tell you?
5. Which three HTTP headers must accompany every direct API request?

### Answers

1. `model`, `max_tokens`, and `messages`.
2. Via the top-level `system` parameter on the request body — there is no `"system"` role in the messages array.
3. As the **last** element in the `messages` array with `role: "assistant"`. Claude treats it as a prefill and continues from that text.
4. Claude's response was truncated because it hit the `max_tokens` limit you set, rather than finishing naturally (`"end_turn"`).
5. `x-api-key`, `anthropic-version`, and `content-type`.

## Module 3 — Prompt Engineering

### Concepts

1. **System prompt vs. user message** [Console/API]: The `system` parameter sets Claude's persistent role/context. User messages go in the `messages` array with `"role": "user"`. System prompts are the right place for role assignments, global constraints, and output format rules. User messages carry the per-turn task.

2. **Turn structure**: The Messages API uses a strict alternating `user`/`assistant` turn structure. You can prefill an `assistant` turn to steer Claude's output format (e.g., start with `{"result":` to force JSON). Each turn is a list of content blocks, not a single string.

3. **XML tags for prompt structure**: Wrapping distinct sections in tags like `<instructions>`, `<context>`, `<example>`, and `<documents>` lets Claude parse complex prompts unambiguously. Nest tags hierarchically—e.g., `<document index="1"><source>` and `<document_content>`—especially for multi-document inputs.

4. **Few-shot examples**: Wrap examples in `<examples>`/`<example>` tags. Make them diverse (cover edge cases) and relevant (mirror real inputs). This is the single most reliable way to control output format, tone, and structure.

5. **Long-context ordering**: Place large documents/data **above** your instructions and query in the prompt. This ordering measurably improves performance. Ask Claude to **quote relevant passages first** before answering to ground responses in source material.

6. **Structured outputs** [Console/API]: Set `output_config.format` to a JSON schema to guarantee valid, parseable JSON via constrained decoding—no more `JSON.parse()` failures. For tool use, set `strict: true` on tool definitions to guarantee parameter types match your schema. These can be combined.

### Exercises

1. **Role + XML prompt** [Console/API]: Send a Messages API request with `system: "You are a senior code reviewer specializing in Python security."` and a user message wrapping code in `<code>` tags. Ask for output in `<issues>` and `<summary>` tags. Verify Claude uses your tags in the response.

2. **Few-shot extraction** [Console/API]: Write a prompt that extracts `name`, `date`, and `amount` from invoice text. Include two `<example>` blocks with different invoice formats (one with a missing date). Send a third invoice as the actual input and confirm Claude handles the missing-field edge case.

3. **Long-context grounding**: Take any document over 2,000 words (a README, article, or PDF text). Place it inside `<document><document_content>...</document_content></document>` at the **top** of your prompt. Below it, write: `First, quote the specific passages relevant to the question, then answer: [your question]`. Compare the answer quality to a prompt without the quoting instruction.

4. **Structured JSON output** [Console/API]: Use the `output_config` parameter with a JSON schema requiring fields `{"sentiment": "string", "confidence": "number", "topics": "array of strings"}`. Send a product review as input. Confirm the response parses without error and matches the schema.

5. **Prefilled assistant turn** [Console/API]: In your `messages` array, add `{"role": "assistant", "content": "```json\n"}` after the user message. Send the request and observe how Claude continues directly in JSON inside a code fence.

### Quiz

1. Where should you place large documents in a prompt relative to your instructions—before or after—and why?

2. What is the purpose of setting `strict: true` on a tool definition, and what specific failure mode does it prevent?

3. You want Claude to always respond in a specific XML structure. What two techniques (from this module) are most effective for ensuring this?

4. A colleague's prompt says `"Format it nicely."` Why is this likely to produce inconsistent results, and what would you change?

5. What happens when you include a partially filled `assistant` turn in the messages array?

### Answers

1. **Before** (above) the instructions. Placing long documents at the top of the prompt significantly improves Claude's ability to reference them accurately.

2. `strict: true` guarantees tool `input` parameters match the declared `input_schema` types exactly. It prevents type mismatches (e.g., `"2"` instead of `2`) and missing required fields that would cause runtime errors in your functions.

3. (a) Provide few-shot `<example>` blocks showing the exact XML structure, and (b) give explicit instructions specifying the tag names and hierarchy Claude must use.

4. `"Nicely"` is ambiguous—Claude has no context for your formatting norms. Replace it with explicit constraints: specify format (e.g., Markdown table), length, and structure (e.g., numbered list of 3 bullet points per section).

5. Claude treats it as a prefix and continues generating from exactly that point, letting you force a specific output format (like starting JSON, a code fence, or a particular opening phrase).

## Module 4 — Claude Code — Setup & First Session

### Concepts

1. **Installation methods**: Claude Code installs via a native installer, Homebrew, or WinGet. The native installer auto-updates in the background; Homebrew and WinGet require manual updates. On Windows, Git for Windows (Git Bash) is required — WSL is an alternative. No Node.js install is needed for the desktop app.

2. **Authentication hierarchy**: Claude Code checks credentials in this order: cloud provider env vars (`CLAUDE_CODE_USE_BEDROCK`, etc.) → `ANTHROPIC_AUTH_TOKEN` → `ANTHROPIC_API_KEY` → `apiKeyHelper` script → stored OAuth credentials from browser login. Running `claude` for the first time triggers a browser-based OAuth flow. Use `/login` to switch accounts; `/logout` to re-authenticate.

3. **Invocation modes**: `claude` starts an interactive REPL session. `claude "task"` runs a one-shot task then returns to the prompt. `claude -p "query"` runs a query and exits (useful for scripting). `claude -c` continues the most recent conversation in the current directory. `claude -r` lets you resume any previous conversation.

4. **Terminal configuration matters**: Shift+Enter for newlines works natively in iTerm2, WezTerm, Ghostty, and Kitty. For VS Code, Alacritty, Zed, and Warp, run `/terminal-setup` inside Claude Code to configure it. Avoid pasting very long content directly — write it to a file and ask Claude to read it instead.

5. **Verification and diagnostics**: `claude --version` confirms installation. `claude doctor` runs a comprehensive check of your installation, authentication, and environment configuration.

### Exercises

1. **Install and verify** [Claude Code]: Install Claude Code using the method for your OS. Run `claude --version` to confirm installation, then run `claude doctor` and note any warnings or errors it reports.

2. **Authenticate and inspect**: Run `claude` in your terminal. Complete the browser login flow. Once inside the session, type `/cost` to see your starting token usage at zero, confirming your account is connected.

3. **Explore a real project**: Clone a small open-source repo (e.g., `git clone https://github.com/expressjs/express.git`), `cd` into it, and run `claude`. Type `what does this project do?` then follow up with `explain the folder structure`. Observe how Claude reads files to build its answer.

4. **Make an edit and commit**: In the same session, type `add a comment at the top of the main entry point file explaining what it does`. Approve the proposed change when prompted. Then type `commit my changes with a descriptive message` and approve the git commit.

5. **Test invocation modes**: Exit the session with `Ctrl+D`. Run `claude -p "what is the license for this project?"` and observe that it prints the answer and exits. Then run `claude -c` to continue where you left off — your previous conversation context should be visible.

6. **Configure your terminal**: Start a new `claude` session and run `/terminal-setup`. Then run `/config` and set your preferred theme. Enable Vim mode by typing `/vim` if you use Vim keybindings.

### Quiz

1. You installed Claude Code via Homebrew. A new version is released. What do you need to do to get it?

2. You have both `ANTHROPIC_API_KEY` set as an environment variable and a stored OAuth login from `claude.ai`. Which credential does Claude Code use?

3. What is the difference between `claude "fix the tests"` and `claude -p "fix the tests"`?

4. You need to paste a 500-line configuration file into Claude Code for analysis. What is the recommended approach?

5. Which command runs a comprehensive diagnostic of your Claude Code installation, authentication, and environment?

### Answers

1. You must manually update — Homebrew and WinGet installations do not auto-update. Run `brew upgrade` or use `claude update`.

2. `ANTHROPIC_API_KEY` takes precedence over stored OAuth credentials. It is higher in the authentication precedence order (position 3 vs. position 5).

3. `claude "fix the tests"` runs the task then drops you into an interactive session. `claude -p "fix the tests"` runs the query and exits immediately, returning you to your shell — useful for piping output or scripting.

4. Don't paste it directly (especially in VS Code's terminal, which truncates long pastes). Instead, save the content to a file and ask Claude to read it: e.g., `read config.yaml and summarize the settings`.

5. `claude doctor`.

## Module 5 — Memory — Teaching Claude About Your Project

### Concepts

1. **Two memory systems, loaded every session** [Claude Code]: `CLAUDE.md` files are instructions *you* write; **auto memory** is notes *Claude* writes when it discovers patterns or you correct it. Both are injected into the context window at session start—they consume tokens, so conciseness matters.

2. **CLAUDE.md scope hierarchy** [Claude Code]: Files are resolved from broad to narrow—managed policy (`/Library/Application Support/ClaudeCode/CLAUDE.md` on macOS), then user (`~/.claude/CLAUDE.md`), then project (`./CLAUDE.md` or `./.claude/CLAUDE.md`). More specific scopes take precedence. Project-level files are committed to git and shared with your team; user-level files are private.

3. **On-demand loading for subdirectories** [Claude Code]: CLAUDE.md files *above* or *at* the working directory load in full at launch. CLAUDE.md files in *subdirectories* load only when Claude reads files in that directory, keeping token cost low for large monorepos.

4. **Scoped rules via `.claude/rules/`** [Claude Code]: Instead of one large CLAUDE.md, you can create topic-specific rule files in `.claude/rules/`. These can target specific file types or subdirectories, so a rule about TypeScript style only loads when Claude is working with `.ts` files.

5. **Auto memory limits** [Claude Code]: Only the first **200 lines** of auto memory are loaded per session. Auto memory is scoped per working tree, not per user. You can review and edit it—it's stored as plain text, not a black box.

### Exercises

1. **Create a project CLAUDE.md** [Claude Code]: In any git repo, create `CLAUDE.md` at the root. Add three concrete lines: your test command (e.g., `Run tests with: npm test`), a naming convention (e.g., `Use camelCase for variables, PascalCase for components`), and one architectural note (e.g., `API routes live in src/routes/; do not import from src/routes/ in src/components/`). Start a new `claude` session and ask Claude to describe the project rules—it should echo your instructions back.

2. **Add a user-level CLAUDE.md** [Claude Code]: Create `~/.claude/CLAUDE.md` with a personal preference, such as `Always use single quotes in JavaScript` or `Prefer concise commit messages under 50 characters`. Open a project that has its own CLAUDE.md and verify both sets of instructions load by asking Claude: "What instructions are you following?"

3. **Create a scoped rule** [Claude Code]: Make the directory `.claude/rules/` in your project. Add a file `python-style.md` containing: `For .py files: use type hints on all function signatures. Use f-strings instead of .format().` Edit a Python file with Claude and confirm it applies these rules. Then edit a JavaScript file and note the rules don't interfere.

4. **Trigger auto memory** [Claude Code]: Start a session and correct Claude on something project-specific—e.g., "No, we use `pnpm` not `npm` in this repo." Then end the session. Start a fresh session and ask Claude how to install dependencies. It should recall `pnpm` without being told again. Inspect the auto memory file to see the saved note.

5. **Audit token cost** [Claude Code]: If your CLAUDE.md has grown large, run a session and note Claude's context usage. Trim redundant or vague lines (e.g., replace "Try to write clean code" with nothing—it adds no signal). Re-check context usage.

### Quiz

1. You have instructions in `~/.claude/CLAUDE.md` and `./CLAUDE.md`. Which takes precedence when they conflict?
2. A CLAUDE.md file exists in `src/api/CLAUDE.md`. When does Claude load it?
3. What is the maximum number of auto memory lines loaded into a session?
4. You want to enforce a rule only for `.tsx` files. Where do you put it?
5. Your teammate doesn't see your preferred code style in Claude's output. You stored the preference in `~/.claude/CLAUDE.md`. Why can't they see it?

### Answers

1. The project-level `./CLAUDE.md` takes precedence—more specific scope wins over user scope.
2. On demand, only when Claude reads files inside the `src/api/` directory—not at launch.
3. **200 lines.**
4. In a file inside `.claude/rules/` (e.g., `.claude/rules/tsx-style.md`), scoped to `.tsx` files.
5. `~/.claude/CLAUDE.md` is user-scoped and local to your machine. It is not committed to version control. The preference must go in the project-level `./CLAUDE.md` or `.claude/rules/` to be shared.

## Module 6 — Everyday Workflows

### Concepts

1. **Codebase exploration workflow** [Claude Code]: Start broad ("Give me an overview of this codebase's architecture"), then narrow ("Find the code that handles user authentication"). Use `@` to reference specific files or directories inline (e.g., `@src/auth/`) so Claude reads them immediately without a separate tool call.

2. **Plan Mode for safe analysis** [Claude Code]: Cycle to Plan Mode with **Shift+Tab** (twice from Normal Mode) or start with `claude --permission-mode plan`. Claude reads files and proposes changes but cannot write anything. Use this for multi-file refactors, architecture reviews, or when you want to iterate on a plan before committing to edits.

3. **Checkpointing and rewind** [Claude Code]: Every prompt automatically creates a checkpoint of edited files. Press **Esc+Esc** or run `/rewind` to open the rewind menu. You can restore code only, conversation only, or both. "Summarize from here" compresses later messages without reverting files — useful for freeing context mid-session. Checkpoints do **not** track bash command side effects (`rm`, `mv`, `cp`).

4. **Test generation workflow** [Claude Code]: Ask Claude to examine your existing test files first so it matches your framework, assertion style, and naming conventions. Then request tests for specific modules. Follow up with "identify edge cases I missed" to get coverage for error conditions and boundary values.

5. **PR creation and session linking** [Claude Code]: After Claude creates a PR via `gh pr create`, the session is automatically linked to that PR number. Resume later with `claude --from-pr <number>` to pick up exactly where you left off.

### Exercises

1. **Explore an unfamiliar repo** [Claude Code]: Clone any open-source project (e.g., `git clone https://github.com/expressjs/express`). Launch `claude` inside it and send: `Give me an overview of this project's architecture and main entry points.` Then follow up: `Find the code responsible for routing middleware.` Note how Claude narrows from structure to specifics.

2. **Plan a refactor without writing code** [Claude Code]: In the same repo, press **Shift+Tab** twice to enter Plan Mode (confirm you see `⏸ plan mode on`). Send: `Plan a refactor of the error-handling logic to use a centralized error handler. List every file that needs changes.` Iterate with follow-ups like `What about backward compatibility?` — verify no files are modified on disk.

3. **Fix a bug with checkpoint safety** [Claude Code]: In a personal project, introduce a deliberate bug (e.g., rename a variable). Switch back to Normal Mode, then ask Claude: `I'm getting a ReferenceError for "userData" — find and fix it.` After Claude edits files, press **Esc+Esc**, select the prompt before the fix, and choose **Restore code and conversation** to rewind. Re-send the prompt to confirm reproducibility.

4. **Generate tests matching project conventions** [Claude Code]: In a project with existing tests, send: `Look at @tests/ to understand my testing patterns, then write unit tests for @src/utils/validate.ts covering happy paths and edge cases.` Review whether Claude matched your assertion library and file naming.

5. **Create a PR end-to-end** [Claude Code]: After making changes, send: `Summarize my changes, then create a PR with a descriptive title and body.` Confirm the PR appears on GitHub, then exit and run `claude --from-pr <number>` to verify session resumption.

### Quiz

1. What does pressing **Esc+Esc** do during a Claude Code session, and what are the available actions?
2. Why should you avoid relying on checkpoints for files modified by bash commands like `rm` or `mv`?
3. How do you enter Plan Mode from Normal Mode using keyboard shortcuts, and what indicator confirms you're in Plan Mode?
4. When you ask Claude to generate tests, what specific step ensures the generated tests match your project's existing style?
5. What happens automatically when Claude creates a PR via `gh pr create`, and how do you leverage it later?

### Answers

1. It opens the rewind menu (equivalent to `/rewind`). Actions: **Restore code and conversation**, **Restore conversation** only, **Restore code** only, **Summarize from here**, or **Never mind**.
2. Checkpointing only tracks direct file edits made through Claude's file editing tools. Bash commands modify files outside that tracking, so those changes cannot be reverted via rewind.
3. Press **Shift+Tab** twice — the first press enters Auto-Accept Mode, the second enters Plan Mode. The terminal shows `⏸ plan mode on`.
4. Point Claude at your existing test files (e.g., `@tests/`) before requesting new tests. Claude examines frameworks, assertion patterns, and naming conventions already in use.
5. The session is automatically linked to the PR number. You resume it later with `claude --from-pr <number>`.

## Module 7 — Permissions & Security

### Concepts

1. **Tiered permission system** [Claude Code]: Tools fall into three categories with different approval behaviors. Read-only tools (file reads, grep) never need approval. File modifications need approval but the "Yes, don't ask again" allowance resets each session. Bash commands need approval but can be permanently allowed per project directory. Rules evaluate in strict order: **deny → ask → allow** — deny always wins.

2. **Permission modes** [Claude Code]: The `defaultMode` setting in `settings.json` controls the baseline behavior. `plan` makes Claude read-only (no edits, no commands). `acceptEdits` auto-approves file writes but still prompts for bash. `dontAsk` auto-denies everything not explicitly pre-approved via `permissions.allow`. `bypassPermissions` skips all prompts except writes to protected directories — use with extreme caution.

3. **Permission rule syntax** [Claude Code]: Rules follow the format `Tool` or `Tool(specifier)`. `Bash(npm run *)` matches any command starting with `npm run ` (the space before `*` enforces a word boundary). `Bash(npm*)` without the space also matches `npmrc` or `npmx`. `Bash(git * main)` matches `git checkout main`, `git merge main`, etc. Compound commands like `git status && npm test` save separate rules per subcommand (up to 5).

4. **Sandboxing** [Claude Code]: The `/sandbox` command enables OS-level isolation (Seatbelt on macOS, bubblewrap on Linux/WSL2). Filesystem isolation restricts writes to the current working directory by default. Network isolation routes traffic through a proxy that blocks unapproved domains. In **auto-allow mode**, sandboxed commands skip permission prompts entirely; in **regular mode**, prompts still appear but the sandbox boundary still enforces restrictions on all child processes.

5. **Data retention and ZDR** [Claude Code]: Commercial users (Team, Enterprise, API) get 30-day retention by default; Anthropic does not train on their data. Consumer users (Free, Pro, Max) can toggle training in privacy settings — opting out reduces retention from 5 years to 30 days. Zero Data Retention is available on Claude for Enterprise and means prompts/responses are not stored after the response is returned. ZDR disables Claude Code on the Web, remote desktop sessions, and `/feedback`.

### Exercises

1. **Inspect current permissions** [Claude Code]: Open Claude Code in any project and run `/permissions`. Note which rules exist and which `settings.json` file each rule comes from (user-level vs. project-level).

2. **Create a deny-first policy** [Claude Code]: In your project's `.claude/settings.json`, add a rule that blocks all `curl` and `wget` while allowing `npm run *` and `git commit *`:
   ```json
   {
     "permissions": {
       "deny": ["Bash(curl *)", "Bash(wget *)"],
       "allow": ["Bash(npm run *)", "Bash(git commit *)"]
     }
   }
   ```
   Then ask Claude to run `curl https://example.com` and verify it is blocked.

3. **Enable sandboxing** [Claude Code]: Run `/sandbox` and select auto-allow mode. Ask Claude to write a file inside your project directory (should succeed silently) and then ask it to write to `/tmp/outside-test.txt` (should trigger a notification or be blocked). Add `"/tmp/build"` to `sandbox.filesystem.allowWrite` in settings and retry.

4. **Test plan mode** [Claude Code]: Set `"defaultMode": "plan"` in your user-level `~/.claude/settings.json`. Start a new session and ask Claude to refactor a function. Confirm it analyzes code but cannot edit files or run commands. Reset the mode afterward.

5. **Check your data privacy setting**: Visit [claude.ai/settings/data-privacy-controls](https://claude.ai/settings/data-privacy-controls) and confirm whether your data is used for model improvement. Note how this changes your retention period (5 years vs. 30 days).

### Quiz

1. If both an `allow` rule for `Bash(git push *)` and a `deny` rule for `Bash(git push *)` exist, which takes effect and why?
2. What is the difference between `Bash(ls *)` and `Bash(ls*)` in a permission rule?
3. In sandbox auto-allow mode, what happens when Claude tries to access a network domain not on the approved list?
4. Which three features are automatically disabled when ZDR is enabled on Claude for Enterprise?
5. What `defaultMode` should you use if you want Claude to auto-deny all tools except those explicitly listed in `permissions.allow`?

### Answers

1. The `deny` rule wins. Rules evaluate in deny → ask → allow order; the first match takes precedence.
2. `Bash(ls *)` enforces a word boundary — it matches `ls -la` but not `lsof`. `Bash(ls*)` has no boundary and matches both.
3. The command falls back to the regular permission flow, prompting the user for approval (or blocks automatically if `allowManagedDomainsOnly` is enabled).
4. Claude Code on the Web, remote desktop sessions, and `/feedback` submission.
5. `dontAsk`.

## Module 8 — Tools & Tool Use

### Concepts

1. **Server tools vs. client tools** [Console/API]: Server tools (`web_search`, `web_fetch`, `code_execution`) execute on Anthropic's servers—you declare them in your request but don't implement them. Client tools (custom functions, `computer_use`, `memory`) execute on your infrastructure—Claude emits a `tool_use` block and you return a `tool_result` with the output.

2. **Web search and web fetch with dynamic filtering** [Console/API]: The `web_search_20260209` and `web_fetch_20260209` tool versions (Opus 4.6/Sonnet 4.6 only) let Claude write and execute code to filter results before they enter the context window. The older versions (`web_search_20250305`, `web_fetch_20250910`) return full content without filtering. Both support `allowed_domains`/`blocked_domains` (mutually exclusive), `max_uses`, and localization (`user_location`).

3. **Code execution as a primitive** [Console/API]: The `code_execution_20250825` tool gives Claude a sandboxed Bash environment with file operations. It is free when combined with `web_search_20260209` or `web_fetch_20260209`. When you also provide a client-side bash tool, Claude operates in two separate environments—state does not persist between them, so your system prompt must clarify which environment to use for what.

4. **Computer use** [Console/API]: The `computer_20251124` tool (beta) gives Claude screenshot capture plus mouse/keyboard control over a virtual desktop. It requires a sandboxed environment you provide (e.g., Docker with Xvfb). An agent loop cycles: Claude requests an action → you execute it → you return a screenshot → Claude decides the next action. Prompt-injection classifiers run automatically on screenshots.

5. **Memory tool** [Console/API]: A client-side tool where Claude issues `view`, `create`, `update`, and `delete` commands against a `/memories` directory you implement. Claude checks this directory at conversation start. You control storage; Claude controls what to remember. This enables cross-conversation learning without bloating the context window.

6. **Claude Code tool names** [Claude Code]: Tools like `Bash`, `Edit`, `Glob`, `Agent`, and `AskUserQuestion` are the exact strings used in permission rules, subagent tool lists, and hook matchers. `Bash` and `Edit` require permission; `Agent`, `AskUserQuestion`, and `Glob` do not.

### Exercises

1. **Basic web search** [Console/API]: Send a Messages API request with `{"type": "web_search_20250305", "name": "web_search", "max_uses": 3, "allowed_domains": ["en.wikipedia.org"]}` in the `tools` array. Ask "When was the Rust programming language first released?" Inspect the response for `server_tool_use`, `web_search_tool_result`, and citation objects.

2. **Fetch + citations** [Console/API]: Add `{"type": "web_fetch_20250910", "name": "web_fetch", "citations": {"enabled": true}, "max_content_tokens": 50000}` to your tools. Ask Claude to summarize `https://www.ietf.org/rfc/rfc2616.txt`. Verify that response text includes `citations` with `char_location` entries.

3. **Code execution for data analysis** [Console/API]: Include `{"type": "code_execution_20250825", "name": "code_execution"}` in your tools. Ask "Generate a CSV of 100 random (x, y) points and compute the Pearson correlation coefficient." Check the response for `bash_code_execution` sub-tool usage and the computed result.

4. **Custom client-side tool** [Console/API]: Define a tool `lookup_order` with `input_schema` requiring `order_id` (string). Send a message "Where is order ORD-4521?" When Claude returns a `tool_use` block, respond with a `tool_result` containing mock tracking data. Confirm Claude incorporates it into its final answer.

5. **Inspect Claude Code tools** [Claude Code]: Run `claude` in a repo directory. Ask Claude to find all TypeScript files containing "async function". Observe it using `Glob` then `Bash` (e.g., `grep`). Check which tool calls required permission approval.

### Quiz

1. You include both `allowed_domains` and `blocked_domains` in a single `web_search` tool definition. What happens?
2. What makes code execution free of additional charges when using the API?
3. In computer use, what happens when the prompt-injection classifier detects a potential injection in a screenshot?
4. A Claude Code permission rule targets the string `Edit`. Does it also cover `Bash` operations that write files via `sed`?
5. You provide both the `code_execution` server tool and a custom client-side `bash` tool. What key risk must your system prompt address?

### Answers

1. The request is invalid—you can use `allowed_domains` or `blocked_domains`, but not both in the same request.
2. Code execution incurs no extra charge (beyond standard token costs) when `web_search_20260209` or `web_fetch_20260209` is included in the request.
3. The classifier automatically steers Claude to ask the user for confirmation before proceeding with the next action.
4. No. `Edit` and `Bash` are separate tool names in Claude Code's permission system. A rule targeting `Edit` does not affect `Bash` commands.
5. State does not persist between Anthropic's sandboxed code execution environment and your client-side bash environment. Your system prompt must instruct Claude to explicitly pass outputs between environments rather than assuming shared files or variables.

## Module 9 — MCP — Connecting Claude to Your Tools

### Concepts

1. **MCP is a protocol, not a feature.** The Model Context Protocol defines how Claude connects to external servers that expose tools (database queries, API calls, file operations). Claude acts as the client; your tool runs as an MCP server. Currently, only the **tool calls** portion of the MCP spec is supported via the API connector.

2. **Three transports, two contexts.** MCP servers communicate over `stdio` (local processes), `sse` (Server-Sent Events), or `streamable-http`. [Claude Code] supports all three via `claude mcp add`. [Console/API] only supports remote servers over HTTPS (`sse` or `streamable-http`)—no local stdio servers.

3. **`mcp_servers` vs. `mcp_toolset` are separate declarations.** [Console/API] In a Messages API request, `mcp_servers` defines *where* to connect (URL, auth token, name). The `tools` array contains an `mcp_toolset` entry that references that server by `mcp_server_name` and controls *which* tools are enabled and how. Every server in `mcp_servers` must be matched by exactly one `mcp_toolset`.

4. **Tool configuration merges with precedence.** [Console/API] System defaults (`enabled: true`, `defer_loading: false`) are overridden by `default_config`, which is overridden by per-tool entries in `configs`. This lets you build allowlist patterns (default `enabled: false`, then enable specific tools) or denylist patterns (default enabled, disable specific tools).

5. **Adding servers in Claude Code.** [Claude Code] The command is `claude mcp add <name> --transport <type> [--env KEY=VALUE] [-- command]`. For remote servers: `claude mcp add my-server --transport http https://example.com/mcp`. For stdio: `claude mcp add my-server --transport stdio -- npx -y some-package`. Environment variables pass secrets without hardcoding them.

### Exercises

1. **[Claude Code] Add a remote MCP server.** Run:
   ```
   claude mcp add demo-fetch --transport http https://fetch.mcp.anthropic.com/http
   ```
   Then start Claude Code and ask it to fetch a webpage. Confirm the tool appears in Claude's available tools.

2. **[Console/API] Make an API call with MCP connector.** Send a Messages API request that connects to a public MCP server. Use this body structure — replace the URL with any public MCP server you have access to:
   ```json
   {
     "model": "claude-sonnet-4-20250514",
     "max_tokens": 1024,
     "mcp_servers": [
       {"type": "url", "url": "https://fetch.mcp.anthropic.com/sse", "name": "fetch-server"}
     ],
     "tools": [
       {"type": "mcp_toolset", "mcp_server_name": "fetch-server"}
     ],
     "messages": [{"role": "user", "content": "Fetch https://example.com and summarize it."}]
   }
   ```

3. **[Console/API] Build an allowlist.** Modify exercise 2: set `default_config.enabled` to `false`, then explicitly enable only one tool by name in `configs`. Verify Claude cannot call the disabled tools.

4. **[Claude Code] Add a stdio server with env vars.** If you have a GitHub token, run:
   ```
   claude mcp add github --transport stdio --env GITHUB_PERSONAL_ACCESS_TOKEN=YOUR_TOKEN -- npx -y @modelcontextprotocol/server-github
   ```
   Ask Claude Code to list your repositories.

5. **[Console/API] Connect two servers in one request.** Add two entries to `mcp_servers` with different names. Add two corresponding `mcp_toolset` entries in `tools`. Send a message that requires tools from both servers.

### Quiz

1. You define a `mcp_servers` entry with `"name": "cal"`. What must be true in the `tools` array?

2. [Console/API] If `default_config` sets `defer_loading: true` and a specific tool in `configs` sets `enabled: false` but doesn't mention `defer_loading`, what is that tool's final `defer_loading` value?

3. Can the MCP connector in the Messages API connect to a local stdio server? Why or why not?

4. [Claude Code] What is the flag to specify transport type when running `claude mcp add`?

5. You want to expose all tools from an MCP server except `delete_everything`. Write the minimal `mcp_toolset` JSON.

### Answers

1. There must be exactly one entry with `"type": "mcp_toolset"` and `"mcp_server_name": "cal"`.

2. `true` — it inherits `defer_loading: true` from `default_config` since the per-tool config doesn't override it.

3. No. The MCP connector only supports publicly exposed HTTPS servers (streamable-http or SSE). Stdio is local-only.

4. `--transport` (e.g., `--transport http`, `--transport sse`, `--transport stdio`).

5. `{"type": "mcp_toolset", "mcp_server_name": "your-server", "configs": {"delete_everything": {"enabled": false}}}`

## Module 10 — Hooks & Automation

### Concepts

1. **Hook lifecycle events** [Claude Code]: Hooks fire at specific points—`SessionStart`, `PreToolUse`, `PostToolUse`, `Notification`, `Stop`, `ConfigChange`, `PreCompact`, `PostCompact`, and others. Each event passes JSON context to your handler via stdin. The event you choose determines *when* your code runs; the `matcher` field filters *which* instances trigger it (e.g., `matcher: "Bash"` on `PreToolUse` targets only shell tool calls, `matcher: "Edit|Write"` on `PostToolUse` targets file edits).

2. **Exit codes control behavior** [Claude Code]: A hook exiting `0` means success (proceed normally). Exit code `2` on a `PreToolUse` hook **blocks** the tool call and feeds your stdout back to Claude as feedback. Any other non-zero exit is treated as a hook failure. This is how you enforce deterministic rules—no LLM judgment involved.

3. **Hook placement in settings files** [Claude Code]: Hooks defined in `~/.claude/settings.json` apply globally. Hooks in `.claude/settings.json` at a project root apply to that project only. The `hooks` key maps event names to arrays of `{matcher, hooks}` objects, where each inner hook has `type: "command"` and a `command` string.

4. **Stdin JSON and `jq` extraction** [Claude Code]: Every hook receives structured JSON on stdin describing the event. Use `jq` to extract fields—e.g., `jq -r '.tool_input.file_path'` pulls the edited file path from a `PostToolUse` event. This is how you pass context from Claude's actions into your shell scripts.

5. **Scheduled prompts with `/loop`** [Claude Code]: The `/loop` skill schedules recurring prompts within a session using cron under the hood. Tasks are session-scoped (lost on exit), have a 3-day expiry, and fire between turns. Up to 50 tasks per session. Intervals support `s`, `m`, `h`, `d` units.

### Exercises

1. **Desktop notification hook** [Claude Code]: Add this to `~/.claude/settings.json` under `"hooks"` → `"Notification"` with `matcher: ""` and command `osascript -e 'display notification "Claude needs input" with title "Claude Code"'` (macOS) or `notify-send "Claude Code" "Claude needs input"` (Linux). Start a session, give Claude a multi-step task, and confirm you get a notification when it pauses.

2. **Auto-format with Prettier** [Claude Code]: In a Node project with Prettier installed, add a `PostToolUse` hook in `.claude/settings.json` with `matcher: "Edit|Write"` and command `jq -r '.tool_input.file_path' | xargs npx prettier --write`. Ask Claude to create a deliberately messy JS file. Verify the saved file is formatted.

3. **Block destructive commands** [Claude Code]: Create `.claude/hooks/block-rm.sh` that reads stdin, pipes through `jq -r '.tool_input.command'`, greps for `rm -rf`, and exits with code `2` echoing `"Blocked: rm -rf is not allowed"` if matched. Wire it as a `PreToolUse` hook with `matcher: "Bash"`. Ask Claude to run `rm -rf /tmp/testdir` and confirm it gets blocked.

4. **Re-inject context after compaction** [Claude Code]: Add a `SessionStart` hook with `matcher: "compact"` whose command outputs your project conventions via `echo` (e.g., `"Use Bun, not npm. Run bun test before committing."`). Force compaction by filling context, then check that Claude follows the re-injected rules.

5. **Schedule a build check** [Claude Code]: In a session, run `/loop 5m check if the latest CI run on main passed`. Verify with `what scheduled tasks do I have?` that the task appears. Cancel it with `cancel the CI check job`.

### Quiz

1. Which exit code must a `PreToolUse` hook return to block a tool call and send feedback to Claude?
2. If you want a hook to run only after file-editing tools (not after Bash or other tools), what event and matcher combination do you use?
3. Where does a hook receive its JSON context—as a command-line argument, an environment variable, or via stdin?
4. What happens to `/loop` scheduled tasks when you exit the Claude Code session?
5. You add a `Notification` hook with `matcher: ""`. When does an empty matcher cause the hook to fire?

### Answers

1. Exit code **2**. Exit 0 means proceed; exit 2 blocks the action and returns stdout as feedback.
2. Event `PostToolUse` with `matcher: "Edit|Write"`.
3. Via **stdin** (as a JSON blob).
4. They are **destroyed**—scheduled tasks are session-scoped and do not survive exit.
5. An empty string matcher matches **all** instances of that event (no filtering).

## Module 11 — Skills, Plugins & Subagents

### Concepts

1. **Skills are markdown playbooks, not code** [Claude Code]. A skill is a `SKILL.md` file with YAML frontmatter (`name`, `description`) and markdown instructions. Claude loads matching skills automatically based on task context, or you invoke one directly with `/skill-name`. Skills live in three scopes: personal (`~/.claude/skills/<name>/SKILL.md`), project (`.claude/skills/<name>/SKILL.md`), or enterprise (managed settings). When names collide, priority is managed > user > project.

2. **Bundled skills orchestrate parallel agents** [Claude Code]. Skills like `/batch`, `/simplify`, and `/loop` ship with Claude Code. `/batch <instruction>` decomposes work into 5–30 units, spawns one background agent per unit in isolated git worktrees, and opens PRs. `/simplify` spawns three review agents in parallel. These are prompt-based, not fixed logic—they adapt to your codebase.

3. **Plugins namespace and package everything** [Claude Code]. A plugin bundles skills, agents, hooks, MCP servers, and LSP configs under a `.claude-plugin/plugin.json` manifest. Plugin skills are namespaced (`/plugin-name:skill-name`) to prevent collisions. Standalone `.claude/` skills use short names like `/deploy`; use plugins when sharing across repos or teams.

4. **Subagents run in isolated context with constrained tools** [Claude Code]. Each subagent gets its own context window, system prompt, and tool allowlist. Define them as markdown files in `.claude/agents/` (project) or `~/.claude/agents/` (user). Frontmatter fields include `description`, `tools`, `disallowedTools`, `model` (e.g., `sonnet` for cost control), `maxTurns`, `permissionMode`, and `isolation`. Claude delegates automatically based on the subagent's `description`.

5. **Marketplaces distribute plugins** [Claude Code]. The official marketplace (`claude-plugins-official`) is built in. Add third-party marketplaces with `/plugin marketplace add owner/repo`. Install plugins with `/plugin install name@marketplace-name`. Refresh catalogs with `/plugin marketplace update`.

### Exercises

1. **Create a project skill** [Claude Code]. In your repo, create `.claude/skills/explain-code/SKILL.md` with frontmatter `name: explain-code` and `description: Explains code using diagrams and analogies. Use when user asks how code works.` Add body instructions: "Use ASCII diagrams. Start with a one-sentence summary. Then walk through the key functions." Test with `/explain-code src/main.ts`.

2. **Test a bundled skill** [Claude Code]. In a git repository, run `/simplify focus on error handling`. Observe that three review agents spawn in parallel. Review the aggregated findings and accept or reject fixes.

3. **Build and test a local plugin** [Claude Code]. Create `my-plugin/.claude-plugin/plugin.json` with `{"name":"my-plugin","version":"1.0.0","description":"Test plugin"}`. Add `my-plugin/skills/greet/SKILL.md` with frontmatter `name: greet` and `description: Greets the user`. Launch Claude Code with `claude --plugin-dir ./my-plugin`, then run `/my-plugin:greet`.

4. **Create a subagent** [Claude Code]. Run `/agents`, choose "Create new", scope it to user level. Name it `security-scanner`, set description to "Scans code for security vulnerabilities. Use after code changes.", restrict tools to `["Read", "Grep", "Glob", "Bash"]`, set model to `sonnet`. Then ask Claude "check this file for security issues" and verify it delegates to `security-scanner`.

5. **Pass subagents via CLI** [Claude Code]. Run: `claude --agents '{"test-runner":{"description":"Runs tests and reports failures","prompt":"You are a test runner. Execute tests and summarize failures.","tools":["Bash","Read"],"maxTurns":5}}'` then ask Claude to run your test suite.

### Quiz

1. What determines whether Claude auto-loads a skill or requires explicit `/skill-name` invocation?
2. How do plugin skill names differ from standalone skill names, and why?
3. Which frontmatter field controls what model a subagent uses, and what's a practical reason to set it?
4. You have a skill named `deploy` at both `~/.claude/skills/deploy/SKILL.md` and `.claude/skills/deploy/SKILL.md`. Which one wins?
5. What command refreshes plugin catalogs from remote marketplaces after they've been updated upstream?

### Answers

1. Claude reads the skill's `description` in frontmatter and loads it automatically when the task context matches. Users can always force invocation with `/skill-name` regardless.
2. Plugin skills are namespaced as `/plugin-name:skill-name`; standalone skills use short names like `/deploy`. Namespacing prevents conflicts when multiple plugins define similarly-named skills.
3. The `model` field (e.g., `"model": "sonnet"`). Setting it to a faster, cheaper model like Haiku or Sonnet controls cost for routine tasks like code scanning.
4. The user-level skill (`~/.claude/skills/`) wins. Priority order is managed > user > project.
5. `/plugin marketplace update`.

## Module 12 — IDE Integration

### Concepts

1. **VS Code Extension Prompt Box** — The Claude Code panel in VS Code supports three permission modes (normal, Plan, auto-accept), `@`-mentions with fuzzy matching and line ranges (e.g., `@app.ts#5-10`), `/` slash commands, a context-window usage indicator, and `Shift+Enter` for multi-line input. Press `Option+K` (Mac) / `Alt+K` (Windows/Linux) to insert an @-mention from your current editor selection.

2. **JetBrains Plugin Integration** — The Claude Code plugin for IntelliJ, PyCharm, WebStorm, etc. displays diffs in the native IDE diff viewer, shares your current selection and diagnostic errors (lint, syntax) automatically, and uses `Cmd+Esc` / `Ctrl+Esc` to launch. From an external terminal, run `claude` then `/ide` to connect to a running JetBrains instance. For Remote Development, the plugin must be installed on the **remote host**, not the local client.

3. **Desktop App Code Tab** — The Claude Desktop app's **Code** tab provides visual diff review with inline comments, live app preview via dev servers, GitHub PR monitoring with auto-fix/auto-merge, parallel sessions using Git worktrees, and scheduled recurring tasks. No Node.js or separate CLI install is required. Sessions can target Local, Remote (Anthropic cloud), or SSH environments.

4. **Chrome Browser Integration** — The `claude-in-chrome` extension (v1.0.36+) lets Claude open tabs, read console logs, click elements, fill forms, and record GIFs. It inherits your browser login state. Launch with `claude --chrome` or run `/chrome` inside a session. Site permissions are managed in the Chrome extension settings.

5. **Remote Control** — Running `claude remote-control` or `/remote-control` registers your local session with the Anthropic API over outbound HTTPS (no inbound ports). You then connect from claude.ai/code or the Claude mobile app. Your local filesystem, MCP servers, and project config remain available. This differs from Claude Code on the web, which runs on Anthropic cloud infrastructure.

### Exercises

1. **VS Code: Plan-mode review** — Install the Claude Code VS Code extension. Open a project, switch the permission mode to **Plan** via the mode indicator at the bottom of the prompt box. Ask Claude to refactor a function. When the plan opens as a markdown document, add an inline comment requesting a change, then let Claude proceed.

2. **JetBrains: Connect from external terminal** — Open a project in IntelliJ or PyCharm with the Claude Code plugin installed. In a separate system terminal, `cd` to the project root, run `claude`, then type `/ide`. Verify the connection by selecting a block of code in the IDE and asking Claude to explain it — your selection should appear in context automatically.

3. **Desktop: Parallel sessions** — Open the Claude Desktop app's Code tab. Start a session on a local repo. From the sidebar, open a second parallel session on the same repo. Observe that Desktop creates a separate Git worktree for each session. Give each session a different task and watch them work independently.

4. **Chrome: Debug a local app** — Start a local dev server (e.g., `npx serve .` on an HTML file). Run `claude --chrome`, then ask: `Open localhost:3000 and check the console for errors.` Confirm Claude navigates to the page and reports console output.

5. **Remote Control: Phone handoff** — Run `claude remote-control --name "my-task"` in your project directory. Scan the displayed QR code with the Claude mobile app. Send a message from your phone and verify it appears in the terminal session, then reply from the terminal and confirm it syncs back.

### Quiz

1. In VS Code, what keyboard shortcut inserts an `@`-mention with the file path and line numbers of your current selection on macOS?
2. When using the JetBrains plugin with Remote Development, where must the plugin be installed — local client or remote host?
3. How does Remote Control differ from Claude Code on the web in terms of where the session executes?
4. What flag do you pass to `claude` to enable Chrome browser integration from the CLI?
5. In the Desktop app's Code tab, what mechanism does parallel sessions use to isolate file changes between sessions?

### Answers

1. `Option+K` (`Alt+K` on Windows/Linux).
2. The remote host.
3. Remote Control executes on your local machine (your filesystem, MCP servers, and config stay available); Claude Code on the web executes on Anthropic-managed cloud infrastructure.
4. `--chrome` (or run `/chrome` inside an existing session to enable it).
5. Git worktrees — each parallel session gets its own worktree so changes don't conflict.

## Module 13 — Cost & Performance Optimization

### Concepts

1. **Prompt caching saves up to 90% on repeated input** [Console/API]. Cache hits cost 1/10th of base input price (e.g., $0.30/MTok vs $3/MTok on Sonnet). Cache writes cost 1.25× base price. The cache has a 5-minute default TTL (refreshed on each hit) or an optional 1-hour TTL at 2× base price. You get 4 breakpoint slots. **Automatic caching** (`"cache_control"` at request top level) moves the breakpoint forward each turn — ideal for multi-turn chat. **Explicit breakpoints** on individual blocks give fine-grained control over what's cached.

2. **Batch processing cuts costs 50%** [Console/API]. The Message Batches API processes up to 100,000 requests asynchronously (most finish within 1 hour). Sonnet 4.6 batch input is $1.50/MTok vs $3/MTok synchronous. Use it for evals, bulk content generation, data analysis — anything that doesn't need real-time responses.

3. **Context management: compaction and clearing** [Console/API]. Server-side compaction (`compact_20260112`) auto-summarizes conversation when input tokens exceed a trigger threshold (minimum 50,000). Tool result clearing (`clear_tool_uses_20250919`) replaces old tool outputs with placeholders. Thinking block clearing (`clear_thinking_20251015`) removes older reasoning blocks. These run server-side — your client keeps the full history.

4. **Model selection directly controls cost** [Claude Code]. Sonnet 4.6 ($3/$15 MTok in/out) handles most coding tasks. Opus ($15/$75) is for complex architectural reasoning. Haiku ($1/$5) works for simple subagent tasks. Use `/model` to switch mid-session. In Claude Code, average daily cost is ~$6/developer on Sonnet.

5. **Context hygiene in Claude Code** [Claude Code]. Every message re-sends the full conversation. Use `/clear` between unrelated tasks. Use `/compact` with custom instructions to control what survives summarization. Run `/context` to audit MCP server overhead — prefer CLI tools (`gh`, `aws`) over MCP servers that add persistent tool definitions.

### Exercises

1. **Measure your baseline** [Claude Code]: Start a session, complete 3-4 coding tasks, then run `/cost`. Note total cost, API duration, and lines changed. Run `/clear`, do similar tasks, and compare the second `/cost` output.

2. **Enable automatic caching** [Console/API]: Send a multi-turn conversation with `"cache_control": {"type": "ephemeral"}` at the request top level. After 3 turns, inspect the response `usage` object — confirm you see `cache_read_input_tokens` increasing and `cache_creation_input_tokens` only on new content.

3. **Submit a batch job** [Console/API]: Create a JSON file with 5 Messages requests, each with a unique `custom_id`. POST to `/v1/messages/batches`. Poll the batch status endpoint until `processing_status` is `"ended"`, then download results. Compare the billed tokens against what 5 synchronous calls would cost.

4. **Configure compaction with a budget** [Console/API]: Set up a Messages request with `context_management.edits` containing `compact_20260112`, a trigger of 80,000 tokens, and `pause_after_compaction: true`. Track `n_compactions` and enforce a total token budget of 500,000 tokens by injecting a wrap-up message when the budget is reached (see the docs' counter pattern).

5. **Audit and trim context** [Claude Code]: Run `/context` in an active session. Identify any MCP servers you're not using and remove them from your config. Replace one MCP-based tool with its CLI equivalent (e.g., switch from a GitHub MCP server to `gh`).

### Quiz

1. What is the cost per MTok for a prompt cache **hit** on Claude Sonnet 4.6, and how does that compare to a cache **write**?
2. By what percentage does the Message Batches API reduce costs compared to synchronous API calls?
3. In Claude Code, what command shows you which MCP servers and tools are consuming context space?
4. You're building an agent that uses heavy tool calls across 200+ turns. Which two server-side context editing strategies should you combine, and why?
5. When using server-side compaction with `pause_after_compaction: true`, what `stop_reason` does the API return?

### Answers

1. Cache hits cost $0.30/MTok; cache writes cost $3.75/MTok. Hits are 10× cheaper than base input ($3/MTok); writes are 1.25× base.
2. 50%.
3. `/context`.
4. `clear_tool_uses_20250919` (removes stale tool results that are no longer needed) and `clear_thinking_20251015` (removes older thinking blocks to reclaim context space). Together they prevent context from growing unboundedly in long agentic loops.
5. `"compaction"`.

## Module 14 — CI/CD & Headless Automation

### Concepts

1. **Non-interactive mode (`-p` flag)** [Claude Code]: The `-p` (or `--print`) flag runs Claude Code headlessly — no TTY required. This is the foundation for all CI/CD usage. Combine it with `--allowedTools` to auto-approve specific tools (e.g., `"Read,Edit,Bash"`) so the agent loop doesn't block waiting for human confirmation.

2. **Structured and streaming output** [Claude Code]: `--output-format json` returns a JSON object with `result`, `session_id`, and usage metadata. Add `--json-schema '{...}'` to get validated structured data in the `structured_output` field. `--output-format stream-json --verbose --include-partial-messages` emits newline-delimited JSON events in real time, including `system/api_retry` events with `attempt`, `retry_delay_ms`, and `error` fields you can use for monitoring.

3. **GitHub Actions integration** [Claude Code]: The `anthropics/claude-code-action@v1` action auto-detects whether it's responding to a PR comment, issue, or review thread. Key inputs: `anthropic_api_key`, `prompt`, and `claude_args` (which accepts flags like `--max-turns 10`, `--model claude-sonnet-4-6`, `--append-system-prompt`). The beta `mode` and `direct_prompt` inputs are removed in v1 — mode is now auto-detected and prompts use `prompt`.

4. **GitLab CI/CD integration** [Claude Code]: Add a job using `image: node:24-alpine3.21`, install Claude Code via `curl -fsSL https://claude.ai/install.sh | bash`, then invoke `claude -p` with `--permission-mode acceptEdits`. Trigger context is passed via pipeline variables (`AI_FLOW_INPUT`, `AI_FLOW_CONTEXT`, `AI_FLOW_EVENT`). Enterprise users can swap in AWS Bedrock or Google Vertex AI as the provider.

5. **Session continuations in CI** [Claude Code]: Use `--output-format json` to capture `session_id` from a run, then pass `--continue` with that session to resume context in a later pipeline step — useful for multi-stage workflows (e.g., analyze → implement → verify).

### Exercises

1. **Run a headless query** [Claude Code]: In any git repo, run:
   ```bash
   claude -p "List all exported functions in this project" --output-format json | jq '.result'
   ```
   Confirm the response is valid JSON and contains the `result` field.

2. **Extract structured data with a schema** [Claude Code]: Run:
   ```bash
   claude -p "List the dependencies in package.json" --output-format json \
     --json-schema '{"type":"object","properties":{"deps":{"type":"array","items":{"type":"string"}}},"required":["deps"]}'
   ```
   Verify the output contains a `structured_output` field matching your schema.

3. **Set up a GitHub Actions workflow** [Claude Code]: In a test repo, create `.github/workflows/claude.yml` with the basic workflow from the docs — `on: issue_comment`, the `anthropics/claude-code-action@v1` step, and `ANTHROPIC_API_KEY` from repository secrets. Open a PR and comment `@claude summarize this PR` to trigger it.

4. **Add a GitLab CI job** [Claude Code]: Add the quick-setup `claude` job from the docs to `.gitlab-ci.yml`. Set `ANTHROPIC_API_KEY` as a masked CI/CD variable under **Settings → CI/CD → Variables**. Trigger manually from **CI/CD → Pipelines** and inspect the job log.

5. **Stream and filter tokens** [Claude Code]: Run:
   ```bash
   claude -p "Explain the strategy pattern" --output-format stream-json --verbose --include-partial-messages | \
     jq -rj 'select(.type == "stream_event" and .event.delta.type? == "text_delta") | .event.delta.text'
   ```
   Observe tokens printing incrementally.

### Quiz

1. What flag makes Claude Code run non-interactively, and what must you combine it with to avoid tool-approval prompts in CI?
2. When using `--json-schema`, which field in the JSON output contains the schema-validated data — `result` or `structured_output`?
3. In the GA version (`@v1`) of `claude-code-action`, how do you pass `--max-turns 10` to Claude — through a dedicated `max_turns` input or through `claude_args`?
4. What `--permission-mode` value is recommended for GitLab CI headless runs to allow file edits without interactive approval?
5. What stream event fields would you check to build a retry progress indicator from `stream-json` output?

### Answers

1. The `-p` (or `--print`) flag. Combine it with `--allowedTools` (e.g., `"Read,Edit,Bash"`) to auto-approve tools.
2. `structured_output`. The `result` field contains the plain-text response.
3. Through `claude_args`. The v1 action removed dedicated inputs like `max_turns`; all CLI flags go in `claude_args`.
4. `acceptEdits`.
5. Events with `type: "system"` and `subtype: "api_retry"`, which include `attempt`, `max_retries`, `retry_delay_ms`, and `error`.

## Module 15 — Agent Teams & Channels

### Concepts

1. **Agent teams vs. subagents** [Claude Code]: Agent teams spawn multiple independent Claude Code sessions that message *each other* directly and share a task list. Subagents run inside one session and can only report back to the caller. Teams cost more tokens but enable real collaboration; subagents are cheaper and better for focused, fire-and-forget work.

2. **Team lead and teammates** [Claude Code]: One session acts as lead—it spawns teammates, assigns tasks, and synthesizes results. You can also message any teammate directly using **Shift+Down** to cycle through them. The lead's terminal shows all teammates and their current tasks.

3. **Display modes** [Claude Code]: `teammateMode` in `settings.json` controls layout. `"in-process"` runs all teammates in one terminal (cycle with Shift+Down). `"tmux"` gives each teammate its own split pane (requires tmux or iTerm2). `"auto"` (default) uses split panes if already inside tmux, otherwise in-process.

4. **Channels** [Claude Code]: A channel is an MCP server that pushes external events (chat messages, CI results, webhooks) into a *running* Claude Code session. Events only arrive while the session is open. You opt in per session with `--channels`. The server declares the `claude/channel` capability and emits `notifications/claude/channel` events over stdio.

5. **Sender allowlists and pairing** [Claude Code]: Every channel plugin maintains an allowlist. For Telegram/Discord, you DM the bot, receive a pairing code, then run `/telegram:access pair <code>` and `/telegram:access policy allowlist` inside Claude Code. Unlisted senders are silently dropped—this is the primary defense against prompt injection via channels.

6. **Enterprise gating** [Claude Code]: On Team/Enterprise plans, channels are disabled by default. An admin must set `channelsEnabled: true` in managed settings. Pro/Max users without an org can use channels immediately by passing `--channels`.

### Exercises

1. **Enable and launch a team** [Claude Code]: Set `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` in your shell (`export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`). Start Claude Code and prompt: *"Create an agent team: one teammate audits package.json dependencies for security issues, another reviews the README for accuracy, and a third checks for unused exports."* Watch the lead spawn teammates and use **Shift+Down** to inspect each one's progress.

2. **Switch display modes** [Claude Code]: Add `{"teammateMode": "in-process"}` to your `~/.claude/settings.json`. Restart and launch the same team. Then change to `"tmux"`, start a `tmux` session, launch Claude Code inside it, and rerun—observe each teammate in its own pane.

3. **Run the fakechat channel** [Claude Code]: Install Bun (`curl -fsSL https://bun.sh/install | bash`). Install the fakechat plugin per the official repo. Start Claude Code with `claude --channels fakechat`. Open the localhost URL in your browser, type a message, and confirm it arrives in the terminal. Verify Claude's reply appears in the browser, not in the terminal output.

4. **Build a minimal webhook channel** [Claude Code]: Create a single-file Bun MCP server that listens on `http://localhost:9090`, declares `claude/channel` capability, and emits `notifications/claude/channel` on each POST. Register it in `.mcp.json` under a server named `webhook`. Launch with `claude --dangerously-load-development-channels server:webhook`. From another terminal, run `curl -X POST http://localhost:9090 -d '{"event":"build_failed","repo":"myapp"}'` and watch Claude react.

5. **Test allowlist enforcement** [Claude Code]: With fakechat running, open a second browser profile (different session). Send a message and confirm it is silently dropped because that sender ID isn't on the allowlist.

### Quiz

1. You need three workers to each edit different functions in the *same file* simultaneously. Should you use agent teams or a single session? Why?
2. What environment variable enables agent teams, and where can you set it besides your shell?
3. A channel MCP server must declare which capability for Claude Code to register its notification listener?
4. On a Team plan, a user runs `claude --channels telegram` but gets a startup warning. What's missing?
5. What is the difference between what you see in the terminal and what appears on the external platform when Claude replies through a channel?

### Answers

1. A single session (or subagents). Agent teams work on independent areas; same-file edits cause conflicts. The docs explicitly list same-file edits as a case where a single session is more effective.
2. `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`. Besides the shell, you can set it in `settings.json` under `"env"`.
3. `claude/channel` (declared in `capabilities.experimental['claude/channel']`).
4. An organization admin must enable `channelsEnabled: true` in managed settings (Admin settings → Claude Code → Channels). Team/Enterprise plans have channels disabled by default.
5. The terminal shows the inbound message, the tool call, and a confirmation (e.g., "sent"), but *not* the reply text. The actual reply text appears only on the external platform (Telegram, Discord, etc.).

## Module 16 — Team & Enterprise Deployment

### Concepts

1. **Analytics dashboards differ by plan.** Claude for Teams/Enterprise uses `claude.ai/analytics/claude-code` and includes PR attribution, GitHub-linked contribution metrics, and CSV export. API (Console) customers use `platform.claude.com/claude-code` and get usage metrics plus spend tracking. Contribution metrics require installing a GitHub app and take ~24 hours to populate.

2. **PR attribution uses session matching.** When contribution metrics are enabled, merged PR diffs are matched against Claude Code session activity. A PR is tagged "with Claude Code" if it contains at least one line written during a session. Only "effective lines" count — lines with >3 characters after normalization, excluding trivial punctuation and brackets.

3. **Code Review is a managed multi-agent service.** Enabled per-org by an admin, it posts inline comments on PRs with severity markers: 🔴 (bug, fix before merge), 🟡 (nit), 🟣 (pre-existing). Reviews are guided by `CLAUDE.md` (general project instructions) and `REVIEW.md` (review-only rules). Trigger modes: automatic on PR open, on push, or manual via `@claude review`.

4. **OpenTelemetry monitoring requires `CLAUDE_CODE_ENABLE_TELEMETRY=1`.** Metrics export via `OTEL_METRICS_EXPORTER` (otlp, prometheus, console) and events via `OTEL_LOGS_EXPORTER` (otlp, console). Admins centralize this through managed settings files so individual developers don't configure it themselves. User prompts are only logged when `OTEL_LOG_USER_PROMPTS=1` is explicitly set.

5. **Server-managed settings vs. endpoint-managed settings.** Server-managed settings are configured in the claude.ai web UI, delivered at authentication time, and require no MDM. Endpoint-managed settings use OS-level policies or managed settings files. When both exist, server-managed settings win and endpoint-managed settings are ignored. Shell commands, custom env vars, and hooks in server-managed settings trigger a security approval dialog on the user's machine.

6. **Network configuration uses standard environment variables.** Proxy: `HTTPS_PROXY`/`HTTP_PROXY`/`NO_PROXY`. Custom CA: `NODE_EXTRA_CA_CERTS`. mTLS: `CLAUDE_CODE_CLIENT_CERT`, `CLAUDE_CODE_CLIENT_KEY`, `CLAUDE_CODE_CLIENT_KEY_PASSPHRASE`. Required allowlist: `api.anthropic.com`, `claude.ai`, `platform.claude.com`.

### Exercises

1. **Enable OTel console export locally.** Run: `CLAUDE_CODE_ENABLE_TELEMETRY=1 OTEL_METRICS_EXPORTER=console OTEL_METRIC_EXPORT_INTERVAL=10000 claude`. Observe metrics printed to stdout every 10 seconds. Note the metric names emitted (e.g., token counts, tool calls).

2. **Add a `REVIEW.md` to a repo.** Create `REVIEW.md` at the repo root with: `Flag any function longer than 50 lines. Skip warnings about missing JSDoc comments.` Open a test PR and comment `@claude review` to observe customized findings.

3. **Simulate managed settings.** Create `~/.claude/managed-settings.json` with: `{"env": {"CLAUDE_CODE_ENABLE_TELEMETRY": "1", "OTEL_METRICS_EXPORTER": "console"}, "permissions": {"deny": ["Bash(rm -rf *)"]}}`. Launch `claude` and run `/permissions` to verify the deny rule appears.

4. **Test proxy configuration.** Set `HTTPS_PROXY=http://localhost:9999` and run `claude`. Observe the connection error confirming Claude Code respects the proxy variable. Unset it afterward.

5. **Explore the analytics dashboard.** [Teams/Enterprise] Navigate to `claude.ai/analytics/claude-code`. Toggle between "Pull requests" and "Lines of code" views on the Leaderboard. Click "Export all users" to download the CSV.

### Quiz

1. What is the minimum condition for a merged PR to be tagged "with Claude Code" in contribution metrics?
2. You want OTel metrics sent to your collector at `http://collector.internal:4317` for all developers. What keys do you put in managed settings JSON?
3. A `REVIEW.md` rule says "Flag any use of `eval()`." What severity level will violations receive?
4. When both server-managed and endpoint-managed settings exist, which takes precedence?
5. Which three URLs must be allowlisted for Claude Code to function behind a corporate firewall?

### Answers

1. It must contain at least one line of code written during a Claude Code session.
2. `"env": {"CLAUDE_CODE_ENABLE_TELEMETRY": "1", "OTEL_METRICS_EXPORTER": "otlp", "OTEL_EXPORTER_OTLP_PROTOCOL": "grpc", "OTEL_EXPORTER_OTLP_ENDPOINT": "http://collector.internal:4317"}`
3. Nit (🟡) — `REVIEW.md` and `CLAUDE.md` violations are treated as nit-level findings.
4. Server-managed settings take precedence; endpoint-managed settings are not used.
5. `api.anthropic.com`, `claude.ai`, and `platform.claude.com`.

## Module 17 — Power User Mastery

### Concepts

1. **Context window is your scarcest resource [Claude Code].** Performance degrades as context fills. Track usage with a custom status line, and structure work so Claude verifies its own output (tests, screenshots, linter checks) rather than you manually reviewing everything.

2. **Explore → Plan → Code → Verify [Claude Code].** Use Plan Mode to separate exploration from execution. Jumping straight to coding produces code that solves the wrong problem. The four-phase workflow prevents wasted context on false starts.

3. **Vision token math [Console/API].** Image tokens are calculated as `(width × height) / 750`. Images over 1568px on the long edge are downscaled automatically, adding latency with no quality gain. Images under 200px on any edge degrade quality. Supported formats: JPEG, PNG, GIF, WebP.

4. **Search result content blocks for RAG citations [Console/API].** Provide `"type": "search_result"` blocks (with `source`, `title`, and `content` fields) either in user messages or as tool return values. Claude automatically produces `search_result_location` citations with `cited_text`, `source`, and positional indices — no prompt engineering needed.

5. **Anthropic does not offer an embedding model [Console/API].** Use Voyage AI (e.g., `voyage-3.5`, `voyage-code-3`). Specify `input_type` as `"document"` for indexing or `"query"` for search queries. Models support up to 32,000 tokens context and configurable dimensions (256, 512, 1024, 2048).

6. **Data residency via `inference_geo` [Console/API].** Pass `"inference_geo": "us"` on any Messages API call to pin inference to US infrastructure. US-only inference on Claude Opus 4.6+ costs 1.1× standard pricing. Workspace-level `allowed_inference_geos` and `default_inference_geo` enforce policy across all keys.

### Exercises

1. **[Console/API] Calculate vision costs.** Take a 1000×1000 px PNG. Compute tokens: `1000*1000/750 ≈ 1334`. At Claude Sonnet 4.6 input pricing ($3/M tokens), confirm cost is ~$0.004/image. Then resize to 800×600 and recalculate.

2. **[Console/API] Build a cited RAG response.** Send a Messages API request with two `search_result` content blocks in the user message — one from `"https://example.com/doc1"` and one from `"https://example.com/doc2"`. Ask Claude a question answerable from both. Inspect the response for `citations` arrays with `search_result_location` objects containing `cited_text`.

3. **[Console/API] Generate and compare embeddings.** Install `voyageai` (`pip install -U voyageai`), set `VOYAGE_API_KEY`, then embed `["How do I reset my password?", "Password reset instructions", "Best pizza in NYC"]` with `voyage-3.5` and `input_type="document"`. Compute cosine similarity between all pairs and confirm the first two are closest.

4. **[Console/API] Pin inference to US.** Make a Messages API call with `"inference_geo": "us"`. Check the response `usage` object for `"inference_geo": "us"`. Then repeat with `"inference_geo": "global"` and compare latency.

5. **[Claude Code] Verify-first workflow.** Open Claude Code and prompt: *"Write a function `parseCSVRow` that handles quoted fields with embedded commas. Write 5 test cases covering edge cases. Run the tests after implementing. Fix failures until all pass."* Observe how providing verification criteria changes Claude's iteration loop.

### Quiz

1. What is the formula for estimating image tokens, and at what long-edge pixel count does the API begin downscaling?
2. What three fields are required on every `search_result` content block?
3. You need code-optimized embeddings with 512 dimensions. Which Voyage model and parameter do you use?
4. What is the pricing multiplier for `inference_geo: "us"` on Claude Opus 4.6+, and does it apply to cache reads?
5. Why does Anthropic's best-practice guide recommend giving Claude a way to verify its own work rather than relying on human review?

### Answers

1. `tokens = (width × height) / 750`. Downscaling begins when the long edge exceeds 1568 pixels.
2. `type` (must be `"search_result"`), `source` (URL or identifier), `title`, and `content` (array of text blocks).
3. `voyage-code-3` with the `output_dimension` parameter set to `512`.
4. 1.1× standard pricing, and yes, it applies to all token categories including cache reads and cache writes.
5. Because context fills fast and LLM performance degrades as it fills. Self-verification (tests, linters, screenshots) lets Claude iterate autonomously without consuming your attention as the sole feedback loop, keeping the human out of the costly retry cycle.