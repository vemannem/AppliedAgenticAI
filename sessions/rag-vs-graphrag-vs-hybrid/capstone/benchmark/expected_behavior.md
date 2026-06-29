# Expected Benchmark Behavior

The benchmark questions are designed to test different retrieval strategies.

## Definition questions

Expected to work well with vector RAG because they require semantically relevant passages.

## Relationship questions

Expected to work well with GraphRAG because they require entities and relationships.

## Multi-hop questions

Expected to work best with hybrid retrieval because they require both explanatory passages and graph paths.

## Unknown questions

Expected behavior is to refuse unsupported claims. A good answer says the available corpus does not contain enough evidence.

---

## How to manually score

For each answer, assign scores from 0 to 3:

- Correctness
- Faithfulness
- Citation quality
- Retrieval relevance

Then compare average scores across vector-only, graph-only, and hybrid systems.
