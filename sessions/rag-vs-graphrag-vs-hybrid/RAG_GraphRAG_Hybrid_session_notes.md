# RAG vs Graph RAG vs Hybrid — Session Notes
**AAA Learning Session · evening hands-on**
Companion notes for the deck (`RAG_vs_GraphRAG_vs_Hybrid.pptx`) and the Colab notebook (`RAG_GraphRAG_Hybrid_handson.ipynb`).

---

## 1. What you'll be able to do after this session
- Explain the retrieval pipeline shared by every RAG system, and why retrieval quality caps answer quality.
- Describe how **Traditional (vector) RAG**, **Graph RAG**, and **Hybrid** differ — in mechanism, cost, and the questions each answers well.
- Choose the right approach for a given use case using a simple decision framework.
- Build all three from scratch on one corpus, and route queries between them.

## 2. Prerequisites
- Comfort with Python and basic LLM/prompting ideas.
- A working understanding of embeddings and vector similarity (we recap it).
- An LLM API key (OpenAI by default; any chat + embedding endpoint works).

## 3. Agenda (≈90 min)
| Time | Segment |
|------|---------|
| 0:00–0:10 | The RAG premise + where naive RAG breaks |
| 0:10–0:25 | Traditional RAG vs Graph RAG — mechanics |
| 0:25–0:40 | Trade-offs, hybrid routing, decision framework, use cases |
| 0:40–1:20 | Hands-on Colab: build all three + router |
| 1:20–1:30 | Compare, evaluate, open discussion |

---

## 4. Core concepts

### 4.1 The RAG premise
An LLM only knows its training data. **Retrieval-Augmented Generation** injects fresh, private, or domain knowledge into the prompt at query time so answers are grounded in *your* data. Every RAG system shares one loop:

> **Query → Retrieve → Augment → Generate**

The retrieval step is the whole game: generation quality is capped by what you retrieve. How you **index and search** your knowledge — flat vectors, a graph, or a mix — is exactly what separates the three approaches.

### 4.2 Traditional (vector) RAG
**Pipeline.** Offline: `Load → Chunk → Embed → Store (vector DB)`. At query time: `Retrieve top-k by similarity → Generate`.

**Mental model.** A smart librarian with sticky notes. Each chunk is an independent point in vector space; a query is embedded the same way and the nearest chunks are returned. Fast, cheap, and **flat** — chunks have no awareness of how they connect.

**Strengths:** simple to build and run; low latency; low cost; trivial updates (just re-embed); strong on single-document, fact-based questions; very mature tooling.

**Best fit:** customer support / FAQ bots, document & policy search, internal knowledge bases, semantic search, chat over a single report.

### 4.3 Where naive RAG breaks down
- **Global questions** ("What are the main themes across all docs?") — top-k similarity only ever sees a few chunks, never the whole corpus.
- **Multi-hop reasoning** (A→B→C across documents) — the connecting facts live in chunks that aren't textually similar to the question.
- **Scattered context** — an entity described in many places gets fragmented; the model never assembles the full picture.

**Root cause:** vectors capture *similarity*, not *relationships*. Graph RAG adds the missing structure.

### 4.4 Graph RAG
**Idea.** Replace the flat chunk list with a **knowledge graph**: extract **entities** (nodes) and **relationships** (edges), then group densely-connected nodes into **communities** with LLM-generated summaries.

**Indexing (offline):** `Chunk → LLM extracts entities + relations → build graph → detect communities + summarise`. This is more expensive than embedding (an LLM call per chunk), which is the main cost trade-off.

**Query — two modes:**
- **Local search** — entity-centric questions: find matching entities, walk their neighbourhood, gather connected facts.
- **Global search** — whole-corpus / thematic questions: map over community summaries, rate & filter, reduce into one global answer (something vector RAG simply cannot do).

**Strengths:** connects facts across documents; multi-hop and relationship reasoning; answers global/thematic questions; higher **explainability** (traceable paths); richer, more comprehensive responses.

**Best fit:** healthcare & biomedical Q&A, legal research, enterprise knowledge management, compliance/audit reasoning, fraud & investigation graphs.

### 4.5 Hybrid — routed retrieval
Don't pick one architecture for every query. Put a lightweight **router** in front that classifies each query and sends it down the cheapest path that can answer it well:

- *Simple / factual* → **Traditional RAG**
- *Multi-hop / thematic* → **Graph RAG**
- *Ambiguous / broad* → **both**, then merge & rerank

**Why it wins:** pay the graph cost only when needed; keep RAG speed for the easy ~80%; one system covers all query types; tune routing as you learn real traffic. The router can start as a keyword/length heuristic and graduate to an LLM classifier.

---

## 5. Side-by-side trade-offs
| Factor | Traditional RAG | Graph RAG | Hybrid |
|--------|-----------------|-----------|--------|
| Best question type | Fact-based, local | Exploratory, multi-hop | Mixed workloads |
| Accuracy on complex Qs | Medium | Very high | High–Very high |
| Speed / latency | Fast | Slower | Routed |
| Explainability | Lower | Higher (paths) | Higher |
| Update speed | Fast (re-embed) | Slower (re-index) | Mixed |
| Relative cost | Low | Higher | Medium–High |

