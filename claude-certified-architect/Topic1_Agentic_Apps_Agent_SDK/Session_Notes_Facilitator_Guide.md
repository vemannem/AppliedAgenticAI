# Session Notes & Facilitator Guide
## Building Agentic Applications with the Claude Agent SDK
**Claude Certified Architect — Foundations · Topic 1 · Domain 1**
Audience: senior / staff engineers · Format: 36-slide deck + 5 live-code walkthroughs · Target length: 50–60 min + Q&A

> Every slide also carries embedded speaker notes (visible in PowerPoint Presenter View). This guide is the run-of-show: timing, transitions, demo cues, and a Q&A bank. Use it on a second screen or printed.

---

## 1. Before you present (checklist)

- [ ] Open the deck in Presenter View so you can see the embedded notes per slide.
- [ ] Have the `code/` folder open in an editor; terminal ready with `ANTHROPIC_API_KEY` set.
- [ ] Pre-run `04_lifecycle_hooks.py` once so the live demo is warm (and you know it works on the room's network).
- [ ] Open `Agent_SDK_Walkthrough.ipynb` in Colab as a backup demo surface.
- [ ] Decide your depth dial: full 60 min (all 5 walkthroughs) vs. 40 min (walkthroughs 1, 3, 4 only).
- [ ] Keep `Reference_Links.md` open — you'll point people there at the close.

---

## 2. Run-of-show (timing)

| Segment | Slides | Time | Goal |
|--------|--------|------|------|
| Open & framing | 1–4 | 7 min | Set the senior frame: workflows vs agents, when NOT to build one |
| The agent loop | 5–11 | 12 min | Loop mechanics + production controls (the spine) |
| Tools & MCP | 12–15 | 9 min | Custom tools, ACI design, context cost |
| Orchestration & delegation | 16–22 | 12 min | Hub-and-spoke, subagents, isolation, failure modes |
| Lifecycle hooks | 23–27 | 9 min | Deterministic control; the prereq-gate payoff |
| Production & continuity | 28–31 | 7 min | Context/compaction, sessions, errors, operating |
| Land it | 32–36 | 6 min | Reference architectures, cheat sheet, lab, Q&A |

Total ≈ 62 min with Q&A folded in. Cut walkthroughs 2 and 5 to land at ~45.

---

## 3. Segment-by-segment facilitation

### Open & framing (slides 1–4)
- **Slide 1 — Title.** One line: "This is for people who will build and review production agents, not just pass a test. By the end you should be able to look at an agent's architecture and say where it breaks."
- **Slide 3 — Workflows vs agents.** This is your credibility slide. Say plainly: *most teams over-build.* Agency is a cost/latency-for-flexibility trade. Ask: "Who here has an 'agent' that could be three if-statements?" — usually a laugh and a nod.
- **Slide 4 — Five patterns.** Don't lecture all five; name them and have people silently map their own system. Land the last cell: the exam's two scenarios ARE two of these patterns.
- **Transition:** "Whichever pattern you pick, the SDK runs the same loop underneath. Let's open it up."

### The agent loop (slides 5–11)
- **Slide 6 — Loop at a glance.** Count the turns out loud on the auth.ts example. The thing people miss: tool execution happens *automatically* inside the loop; your code only sees the message stream.
- **Slide 8 — Walkthrough 1 (live).** Show the raw Messages-API loop so they see what the SDK automates. Read the three numbered steps against the code. **Money line:** "Never decide completion by reading the assistant's text. Branch on `stop_reason`."
- **Slides 10–11 — Production controls + result subtypes.** This is the senior payoff of the section. Headline: **set a budget.** Then: always check `ResultMessage.subtype` before reading `result`.
- **Transition:** "The loop is the engine. Tools are the hands."

### Tools & MCP (slides 12–15)
- **Slide 13 — Walkthrough 2 (live).** Map the four code comments to the four cards. Hammer: the description is the *only* thing the model uses to pick between similar tools.
- **Slide 14 — ACI.** Drop the SWE-bench anecdote: Anthropic spent more time on tools than on the prompt; switching relative→absolute paths killed a whole error class. "Poka-yoke" = mistake-proof the arguments.
- **Slide 15 — Context cost.** The senior insight: tool schemas cost tokens on *every* turn, so "just add more MCP servers" has a price.
- **Transition:** "One agent with good tools is powerful. Now let's coordinate several."

### Orchestration & delegation (slides 16–22)
- **Slide 16 — Hub & spoke.** Spokes never connect. Why route through the hub? Observability + consistent error handling.
- **Slide 18 — Walkthrough 3 (live).** Gotcha #1: forget `Task`/`Agent` in `allowed_tools` and the coordinator silently does the work itself.
- **Slide 19 — Isolation.** Reframe as a *feature*: a subagent reads 30 files, only the summary returns — main context stays lean. Consequence: pass everything in the spawn prompt.
- **Slide 22 — Failure mode (interactive).** Ask "who's at fault?" before revealing. Answer: the coordinator's decomposition, not the workers. Transferable heuristic: *green workers + wrong output = upstream decomposition problem.*
- **Transition:** "Prompts shape behavior. When a rule must *hold*, we need something stronger."

### Lifecycle hooks (slides 23–27)
- **Slide 23 — Hooks table.** Key sentence: hooks run in *your* process and don't consume model context — so auditing via hooks is free.
- **Slide 24 — Walkthrough 4 (live, the crowd-pleaser).** Run it: the $720 refund gets blocked by the hook. Three points: deny stops it; the reason makes the model pivot; deny wins when multiple hooks fire.
- **Slide 26 — Hooks vs prompts.** *If they remember one thing from this section, it's this slide.* Deterministic vs probabilistic.
- **Slide 27 — Walkthrough 5.** State lives OUTSIDE the model (a Python set); the hook enforces ordering. Walk the four answer options — this is the canonical exam answer.
- **Transition:** "We can build and control one. Now let's run it for real."

### Production & continuity (slides 28–31)
- **Slide 28 — Compaction.** Senior insight: persistent rules belong in CLAUDE.md (re-injected every request, survives compaction), not in the opening prompt.
- **Slide 29 — Sessions.** Three verbs: continue / resume / fork. Nuance: when prior results are stale, a fresh session + injected summary beats resume.
- **Slide 31 — Operating in production.** The "ship it" slide — four pillars: Observe, Bound cost, Constrain, Recover. If someone asks "how do I run this safely at scale?", this is the answer.

### Land it (slides 32–36)
- **Slide 32 — Reference architectures.** Walk each bullet and name the technique behind it (gate, hook, scoping, structured errors). Good recall check.
- **Slide 33 — Cheat sheet.** Speed round; tell people to photograph it.
- **Slide 34 — Lab.** Point to the actual files. Homework: read 01→05, run the Colab, take the MCQ set.
- **Slide 36 — Close / Q&A.** Invite real systems into the room.

---

## 4. Live-demo cues

| # | File | What to show | Watch-out |
|---|------|-------------|-----------|
| 1 | `01_agentic_loop_raw_api.py` | The `stop_reason` branch driving the loop | Needs `anthropic` + key; it's a real API call |
| 2 | `02_custom_tools_sdk.py` | `@tool` + `mcp__support__lookup_order` selection | Needs `claude-agent-sdk` |
| 3 | `03_coordinator_subagents.py` | Coordinator spawning scoped subagents | Will make several calls — can be slow; narrate while it runs |
| 4 | `04_lifecycle_hooks.py` | **$720 refund blocked by PreToolUse** | Best demo; pre-run once to be safe |
| 5 | `05_prerequisite_gate_enforcement.py` | Verify-before-refund gate | Show the `deny` reason in output |

If the network is unreliable, run the Colab notebook cells you pre-executed and walk the saved output instead.

---

## 5. Q&A bank (anticipated questions)

**"How do I stop an agent from running up a huge bill?"**
`max_budget_usd` (recommended default) + `max_turns` as a hard cap + lower `effort` for routine turns. Every `ResultMessage` carries `total_cost_usd`, so meter it.

**"How do I *guarantee* a business rule (refund limit, identity check)?"**
A hook or prerequisite gate — deterministic, enforced in your code outside the model. Never a stronger prompt or more few-shot; those are probabilistic. (Slides 26–27.)

**"One big agent with all the tools, or many small subagents?"**
Subagents when you want context isolation, scoped tools (better selection), or parallelism. One agent when the task is cohesive and the tool set is small (~4–5). Note subagents can't recurse.

**"When should I NOT build an agent at all?"**
When the steps are predictable — use a workflow (you own the control flow): more predictable, cheaper, easier to debug. (Slide 3.)

**"`Task` or `Agent` for spawning?"**
Both. Renamed `Task`→`Agent` in Claude Code v2.1.63; current SDKs emit `Agent` in tool-use blocks but still list `Task` in `system:init`. Include both in `allowed_tools` and match both when detecting. (Slide 20.)

**"How do I observe what the agent did?"**
Stream the typed messages (`AssistantMessage` per turn) for live progress; use `SubagentStart/Stop` and `PostToolUse` hooks for audit trails (no context cost); read cost/usage off `ResultMessage`. (Slides 7, 31.)

**"My long-running agent 'forgets' early instructions."**
Automatic compaction summarized them away. Put persistent rules in CLAUDE.md (re-injected every request) and offload heavy exploration to subagents. (Slide 28.)

**"Resume a session or start fresh?"**
Resume when prior context is still valid (follow-up, recover from a limit). Start fresh with an injected summary when prior tool results are stale — often more robust, especially across hosts. (Slide 29.)

**"How is this different from LangGraph / other frameworks?"**
Per Anthropic's guidance: start from the LLM API directly; frameworks add abstraction that can obscure prompts/responses. The Agent SDK is the Claude Code runtime as a library — you keep close to the loop while getting tools, permissions, sessions, and hooks. (Slide 3.)

---

## 6. If you only have 20 minutes (lightning version)
Slides **3, 6, 8, 16, 19, 24, 26, 33**. That's the framing, the loop + one live demo, hub-and-spoke + isolation, the hooks demo + the deterministic-vs-probabilistic rule, and the cheat sheet. Everything else is optional depth.

---

## 7. Companion assets in this folder
- `Agentic_Apps_Claude_Agent_SDK.pptx` — the deck (speaker notes embedded)
- `code/` — five runnable Python files + the Colab notebook
- `MCQ_Practice_Set.md` — 15 exam-style questions with rationale
- `Reference_Links.md` — annotated official + community sources
