"""
04 - Lifecycle hooks: deterministic control & data normalization
================================================================
Exam focus: Domain 1, Task 1.5 (hooks for tool-call interception & data
normalization) and Task 1.4 (programmatic enforcement vs prompt guidance).

Hooks are callbacks that fire at agent lifecycle events. The two most
exam-relevant:

    PreToolUse   - fires BEFORE a tool runs. Can ALLOW / DENY / modify input.
                   Use for deterministic compliance (block refunds > $500).
    PostToolUse  - fires AFTER a tool returns. Can append additionalContext or
                   replace output. Use to NORMALIZE heterogeneous data
                   (Unix ts, ISO-8601, numeric codes) before the model sees it.

KEY EXAM POINTS
---------------
* Hooks give DETERMINISTIC guarantees; prompt instructions are only
  probabilistic. When a business rule MUST hold (financial limits, identity
  checks), enforce it with a hook, not a prompt.
* PreToolUse returns hookSpecificOutput.permissionDecision:
  "allow" | "deny" | "ask". On DENY, also set permissionDecisionReason so the
  model knows why and doesn't blindly retry.
* If multiple hooks fire, "deny" wins over everything.
* Other lifecycle events: SubagentStart/Stop, Stop, UserPromptSubmit,
  PreCompact, Notification, (TS-only) SessionStart/SessionEnd.

Run:
    pip install claude-agent-sdk
    export ANTHROPIC_API_KEY=sk-ant-...
    python 04_lifecycle_hooks.py
"""

import asyncio
import datetime as dt
from claude_agent_sdk import (
    tool,
    create_sdk_mcp_server,
    ClaudeSDKClient,
    ClaudeAgentOptions,
    HookMatcher,
    AssistantMessage,
    ResultMessage,
)

REFUND_LIMIT = 500.0


# --- A tool that returns a Unix timestamp (heterogeneous format on purpose) --
@tool("lookup_order", "Look up an order; returns total and a Unix timestamp.",
      {"order_id": str})
async def lookup_order(args):
    return {"content": [{"type": "text",
            "text": '{"order_id": "%s", "total": 720.0, "ordered_at": 1719500000}'
                    % args["order_id"]}]}


@tool("process_refund", "Issue a refund for an order. Input: order_id, amount.",
      {"order_id": str, "amount": float})
async def process_refund(args):
    return {"content": [{"type": "text",
            "text": f"Refund of ${args['amount']} issued for {args['order_id']}."}]}


server = create_sdk_mcp_server(name="ops", version="1.0.0",
                              tools=[lookup_order, process_refund])


# ---------------------------------------------------------------------------
# PreToolUse hook: DETERMINISTICALLY block refunds over the policy limit and
# redirect to human escalation. A prompt saying "never refund over $500" would
# fail some % of the time; this never does.
# ---------------------------------------------------------------------------
async def enforce_refund_limit(input_data, tool_use_id, context):
    if input_data.get("tool_name") == "mcp__ops__process_refund":
        amount = float(input_data["tool_input"].get("amount", 0))
        if amount > REFUND_LIMIT:
            return {
                "systemMessage": f"Refund ${amount} exceeds ${REFUND_LIMIT}; escalating.",
                "hookSpecificOutput": {
                    "hookEventName": input_data["hook_event_name"],
                    "permissionDecision": "deny",
                    "permissionDecisionReason": (
                        f"Refunds over ${REFUND_LIMIT} require a human. "
                        "Compile a handoff summary instead of refunding."
                    ),
                },
            }
    return {}  # allow everything else


# ---------------------------------------------------------------------------
# PostToolUse hook: NORMALIZE the Unix timestamp to ISO-8601 and append it as
# additionalContext so the model reasons over a consistent date format.
# ---------------------------------------------------------------------------
async def normalize_timestamps(input_data, tool_use_id, context):
    if input_data.get("tool_name") == "mcp__ops__lookup_order":
        try:
            raw = input_data["tool_response"]["content"][0]["text"]
            import json
            data = json.loads(raw)
            iso = dt.datetime.utcfromtimestamp(data["ordered_at"]).isoformat() + "Z"
            return {"hookSpecificOutput": {
                "hookEventName": input_data["hook_event_name"],
                "additionalContext": f"Normalized ordered_at (ISO-8601): {iso}",
            }}
        except Exception:
            return {}
    return {}


async def main():
    options = ClaudeAgentOptions(
        mcp_servers={"ops": server},
        allowed_tools=["mcp__ops__lookup_order", "mcp__ops__process_refund"],
        hooks={
            "PreToolUse": [HookMatcher(hooks=[enforce_refund_limit])],
            "PostToolUse": [HookMatcher(hooks=[normalize_timestamps])],
        },
    )

    async with ClaudeSDKClient(options=options) as client:
        # This refund (720 > 500) will be blocked by the PreToolUse hook.
        await client.query("Refund order O-501 in full ($720).")
        async for message in client.receive_response():
            if isinstance(message, (AssistantMessage, ResultMessage)):
                print(message)


if __name__ == "__main__":
    asyncio.run(main())