## 6. Decision framework
- Fact-based and answerable from one place? → **Traditional RAG**
- Spans many documents or needs multi-hop reasoning? → **Graph RAG**
- Traffic is mixed, or unsure per query? → **Hybrid + routing**
- Tight latency/budget with simple data? → **Stay with Traditional RAG**

> Most teams **start with RAG**, add **Graph** for the hard ~20%, then formalise the choice as a **router** (Hybrid).

## 7. Real use cases
- **Support assistant → Traditional RAG.** Help-centre articles, single-doc factual queries, latency/cost sensitive, content refreshed daily.
- **Clinical knowledge base → Graph RAG.** Links symptoms, drugs, studies; multi-hop medical reasoning; needs traceable evidence; accuracy over speed.
- **Enterprise "ask-your-docs" → Hybrid.** Mix of quick lookups and cross-team analysis; route simple vs. complex; graph for themes, RAG for facts.

---

## 8. Hands-on: what the Colab builds
The notebook uses one small, fictional tech-ecosystem corpus, deliberately built so facts are **scattered** and **connected through entities** (companies, people, products, acquisitions).

1. **Traditional RAG** — chunk → embed → FAISS → retrieve → generate. Then a *multi-hop* question ("How is Lena Ortiz connected to NimbusDB?") to expose the limitation.
2. **Graph RAG (from scratch)** — LLM extracts `(entity, relation, entity)` triples → `networkx` graph → seed-entity traversal → answer the same question completely **and traceably**.
3. **Hybrid router** — an LLM classifier picks `vector` / `graph` / `both` per query, merging when needed.
4. **Compare & evaluate** — run a fixed question set through all three; add a minimal LLM-as-judge faithfulness check.

**Implementation stack:** OpenAI (`gpt-4o-mini` + `text-embedding-3-small`) · FAISS · networkx · (LangChain-style orchestration). Everything is swappable; a local path via Ollama + `sentence-transformers` is noted in the notebook.

---

## 9. Pitfalls & best practices
**Pitfalls**
- Reaching for Graph RAG when plain RAG suffices.
- Underestimating graph indexing cost and time.
- Poor chunking (too big or too small).
- No evaluation harness — flying blind.
- Stale index after data changes.
- Blaming the LLM for what are really retrieval failures.

**Best practices**
- Start with RAG; add graph only for the hard ~20%.
- Measure faithfulness, recall, relevancy (e.g. **Ragas**) on a **golden Q&A set**.
- Tune chunk size & overlap to your documents.
- Add **reranking** before generation.
- Cache embeddings; re-index incrementally.
- Keep regression tests so quality doesn't silently drift.

> The single biggest real-world lesson: **most "LLM problems" are retrieval problems. Evaluate retrieval first.**

---

## 10. Glossary
- **Chunk** — a passage of a document that gets embedded/indexed.
- **Embedding** — a vector representation of text; nearby vectors ≈ similar meaning.
- **Top-k retrieval** — returning the k most similar chunks to a query.
- **Knowledge graph** — entities (nodes) connected by typed relationships (edges).
- **Community / community summary** — a cluster of densely-connected nodes and its LLM-generated summary; powers global search.
- **Local vs global search** — entity-neighbourhood retrieval vs. corpus-wide map-reduce over summaries.
- **Multi-hop** — an answer requiring you to follow several connected facts.
- **Router** — a classifier that picks which retrieval engine handles a query.
- **Reranking** — reordering retrieved candidates by a stronger relevance model before generation.

---

## 11. References (high-star, current as of June 2026)
- **microsoft/graphrag** — canonical Graph RAG: entity graph + community summaries, local/global search. https://github.com/microsoft/graphrag  *(~33.6k⭐)*
- **HKUDS/LightRAG** — simple & fast KG-RAG; dual-level retrieval, cheap incremental updates. https://github.com/HKUDS/LightRAG  *(~36.5k⭐)*
- **gusye1234/nano-graphrag** — tiny, readable GraphRAG; ideal for learning internals. https://github.com/gusye1234/nano-graphrag
- **NirDiamant/RAG_Techniques** — 40+ notebook tutorials (simple, adaptive, corrective, agentic, graph). https://github.com/NirDiamant/RAG_Techniques  *(~27.8k⭐)*
- **neo4j/neo4j-graphrag** + **neo4j-labs/llm-graph-builder** — build KGs from unstructured data; production graph retrievers on Neo4j.
- **Awesome-GraphRAG (DEEP-PolyU)** — curated surveys, papers, benchmarks, projects.
- **Edge et al., 2024** — *From Local to Global: A Graph RAG Approach to Query-Focused Summarization.* https://arxiv.org/abs/2404.16130
- **Guo et al., 2024** — *LightRAG: Simple and Fast Retrieval-Augmented Generation.* https://arxiv.org/abs/2410.05779

---

## 12. Open discussion prompts
- Built any RAG, GraphRAG, Agent, MCP, CrewAI, LangGraph, ADK or A2A project recently? Share a demo or a learning.
- Where in your own data would multi-hop questions show up?
- What would your router's first heuristic be?

*Reuse and adapt these notes freely.*
