"""
03 - Multi-agent orchestration & subagent delegation
====================================================
Exam focus: Domain 1, Tasks 1.2 & 1.3 (coordinator-subagent, hub-and-spoke,
context passing, parallel spawning).

A COORDINATOR delegates to specialized SUBAGENTS defined via AgentDefinition.
Claude invokes them through the Agent tool (historically named "Task").

KEY EXAM POINTS
---------------
* The coordinator's allowed_tools MUST include the spawning tool.
    - The exam guide (and many SDK builds) call it "Task".
    - It was renamed to "Agent" in Claude Code v2.1.63; current SDKs emit
      "Agent" in tool_use blocks but still list "Task" in system:init.
    - Safest practice: include BOTH and match both names when detecting.
* Subagents run with ISOLATED context. They do NOT inherit the coordinator's
  conversation history - pass everything they need in the prompt / definition.
* Subagents CANNOT spawn their own subagents (don't give them the Agent tool).
* Spawn subagents IN PARALLEL by emitting multiple Task/Agent calls in ONE
  coordinator turn (vs sequential turns).
* Give each subagent only the tools for its role (scoped tool access).

Run:
    pip install claude-agent-sdk
    export ANTHROPIC_API_KEY=sk-ant-...
    python 03_coordinator_subagents.py
"""

import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions, AgentDefinition


def build_research_system() -> ClaudeAgentOptions:
    return ClaudeAgentOptions(
        # Coordinator can spawn subagents + read web. Include BOTH spawn names.
        allowed_tools=["WebSearch", "Read", "Grep", "Glob", "Task", "Agent"],
        system_prompt=(
            "You are a research COORDINATOR. Decompose the user's topic into "
            "BROAD, non-overlapping subtopics that cover the WHOLE question "
            "(avoid the classic failure of covering only one narrow slice). "
            "Delegate searching to the web-researcher subagent and synthesis "
            "to the synthesizer subagent. Spawn independent searches in "
            "parallel. Require every finding to carry its source URL and date."
        ),
        agents={
            # Each subagent: clear description (when to use) + scoped tools.
            "web-researcher": AgentDefinition(
                description=(
                    "Searches the web for a single assigned subtopic and "
                    "returns findings. Use one per subtopic, in parallel."
                ),
                prompt=(
                    "You research ONE subtopic. Return 3-6 findings. For each: "
                    "a one-line claim, a short evidence excerpt, the source "
                    "URL, and the publication date. Do not synthesize."
                ),
                tools=["WebSearch", "Read"],   # scoped - no spawning, no write
                model="sonnet",
            ),
            "synthesizer": AgentDefinition(
                description=(
                    "Combines findings from researchers into a cited report. "
                    "Use after research subtopics return."
                ),
                prompt=(
                    "You synthesize findings passed to you IN THE PROMPT (you "
                    "have no memory of prior turns). Preserve every claim's "
                    "source URL and date. Separate well-supported findings "
                    "from contested ones, and flag any coverage gaps."
                ),
                tools=["Read"],                # no web access -> can't go rogue
                model="sonnet",
            ),
        },
    )


async def main():
    options = build_research_system()
    topic = "Impact of AI on the creative industries (cover music, writing, film, and visual art)"

    async for message in query(prompt=topic, options=options):
        # Detect subagent invocation: match BOTH 'Task' and 'Agent'.
        if hasattr(message, "content") and message.content:
            for block in message.content:
                if getattr(block, "type", None) == "tool_use" and block.name in ("Task", "Agent"):
                    print(f"[spawn] subagent -> {block.input.get('subagent_type')}")
        if hasattr(message, "parent_tool_use_id") and message.parent_tool_use_id:
            print("   (message from inside a subagent)")
        if hasattr(message, "result"):
            print("\nFINAL REPORT:\n", message.result)


if __name__ == "__main__":
    asyncio.run(main())
