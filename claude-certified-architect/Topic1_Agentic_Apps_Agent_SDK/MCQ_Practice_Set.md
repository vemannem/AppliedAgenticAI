# MCQ Practice Set — Building Agentic Applications with the Claude Agent SDK

**Claude Certified Architect — Foundations**
**Topic 1 · Domain 1: Agentic Architecture & Orchestration** (with touches of Domains 2 & 5)

Format matches the exam: one correct answer, three distractors, scenario-grounded. Answers and rationale are at the bottom — try all 15 first.

---

## Section A — Agentic loops (Task 1.1)

**Q1.** Your agent runs a loop calling the Messages API. Which signal should *primarily* decide whether the loop continues or terminates?

A. Whether the assistant's latest message contains any text content
B. The `stop_reason` field (`"tool_use"` to continue, `"end_turn"` to stop)
C. A fixed maximum-iteration counter that ends the loop after N turns
D. Whether the assistant's text contains a phrase like "I'm done" or "final answer"

---

**Q2.** After the model returns a `tool_use` block and you execute the tool, how should the result be returned so the model can reason about the next step?

A. Appended to the conversation as a `user` message containing a `tool_result` block referencing the `tool_use_id`
B. Concatenated into the system prompt before the next call
C. Returned as a new `assistant` message so it appears to come from the model
D. Stored in an external database and summarized in plain English in the next user turn

---

**Q3.** Which of the following is an **anti-pattern** for controlling an agentic loop?

A. Inspecting `stop_reason` each turn
B. Appending tool results to conversation history between iterations
C. Parsing the assistant's natural-language output to detect when work is "finished"
D. Keeping a high iteration cap purely as a safety circuit breaker

---

## Section B — Multi-agent orchestration (Tasks 1.2, 1.3)

**Q4.** In a hub-and-spoke research system, what is the coordinator responsible for?

A. Letting each subagent call other subagents directly to speed up the pipeline
B. Task decomposition, delegation, result aggregation, and deciding which subagents to invoke
C. Sharing its full conversation history automatically with every subagent
D. Executing all web searches itself and passing raw HTML to subagents

---

**Q5.** A research system's final reports on "impact of AI on creative industries" only ever cover visual arts, never music, writing, or film. Logs show the coordinator decomposed the topic into "digital art," "graphic design," and "photography." Each subagent succeeded at its assigned task. Most likely root cause?

A. The synthesis agent lacks coverage-gap detection
B. The coordinator's task decomposition was too narrow, omitting whole domains
C. The web-search agent's queries weren't comprehensive enough
D. The document-analysis agent filtered out non-visual sources

---

**Q6.** For a coordinator to spawn subagents in the Agent SDK, what must be true?

A. Each subagent must include the spawning tool so it can recurse
B. The coordinator's allowed tools must include the spawning tool (`Task`/`Agent`)
C. Subagents automatically inherit the coordinator's tools, so no configuration is needed
D. The coordinator must run in plan mode

---

**Q7.** How do subagents receive the context they need to do their work?

A. They automatically inherit the parent's conversation history and tool results
B. Context must be explicitly provided in the prompt / agent definition — subagents start with isolated context
C. They share a global memory store updated live by the coordinator
D. They read the parent's system prompt at spawn time

---

**Q8.** You need three independent web searches to run as fast as possible. What does the coordinator do?

A. Emit multiple `Task`/`Agent` tool calls in a **single** response so they run in parallel
B. Emit one search per turn across three separate turns
C. Give one subagent all three queries to run sequentially
D. Increase `max_tokens` so all searches fit in one completion

---

**Q9.** The synthesis agent in your pipeline keeps trying to run web searches itself, sometimes badly. Best fix consistent with scoped tool access?

A. Give the synthesis agent every web tool so it stops failing
B. Restrict the synthesis agent's tool set to its role; route real searches through the coordinator (optionally give it a narrow `verify_fact` tool for the common case)
C. Add a prompt line telling it "never search the web"
D. Merge the synthesis and search agents into one agent

---

## Section C — Lifecycle hooks & enforcement (Tasks 1.4, 1.5)

**Q10.** A business rule requires that refunds over $500 must never be auto-issued. Which approach gives a deterministic guarantee?

A. A strongly worded system prompt stating the $500 limit
B. Few-shot examples showing the agent escalating large refunds
C. A `PreToolUse` hook that denies `process_refund` when `amount > 500` and redirects to escalation
D. A higher-tier model that follows instructions more reliably

---

**Q11.** Different MCP tools return dates as Unix timestamps, ISO-8601 strings, and numeric codes. You want the model to always see a normalized format. Which hook fits?

