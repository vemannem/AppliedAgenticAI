# Validation Checklist

Use this checklist before final submission.

---

## Environment

- [ ] `.env` file is configured locally.
- [ ] No API keys are committed to Git.
- [ ] Dependencies install successfully.
- [ ] README setup instructions are accurate.

---

## Data ingestion

- [ ] Documents download or load successfully.
- [ ] Text extraction works.
- [ ] Chunking produces reasonable chunks.
- [ ] Metadata includes document name and source.
- [ ] Processed chunks can be saved and reloaded.

---

## Vector RAG

- [ ] Embeddings are generated.
- [ ] Vector database collection/index is created.
- [ ] Query retrieval returns top-k chunks.
- [ ] Scores are displayed or logged.
- [ ] Answers include retrieved evidence.
- [ ] Citations are included.

---

## GraphRAG

- [ ] Entities are extracted.
- [ ] Relationships are extracted.
- [ ] Neo4j connection works.
- [ ] Nodes are created.
- [ ] Relationships are created.
- [ ] Graph schema is documented.
- [ ] Cypher queries return relevant paths.
- [ ] Multi-hop questions work.

---

## Hybrid RAG

- [ ] Router classifies queries as vector, graph, or hybrid.
- [ ] Vector context and graph context are both available.
- [ ] Context fusion removes duplicates.
- [ ] Hybrid answers cite sources.
- [ ] Routing decisions are logged.

---

## Evaluation

- [ ] Benchmark contains at least 20 questions.
- [ ] Questions cover semantic, comparison, relationship, multi-hop, and unknown categories.
- [ ] Vector, graph, and hybrid systems are compared.
- [ ] Correctness is scored.
- [ ] Faithfulness is scored.
- [ ] Latency is measured.
- [ ] Results are summarized in a table.

---

## Demo readiness

- [ ] Demo can run from a clean environment.
- [ ] Architecture diagram is ready.
- [ ] Evaluation report is ready.
- [ ] Known limitations are documented.
- [ ] Final presentation answers trade-off questions.
