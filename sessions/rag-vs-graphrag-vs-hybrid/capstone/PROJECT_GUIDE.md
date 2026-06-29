# Capstone Project Guide

This guide breaks the capstone into implementation milestones. Complete each milestone in order. Do not jump directly to the final application; a strong capstone is built from validated components.

---

## Milestone 1: Define the problem

### Objective

Choose a domain and define what the assistant should answer.

### Required decisions

Document your choices:

- What corpus are you using?
- Who is the user?
- What types of questions should the assistant answer?
- Which questions should vector RAG handle?
- Which questions should GraphRAG handle?
- Which questions need hybrid retrieval?

### Output

Create a short `design.md` with:

```text
Project name:
Target users:
Corpus:
Primary use cases:
Expected question types:
Success criteria:
```

---

## Milestone 2: Build the ingestion pipeline

### Objective

Convert raw documents into clean text chunks.

### Required features

- Download or load documents.
- Extract text from PDF, Markdown, or HTML.
- Add metadata: document name, source URL, page number if available.
- Chunk the text.
- Save processed chunks as JSONL.

### Validation

You should be able to print:

```text
Documents loaded: N
Chunks created: N
Average chunk length: X tokens/characters
Example chunk with metadata: {...}
```

### Design questions

Explain:

- Why did you choose this chunk size?
- Did you use overlap? Why or why not?
- What metadata is needed for citations?

---

## Milestone 3: Build Traditional RAG

### Objective

Store chunks in a vector database and answer semantic questions.

### Required features

- Generate embeddings for all chunks.
- Store embeddings in Chroma, Pinecone, Qdrant, Weaviate, or another vector DB.
- Retrieve top-k chunks for a query.
- Generate an answer using retrieved context.
- Return citations.

### Validation questions

Test with questions such as:

- What is Retrieval-Augmented Generation?
- What problem does GraphRAG address?
- What are the limitations of vector-only retrieval?

### Expected output

Each answer should include:

```text
Answer:
Sources:
- paper_name, page/chunk id
Retrieved chunks:
- score, title, snippet
```

---

## Milestone 4: Build the Knowledge Graph

### Objective

Extract entities and relationships from the corpus and store them in Neo4j.

### Required node types

At minimum, include:

- `Paper`
- `Author`
- `Method`
- `Dataset`
- `Model`
- `Concept`
- `Organization`

You may add more labels depending on the corpus.

### Required relationship types

Examples:

- `AUTHORED_BY`
- `PROPOSES`
- `USES`
- `EVALUATED_ON`
- `COMPARES_TO`
- `IMPROVES_OVER`
- `RELATED_TO`
- `CITES`

### Validation

Run Neo4j queries such as:

```cypher
MATCH (n) RETURN labels(n) AS labels, count(*) AS count ORDER BY count DESC;
```

```cypher
MATCH ()-[r]->() RETURN type(r) AS rel, count(*) AS count ORDER BY count DESC;
```

```cypher
MATCH p=(a)-[*1..3]-(b)
WHERE toLower(a.name) CONTAINS 'rag'
RETURN p LIMIT 10;
```

---

## Milestone 5: Build GraphRAG

### Objective

Use the graph to answer relationship and multi-hop questions.

### Required features

- Detect seed entities from the question.
- Retrieve related nodes and relationships from Neo4j.
- Convert graph paths into LLM-readable context.
- Ask the LLM to answer step by step.

### Validation questions

- Which methods are related to RAG?
- Which papers propose graph-based retrieval?
- How is GraphRAG connected to community detection?
- Which datasets are used to evaluate retrieval methods?

---

## Milestone 6: Build Hybrid RAG

### Objective

Combine vector retrieval and graph retrieval.

### Required features

- Query router with at least three labels: `vector`, `graph`, `hybrid`.
- Vector retriever.
- Graph retriever.
- Context fusion.
- Final answer generation.

### Suggested routing rules

Use vector retrieval when the question asks for definitions, summaries, or explanations.

Use graph retrieval when the question asks about relationships, authors, methods, dependencies, or paths.

Use hybrid retrieval when the question needs both background explanation and explicit relationships.

### Example router behavior

| Question | Expected route |
|---|---|
| What is RAG? | vector |
| Which paper introduced GraphRAG? | graph |
| Compare RAG and GraphRAG with evidence from the papers. | hybrid |

---

## Milestone 7: Evaluate the system

### Objective

Compare Traditional RAG, GraphRAG, and Hybrid RAG.

### Required metrics

- Answer correctness
- Faithfulness
- Citation quality
- Retrieval relevance
- Latency
- Cost estimate

### Required comparison

Create a table like:

| Question ID | Type | Vector RAG | GraphRAG | Hybrid RAG | Winner | Notes |
|---|---|---|---|---|---|---|

---

## Milestone 8: Final demo

### Required demo flow

1. Show architecture.
2. Show corpus and ingestion.
3. Show vector database results.
4. Show Neo4j graph.
5. Ask semantic question.
6. Ask relationship question.
7. Ask hybrid question.
8. Show evaluation results.
9. Explain trade-offs.

### Final reflection

Answer these questions in your report:

- Where did vector RAG work best?
- Where did GraphRAG work best?
- Where did hybrid retrieval help?
- What failed?
- What would you improve for production?
