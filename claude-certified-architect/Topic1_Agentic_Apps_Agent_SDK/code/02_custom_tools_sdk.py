"""
02 - Tool integration with the Claude Agent SDK (in-process MCP)
================================================================
Exam focus: Domain 2 (Tool Design & MCP Integration), Domain 1 (agent loop).

Instead of hand-writing the agentic loop, the Claude Agent SDK runs it for
you. You define custom tools with the @tool decorator, bundle them into an
in-process MCP server with create_sdk_mcp_server, and pass that server to
query() / ClaudeSDKClient.

KEY EXAM POINTS
---------------
* MCP tool names are namespaced: mcp__<server_name>__<tool_name>.
* `allowed_tools` pre-approves tools so they run without a permission prompt.
* Scope each agent to ONLY the tools it needs - too many tools (e.g. 18 vs
  4-5) degrades tool-selection reliability (Domain 2, Task 2.3).
* Return {"is_error": True} from a handler so the model can react to a
  failure instead of crashing the loop (Domain 2, Task 2.2).

Run:
    pip install claude-agent-sdk
    export ANTHROPIC_API_KEY=sk-ant-...
    python 02_custom_tools_sdk.py
"""

import asyncio
from typing import Any
from claude_agent_sdk import (
    tool,
    create_sdk_mcp_server,
    query,
    ClaudeAgentOptions,
    AssistantMessage,
    ToolUseBlock,
    ResultMessage,
)

# Fake backend "database" for the demo.
_CUSTOMERS = {"C-100": {"name": "Ada Lovelace", "tier": "gold"}}
_ORDERS = {"O-501": {"customer_id": "C-100", "total": 240.0, "status": "shipped"}}


# ---------------------------------------------------------------------------
# Define tools. Note the DISTINCT, non-overlapping descriptions - this is how
# the model decides which tool to call.
# ---------------------------------------------------------------------------
@tool(
    "get_customer",
    "Look up a CUSTOMER record by their customer ID (format: C-###). "
    "Returns name and loyalty tier. Use this to VERIFY identity before any "
    "order or refund operation. Do NOT use for order lookups.",
    {"customer_id": str},
)
async def get_customer(args: dict[str, Any]) -> dict[str, Any]:
    rec = _CUSTOMERS.get(args["customer_id"])
    if not rec:
        return {
            "content": [{"type": "text", "text": "No customer with that ID."}],
            "is_error": True,  # structured failure -> model can recover
        }
    return {"content": [{"type": "text", "text": str(rec)}]}


@tool(
    "lookup_order",
    "Look up an ORDER by its order ID (format: O-###). Returns total, status, "
    "and the owning customer_id. Use for questions about a specific order. "
    "Do NOT use to look up customers.",
    {"order_id": str},
)
async def lookup_order(args: dict[str, Any]) -> dict[str, Any]:
    rec = _ORDERS.get(args["order_id"])
    if not rec:
        return {
            "content": [{"type": "text", "text": "No order with that ID."}],
            "is_error": True,
        }
    return {"content": [{"type": "text", "text": str(rec)}]}


# Bundle tools into an in-process MCP server.
support_server = create_sdk_mcp_server(
    name="support",
    version="1.0.0",
    tools=[get_customer, lookup_order],
)


async def main():
    options = ClaudeAgentOptions(
        mcp_servers={"support": support_server},
        # Scoped allow-list. Names follow mcp__<server>__<tool>.
        allowed_tools=[
            "mcp__support__get_customer",
            "mcp__support__lookup_order",
        ],
        system_prompt=(
            "You are a support agent. Always verify the customer with "
            "get_customer before discussing their orders."
        ),
    )

    prompt = "Look up order O-501 and tell me who it belongs to and its status."
    async for message in query(prompt=prompt, options=options):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, ToolUseBlock):
                    print(f"[tool call] {block.name}({block.input})")
        elif isinstance(message, ResultMessage) and message.subtype == "success":
            print("\nFINAL:", message.result)


if __name__ == "__main__":
    asyncio.run(main())
