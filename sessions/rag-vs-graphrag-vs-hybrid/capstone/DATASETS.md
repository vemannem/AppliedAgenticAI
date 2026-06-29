# Suggested Datasets

Learners may use any public or permitted internal corpus. The recommended default corpus is a collection of public AI research papers because it naturally supports semantic, relationship, and multi-hop questions.

---

## Recommended corpus: Research Intelligence Assistant

Use papers about retrieval, GraphRAG, and agentic AI.

Suggested sources:

| Topic | Paper / resource | Why useful |
|---|---|---|
| RAG | Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks | Foundation of vector RAG |
| GraphRAG | From Local to Global: A GraphRAG Approach to Query-Focused Summarization | Graph-based retrieval and summarization |
| Hierarchical retrieval | RAPTOR | Tree-structured retrieval |
| Self-evaluation | Self-RAG | Retrieval + critique |
| Corrective RAG | CRAG | Corrective retrieval pipeline |
| Dense retrieval | ColBERT | Retrieval model comparison |
| Knowledge graphs | Neo4j GraphRAG docs | Practical graph database usage |

---

## Alternative domains

### Finance

Use public SEC filings, annual reports, and earnings call transcripts.

Good question types:

- Which companies acquired which products?
- What risks are repeated across filings?
- How are subsidiaries connected?

### Healthcare

Use public medical guidelines and research papers.

Important: Do not provide medical advice. Use the project only for retrieval and summarization demonstrations.

### Legal

Use public regulations, judgments, and policy documents.

Important: Do not provide legal advice. Use the project only for retrieval and summarization demonstrations.

### Software documentation

Use LangChain, LlamaIndex, Neo4j, Chroma, Pinecone, and OpenAI documentation.

Good question types:

- Which components integrate with which stores?
- What are the setup steps?
- Which retrieval strategies are supported?

---

## Dataset quality checklist

Choose a corpus that has:

- At least 5 documents
- At least 30 pages total
- Clear entities
- Clear relationships
- Enough content for semantic questions
- Enough structure for graph questions
- Public or permitted usage rights

---

## Minimum corpus size

For a meaningful capstone:

| Level | Documents | Chunks | Graph nodes | Relationships |
|---|---:|---:|---:|---:|
| Beginner | 5 | 100+ | 50+ | 75+ |
| Intermediate | 10 | 300+ | 150+ | 250+ |
| Advanced | 25+ | 1,000+ | 500+ | 1,000+ |
