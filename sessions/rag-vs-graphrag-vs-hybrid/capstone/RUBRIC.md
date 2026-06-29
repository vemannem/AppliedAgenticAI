# Capstone Grading Rubric

Total: **100 points**

---

## 1. Problem Definition and Architecture — 10 points

| Criteria | Points |
|---|---:|
| Clear problem statement and target user | 2 |
| Well-defined corpus and use cases | 2 |
| Architecture diagram included | 2 |
| Correct separation of vector, graph, and hybrid components | 2 |
| Trade-offs explained | 2 |

---

## 2. Data Pipeline — 10 points

| Criteria | Points |
|---|---:|
| Documents can be loaded reproducibly | 2 |
| Text extraction works | 2 |
| Chunking strategy is reasonable | 2 |
| Metadata is preserved for citations | 2 |
| Processed data can be inspected/debugged | 2 |

---

## 3. Traditional RAG — 15 points

| Criteria | Points |
|---|---:|
| Embeddings generated correctly | 3 |
| Vector database index created | 3 |
| Top-k retrieval works | 3 |
| Answers are grounded in retrieved chunks | 3 |
| Citations or source references included | 3 |

---

## 4. GraphRAG — 20 points

| Criteria | Points |
|---|---:|
| Entities extracted clearly | 3 |
| Relationships extracted clearly | 3 |
| Neo4j graph schema is well designed | 4 |
| Cypher retrieval works | 3 |
| Multi-hop questions are supported | 3 |
| Graph facts are used in answer generation | 2 |
| Graph limitations are documented | 2 |

---

## 5. Hybrid Retrieval — 15 points

| Criteria | Points |
|---|---:|
| Query router implemented | 3 |
| Vector and graph contexts are combined | 4 |
| Hybrid answers improve over at least one baseline | 4 |
| Routing decisions are explainable | 2 |
| Failure cases are analyzed | 2 |

---

## 6. Evaluation — 15 points

| Criteria | Points |
|---|---:|
| Benchmark question set created | 3 |
| Vector vs graph vs hybrid comparison completed | 4 |
| Faithfulness/correctness measured | 3 |
| Latency and cost measured or estimated | 2 |
| Evaluation findings clearly summarized | 3 |

---

## 7. Engineering Quality — 5 points

| Criteria | Points |
|---|---:|
| Environment variables used for secrets | 1 |
| Code structure is clean | 1 |
| Setup instructions are reproducible | 1 |
| Error handling/logging included | 1 |
| No credentials committed | 1 |

---

## 8. Presentation and Documentation — 10 points

| Criteria | Points |
|---|---:|
| README is complete | 2 |
| Demo is clear | 2 |
| Slides or report explain the system | 2 |
| Results are easy to understand | 2 |
| Reflection and future work included | 2 |

---

## Bonus — up to 10 points

Optional bonus features:

- Streamlit or Gradio UI
- Docker Compose setup
- Neo4j graph visualization
- Automated evaluation script
- Agentic planner/retriever/verifier workflow
- Human feedback loop
- CI pipeline
- Observability with LangSmith, Phoenix, or OpenTelemetry
