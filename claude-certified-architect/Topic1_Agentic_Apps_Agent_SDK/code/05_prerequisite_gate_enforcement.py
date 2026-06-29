"""
05 - Programmatic prerequisite gate (handoff & enforcement patterns)
====================================================================
Exam focus: Domain 1, Task 1.4. This is the pattern behind sample Question 1:
the agent sometimes skips get_customer and refunds the wrong account. The
correct fix is a PROGRAMMATIC PREREQUISITE, not a stronger prompt.

PATTERN
-------
Block lookup_order / process_refund with a PreToolUse hook UNTIL get_customer
has returned a verified customer ID in this session. State is tracked OUTSIDE
the model (a plain Python set), giving a deterministic guarantee that a prompt
("always verify first") cannot.

Why not the alternatives (from the sample question):
  B) "make the system prompt say it's mandatory" -> probabilistic, ~nonzero fail
  C) few-shot examples                            -> still probabilistic
  D) routing classifier                           -> changes tool AVAILABILITY,
                                                     not tool ORDERING

Run:
    pip install claude-agent-sdk
    export ANTHROPIC_API_KEY=sk-ant-...
    python 05_prerequisite_gate_enforcement.py
"""

import asyncio
from claude_agent_sdk import (
    tool, create_sdk_mcp_server, ClaudeSDKClient, ClaudeAgentOptions,
    HookMatcher, AssistantMessage, ResultMessage,
)

# Deterministic session state, held outside the model.
VERIFIED_CUSTOMERS: set[str] = set()
GATED_TOOLS = {"mcp__support__lookup_order", "mcp__support__process_refund"}


@tool("get_customer", "Verify a customer by ID (C-###).", {"customer_id": str})
async def get_customer(args):
    cid = args["customer_id"]
    if cid == "C-100":
        VERIFIED_CUSTOMERS.add(cid)   # mark verified ONLY on a real match
        return {"content": [{"type": "text", "text": "Verified: Ada Lovelace (C-100)."}]}
    return {"content": [{"type": "text", "text": "No such customer."}], "is_error": True}


@tool("lookup_order", "Look up an order (O-###).", {"order_id": str})
async def lookup_order(args):
    return {"content": [{"type": "text", "text": "Order O-501: $240, shipped."}]}


@tool("process_refund", "Refund an order.", {"order_id": str, "amount": float})
async def process_refund(args):
    return {"content": [{"type": "text", "text": f"Refunded ${args['amount']}."}]}


server = create_sdk_mcp_server(
    name="support", version="1.0.0",
    tools=[get_customer, lookup_order, process_refund],
)


async def require_verification(input_data, tool_use_id, context):
    """DENY gated tools until at least one customer is verified."""
    if input_data.get("tool_name") in GATED_TOOLS and not VERIFIED_CUSTOMERS:
        return {"hookSpecificOutput": {
            "hookEventName": input_data["hook_event_name"],
            "permissionDecision": "deny",
            "permissionDecisionReason": (
                "Identity not verified. Call get_customer with a valid "
                "customer ID before any order or refund operation."
            ),
        }}
    return {}


async def main():
    options = ClaudeAgentOptions(
        mcp_servers={"support": server},
        allowed_tools=[
            "mcp__support__get_customer",
            "mcp__support__lookup_order",
            "mcp__support__process_refund",
        ],
        hooks={"PreToolUse": [HookMatcher(hooks=[require_verification])]},
    )

    async with ClaudeSDKClient(options=options) as client:
        # Tempt the agent to skip verification - the hook forces it to verify.
        await client.query(
            "Refund order O-501 for $240 for customer C-100, please."
        )
        async for message in client.receive_response():
            if isinstance(message, (AssistantMessage, ResultMessage)):
                print(message)


if __name__ == "__main__":
    asyncio.run(main())