A. `PreToolUse`, by rewriting the user's prompt
B. `PostToolUse`, by transforming/augmenting the tool result before the model processes it
C. `SessionStart`, by setting a global date format
D. `Stop`, by reformatting the final answer

---

**Q12.** In a `PreToolUse` hook you set `permissionDecision: "deny"`. Why also set `permissionDecisionReason`?

A. It is required syntax or the hook errors
B. So the model understands why the call was blocked and avoids blindly retrying
C. It automatically escalates to a human
D. It converts the denial into an "ask" decision

---

**Q13.** Production data shows the agent skips `get_customer` ~12% of the time and looks up orders by stated name, causing misidentified accounts. Most effective fix?

A. Add a programmatic prerequisite that blocks `lookup_order`/`process_refund` until `get_customer` returns a verified customer ID
B. Make the system prompt say verification is mandatory
C. Add few-shot examples showing verification first
D. Add a routing classifier that enables only a subset of tools per request

---

## Section D — Tooling & reliability crossovers (Domains 2 & 5)

**Q14.** Two tools have minimal descriptions ("Retrieves customer information" / "Retrieves order details") and the model frequently picks the wrong one. Best *first* step?

A. Add 5–8 few-shot examples of correct routing to the system prompt
B. Expand each tool's description with input formats, example queries, edge cases, and when to use it vs the similar tool
C. Build a keyword-based routing layer before each turn
D. Merge both into a single `lookup_entity` tool

---

**Q15.** A web-search subagent times out. Which error-propagation design best enables coordinator recovery?

A. Return structured error context: failure type, attempted query, partial results, and possible alternatives
B. Retry with backoff internally, then return a generic "search unavailable" after exhausting retries
C. Catch the timeout and return an empty result set marked successful
D. Let the exception bubble to a top-level handler that kills the whole workflow

---

---

## Answer Key & Rationale

**Q1 — B.** The loop is driven by `stop_reason`. Checking for text (A, D) or using an iteration cap as the primary stop (C) are the named anti-patterns.

**Q2 — A.** Tool results go back as a `user` turn with a `tool_result` block keyed by `tool_use_id`, so the model can reason over them on the next iteration.

**Q3 — C.** Parsing natural-language "finished" signals is an explicit anti-pattern. A and B are correct practice; D (high cap as a *safety* breaker) is acceptable as long as it isn't the *primary* stop.

**Q4 — B.** The coordinator owns decomposition, delegation, aggregation, and selection. Subagents don't talk to each other directly (A); context isn't auto-shared (C); the coordinator shouldn't do all the work itself (D).

**Q5 — B.** The logs show the decomposition itself omitted whole domains. The subagents executed correctly within their (too-narrow) assignments, so blaming downstream agents (A, C, D) is wrong.

**Q6 — B.** The coordinator's `allowed_tools` must include the spawn tool. Subagents must **not** include it (they can't recurse), tools aren't auto-inherited, and plan mode is unrelated.

**Q7 — B.** Subagents start with isolated context; everything they need must be passed explicitly in the prompt / `AgentDefinition`.

**Q8 — A.** Parallelism comes from emitting multiple spawn calls in one response. Separate turns (B) or one sequential subagent (C) are slower; `max_tokens` (D) is irrelevant.

**Q9 — B.** Principle of least privilege: scope tools to the role and route exceptions through the coordinator, optionally adding a narrow tool for the high-frequency case. Over-provisioning (A), prompt-only bans (C), and collapsing roles (D) are weaker.

**Q10 — C.** Hooks give deterministic guarantees; prompts and examples are probabilistic; a "better" model still has nonzero failure on must-hold rules.

**Q11 — B.** `PostToolUse` intercepts results after execution — the right place to normalize heterogeneous formats before the model sees them.

**Q12 — B.** The reason is fed back so the model knows why and doesn't retry pointlessly; it's not required syntax, doesn't auto-escalate, and doesn't change the decision type.

**Q13 — A.** Critical ordering for financial logic needs programmatic enforcement. B and C are probabilistic; D addresses tool *availability*, not tool *ordering* (the actual problem).

**Q14 — B.** Tool descriptions are the primary selection mechanism; enriching them is the low-effort, high-leverage first step. Few-shot (A) adds tokens without fixing the root cause; a routing layer (C) and consolidation (D) are heavier than a "first step" warrants.

**Q15 — A.** Structured error context lets the coordinator decide intelligently (retry, alternative, or proceed with partial results). Generic statuses (B) hide context; marking failure as success (C) suppresses recovery; killing the workflow (D) is disproportionate.

---

### Score guide
13–15 correct: exam-ready on this domain · 10–12: solid, review misses · <10: re-read Domain 1 task statements and re-run the code walkthrough.
