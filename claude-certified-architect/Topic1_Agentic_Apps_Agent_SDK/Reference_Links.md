# Reference Links — Agentic Applications with the Claude Agent SDK

Curated, top-rated references for **Topic 1 (Domain 1: Agentic Architecture & Orchestration)**. Official Anthropic docs first (authoritative for the exam), then high-quality community deep-dives. Last verified June 2026.

## ⭐ Official — start here (authoritative)

**Agent SDK core**
- Agent SDK overview — https://platform.claude.com/docs/en/agent-sdk/overview
- Quickstart — https://platform.claude.com/docs/en/agent-sdk/quickstart
- How the agent loop works — https://platform.claude.com/docs/en/agent-sdk/agent-loop
- Handling stop reasons (`tool_use` vs `end_turn`) — https://platform.claude.com/docs/en/build-with-claude/handling-stop-reasons

**Subagents & orchestration**
- Subagents in the SDK (`agents` param, `AgentDefinition`, what subagents inherit, parallel + resume) — https://platform.claude.com/docs/en/agent-sdk/subagents
- Claude Code subagents (filesystem `.claude/agents/`, deeper reference) — https://code.claude.com/docs/en/sub-agents
- Orchestrate teams of Claude Code sessions — https://code.claude.com/docs/en/agent-teams

**Tools & MCP integration**
- Define custom tools (`@tool`, `create_sdk_mcp_server`, `mcp__server__tool`, `is_error`) — https://platform.claude.com/docs/en/agent-sdk/custom-tools
- Connect MCP servers — https://platform.claude.com/docs/en/agent-sdk/mcp
- Tool use overview — https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview
- How tool use works — https://platform.claude.com/docs/en/agents-and-tools/tool-use/how-tool-use-works
- `tool_choice` and tool-use behavior — https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview

**Lifecycle hooks**
- Control execution with hooks (`PreToolUse`/`PostToolUse`, matchers, allow/deny, `updatedInput`, `additionalContext`) — https://platform.claude.com/docs/en/agent-sdk/hooks
- Claude Code hooks reference (full JSON I/O, all events, matcher patterns) — https://code.claude.com/docs/en/hooks
- Hooks guide (shell-command examples) — https://code.claude.com/docs/en/hooks-guide

**Sessions, permissions, structured output**
- Work with sessions (resume, fork) — https://platform.claude.com/docs/en/agent-sdk/sessions
- Handling permissions — https://platform.claude.com/docs/en/agent-sdk/permissions
- Structured outputs in the SDK — https://platform.claude.com/docs/en/agent-sdk/structured-outputs

**SDK API references**
- Python SDK reference — https://platform.claude.com/docs/en/agent-sdk/python
- TypeScript SDK reference — https://platform.claude.com/docs/en/agent-sdk/typescript

**Conceptual / engineering blog (highly recommended)**
- Building effective agents (Anthropic engineering) — https://www.anthropic.com/engineering/building-effective-agents
- Building agents with the Claude Agent SDK — https://www.anthropic.com/engineering/building-agents-with-the-claude-agent-sdk
- How we built our multi-agent research system — https://www.anthropic.com/engineering/multi-agent-research-system

## 📦 Source & examples
- Python SDK on GitHub — https://github.com/anthropics/claude-agent-sdk-python
- TypeScript SDK on GitHub — https://github.com/anthropics/claude-agent-sdk-typescript
- Anthropic Cookbook (tool use, agents) — https://github.com/anthropics/anthropic-cookbook
- Model Context Protocol spec & docs — https://modelcontextprotocol.io

## 👥 Community deep-dives (for intuition, not exam authority)
- "The Claude Agent SDK: Subagents, Sessions and Why It's Worth It" — https://www.ksred.com/the-claude-agent-sdk-what-it-is-and-why-its-worth-understanding/
- Claude Code subagents & orchestration guide (hidekazu-konishi) — https://hidekazu-konishi.com/entry/claude_code_subagents_and_orchestration_guide.html
- "Building Agents with Claude Code's SDK" (PromptLayer) — https://blog.promptlayer.com/building-agents-with-claude-codes-sdk/
- Claude Code parallel agents & orchestrator coordination (MindStudio) — https://www.mindstudio.ai/blog/claude-code-agent-teams-parallel-agents
- Claude Code hooks: production patterns — https://www.pixelmojo.io/blogs/claude-code-hooks-production-quality-ci-cd-patterns

## 🎯 Exam-mapping quick notes
- The exam guide (Feb 2025) refers to the spawn tool as **`Task`** and to `allowedTools` including `"Task"`. Current SDKs renamed it to **`Agent`** (Claude Code v2.1.63) but still emit `"Task"` in the init tools list. **Know both.**
- Hooks vs prompts: hooks = **deterministic**; prompts = **probabilistic**. Choose hooks for must-hold business rules.
- Subagents = **isolated context**, **cannot spawn** their own subagents, **scoped tools**.
- Drive loops on **`stop_reason`**, never on parsed text or an iteration cap as the primary stop.
