# Claude Certified Architect — Foundations · Study & Teaching Repo

Preparation materials for the **Claude Certified Architect – Foundations** certification: for each exam topic, a professional slide deck, runnable code walkthroughs, an MCQ practice set, a facilitator guide, and curated reference links.

The certification covers five domains: Agentic Architecture & Orchestration (27%), Tool Design & MCP Integration (18%), Claude Code Configuration & Workflows (20%), Prompt Engineering & Structured Output (20%), and Context Management & Reliability (15%).

## Repository layout

```
.
├── Claude Certified Architect.pdf          # Official exam guide
├── Topic1_Agentic_Apps_Agent_SDK/          # Topic 1 — Domain 1
│   ├── Agentic_Apps_Claude_Agent_SDK.pptx  # 36-slide deck (speaker notes embedded)
│   ├── Agentic_Apps_Claude_Agent_SDK.pdf   # PDF export of the deck (view on GitHub)
│   ├── Session_Notes_Facilitator_Guide.md  # Run-of-show, talking points, Q&A bank
│   ├── MCQ_Practice_Set.md                 # 15 exam-style questions + rationale
│   ├── Reference_Links.md                  # Annotated official + community sources
│   └── code/                               # Runnable Python + Colab notebook
│       ├── 01_agentic_loop_raw_api.py
│       ├── 02_custom_tools_sdk.py
│       ├── 03_coordinator_subagents.py
│       ├── 04_lifecycle_hooks.py
│       ├── 05_prerequisite_gate_enforcement.py
│       └── Agent_SDK_Walkthrough.ipynb
└── README.md
```

Future topics will be added as sibling `TopicN_*` folders following the same structure.

## Topics

| # | Topic | Primary domain | Status |
|---|-------|----------------|--------|
| 1 | Building agentic applications with the Claude Agent SDK (loops, orchestration, subagent delegation, tools, lifecycle hooks) | Domain 1 | ✅ Complete |

## Running the code

```bash
pip install anthropic claude-agent-sdk
export ANTHROPIC_API_KEY=sk-ant-...
python Topic1_Agentic_Apps_Agent_SDK/code/01_agentic_loop_raw_api.py
```

Or open `Topic1_Agentic_Apps_Agent_SDK/code/Agent_SDK_Walkthrough.ipynb` in Google Colab to run all examples interactively.

## License / use

Personal study and internal learning-group material. The exam guide PDF is Anthropic Confidential (NTK) — review before pushing to any public remote.
