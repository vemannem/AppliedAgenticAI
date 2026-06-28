# Applied Agentic AI (AAA) — Learning Community

Hands-on materials from the **Applied Agentic AI (AAA) learning community** sessions — slides, runnable notebooks, and session notes for building real LLM-based applications and agents.

---

## Sessions

### 📘 RAG vs Graph RAG vs Hybrid
Real use cases, trade-offs, and step-by-step implementation of the three core retrieval architectures.

| File | What it is |
|------|------------|
| [`RAG_vs_GraphRAG_vs_Hybrid.pptx`](sessions/rag-vs-graphrag-vs-hybrid/RAG_vs_GraphRAG_vs_Hybrid.pptx) | Presentation deck (18 slides) |
| [`RAG_GraphRAG_Hybrid_handson.ipynb`](sessions/rag-vs-graphrag-vs-hybrid/RAG_GraphRAG_Hybrid_handson.ipynb) | Colab notebook — builds all three from scratch |
| [`RAG_GraphRAG_Hybrid_session_notes.md`](sessions/rag-vs-graphrag-vs-hybrid/RAG_GraphRAG_Hybrid_session_notes.md) | Written session notes & references |

**Run the notebook in Colab:** open [colab.research.google.com](https://colab.research.google.com) → *File → Upload notebook* → pick the `.ipynb`. You only need an LLM API key.

**Covered:** the RAG premise · Traditional (vector) RAG · where naive RAG breaks · Graph RAG (knowledge graphs, local vs global search) · the hybrid router · a decision framework · real use cases · pitfalls & best practices.

---

## References (high-star, current as of June 2026)
- [microsoft/graphrag](https://github.com/microsoft/graphrag) — canonical Graph RAG (~33.6k⭐)
- [HKUDS/LightRAG](https://github.com/HKUDS/LightRAG) — simple & fast KG-RAG (~36.5k⭐)
- [gusye1234/nano-graphrag](https://github.com/gusye1234/nano-graphrag) — tiny, readable GraphRAG
- [NirDiamant/RAG_Techniques](https://github.com/NirDiamant/RAG_Techniques) — 40+ RAG notebooks (~27.8k⭐)
- [neo4j/neo4j-graphrag](https://github.com/neo4j/neo4j-graphrag) + [llm-graph-builder](https://github.com/neo4j-labs/llm-graph-builder)
- Papers: [Graph RAG (Edge et al., 2024)](https://arxiv.org/abs/2404.16130) · [LightRAG (Guo et al., 2024)](https://arxiv.org/abs/2410.05779)

---

*Materials are free to reuse and adapt.*
