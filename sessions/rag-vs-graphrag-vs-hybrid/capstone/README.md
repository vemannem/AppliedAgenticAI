# Capstone Project: Enterprise Knowledge Intelligence Platform

This capstone is the final project for the **RAG vs GraphRAG vs Hybrid RAG** workbook. Learners build a production-style AI knowledge assistant that can answer semantic questions, relationship questions, and multi-hop reasoning questions from a real document corpus.

The goal is not only to make a chatbot. The goal is to design, build, evaluate, and present a complete retrieval system using both vector databases and graph databases.

---

## Scenario

You are part of an AI engineering team at an enterprise company. The organization has a large knowledge base containing research papers, documentation, architecture notes, and internal reports. Employees ask questions that are difficult to answer with keyword search alone.

Your team must build an assistant that can:

1. Retrieve relevant text passages using vector search.
2. Extract entities and relationships into a knowledge graph.
3. Answer relationship and multi-hop questions using graph traversal.
4. Combine vector and graph retrieval using a hybrid strategy.
5. Return cited, grounded answers.
6. Evaluate quality, latency, and cost.

---

## Recommended project theme

**Research Intelligence Assistant for RAG, GraphRAG, and Agentic AI papers**

Use public papers such as:

- Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks
- From Local to Global: A GraphRAG Approach to Query-Focused Summarization
- RAPTOR: Recursive Abstractive Processing for Tree-Organized Retrieval
- Self-RAG: Learning to Retrieve, Generate, and Critique
- Corrective Retrieval Augmented Generation
- ColBERT: Efficient and Effective Passage Search via Contextualized Late Interaction

Learners may also choose another domain, but the final system must support both vector retrieval and graph retrieval.

---

## What learners will build

A complete application or notebook-based system with this architecture:

```text
User Question
     |
     v
Query Router
     |
     +------------------+
     |                  |
     v                  v
Vector Retriever     Graph Retriever
Chroma/Pinecone      Neo4j
     |                  |
     +--------+---------+
              v
        Context Fusion
              |
              v
        LLM Answerer
              |
              v
   Cited Answer + Evaluation Logs
```

---

## Required components

The project must include:

- Document ingestion pipeline
- Chunking strategy
- Embedding generation
- Vector database storage
- Entity and relationship extraction
- Neo4j graph construction
- Graph traversal queries
- Hybrid retrieval strategy
- Answer generation with citations
- Evaluation benchmark
- README with setup instructions
- Final presentation or demo

---

## Suggested timeline

| Phase | Focus | Output |
|---|---|---|
| 1 | Problem definition | Scope, corpus, architecture |
| 2 | Data ingestion | Parsed documents and chunks |
| 3 | Traditional RAG | Vector index and vector answers |
| 4 | GraphRAG | Neo4j graph and graph answers |
| 5 | Hybrid RAG | Router and context fusion |
| 6 | Evaluation | Benchmark results and analysis |
| 7 | Demo | App/notebook, slides, final report |

---

## Final deliverables

Each team or learner submits:

1. GitHub repository or folder with source code.
2. `README.md` explaining setup and usage.
3. Architecture diagram.
4. Working demo notebook or application.
5. Evaluation report.
6. Benchmark question file.
7. Final presentation.
8. Optional demo video.

---

## Definition of done

A project is complete when:

- The corpus can be ingested from scratch.
- Vector search returns relevant chunks.
- Neo4j contains meaningful nodes and relationships.
- Hybrid retrieval works for at least 10 benchmark questions.
- Answers include citations or source references.
- Evaluation metrics are reported.
- Setup can be reproduced by another learner.
