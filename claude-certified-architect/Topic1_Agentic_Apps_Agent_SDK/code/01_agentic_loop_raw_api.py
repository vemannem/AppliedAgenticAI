"""
01 - The Agentic Loop (raw Messages API)
=========================================
Exam focus: Domain 1, Task 1.1 - Design and implement agentic loops.

The agentic loop is the foundation of every agent. The model is called in a
loop; on each turn you inspect `stop_reason`:

    - "tool_use"  -> the model wants to call a tool. Execute it, append the
                     result to the conversation, and loop again.
    - "end_turn"  -> the model is done. Exit the loop.

KEY EXAM POINTS
---------------
* Drive the loop with `stop_reason`, NOT by parsing natural-language text,
  NOT by counting iterations, and NOT by checking for assistant text.
* Tool results are appended to the conversation as a `user` message with
  `tool_result` blocks so the model can reason about the next step.
* This is model-driven decision making (Claude chooses the next tool),
  not a hard-coded decision tree.

Run:
    pip install anthropic
    export ANTHROPIC_API_KEY=sk-ant-...
    python 01_agentic_loop_raw_api.py
"""

import json
from anthropic import Anthropic

client = Anthropic()
MODEL = "claude-sonnet-4-5"  # use a current model string

# ---------------------------------------------------------------------------
# 1. Tool schemas - the model only sees name + description + input_schema.
#    Descriptions are the PRIMARY signal the model uses to pick a tool, so
#    make them specific and non-overlapping (Domain 2, Task 2.1).
# ---------------------------------------------------------------------------
TOOLS = [
    {
        "name": "get_weather",
        "description": (
            "Get the CURRENT weather for a city. Use when the user asks about "
            "temperature or conditions right now. Input: a city name string."
        ),
        "input_schema": {
            "type": "object",
            "properties": {"city": {"type": "string"}},
            "required": ["city"],
        },
    },
]


# ---------------------------------------------------------------------------
# 2. Tool implementations (your real backend would live here).
# ---------------------------------------------------------------------------
def get_weather(city: str) -> dict:
    fake_db = {"paris": "18C, light rain", "tokyo": "27C, clear"}
    return {"city": city, "conditions": fake_db.get(city.lower(), "unknown")}


TOOL_IMPLS = {"get_weather": lambda args: get_weather(**args)}


# ---------------------------------------------------------------------------
# 3. The agentic loop.
# ---------------------------------------------------------------------------
def run_agent(user_prompt: str, max_safety_turns: int = 10) -> str:
    messages = [{"role": "user", "content": user_prompt}]

    # max_safety_turns is a CIRCUIT BREAKER, not the primary stop mechanism.
    for _ in range(max_safety_turns):
        response = client.messages.create(
            model=MODEL,
            max_tokens=1024,
            tools=TOOLS,
            messages=messages,
        )

        # Always append the assistant turn to history.
        messages.append({"role": "assistant", "content": response.content})

        # ---- The decision point: branch on stop_reason ----
        if response.stop_reason == "end_turn":
            # Model is finished. Return its final text.
            return "".join(b.text for b in response.content if b.type == "text")

        if response.stop_reason == "tool_use":
            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    impl = TOOL_IMPLS[block.name]
                    result = impl(block.input)
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": json.dumps(result),
                    })
            # Append tool results as a USER turn, then loop again so the
            # model can incorporate the new information.
            messages.append({"role": "user", "content": tool_results})
            continue

        # Other stop reasons (max_tokens, pause_turn, refusal...) handled here.
        return f"[stopped: {response.stop_reason}]"

    return "[circuit breaker: too many turns]"


if __name__ == "__main__":
    print(run_agent("What's the weather in Paris right now?"))
