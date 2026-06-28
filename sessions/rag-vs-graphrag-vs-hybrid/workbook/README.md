# RAG vs GraphRAG vs Hybrid RAG Workbook

This workbook contains Colab-ready notebooks for teaching three retrieval patterns using a real research-paper corpus.

## Corpus

The notebooks download and process public research papers at runtime:

1. **Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks** — the original RAG paper by Lewis et al.
2. **From Local to Global: A Graph RAG Approach to Query-Focused Summarization** — Microsoft Research's GraphRAG paper by Edge et al.

These papers are useful for teaching because they contain concepts, authors, methods, systems, datasets, citations, and comparison statements that work well for vector search, graph extraction, and hybrid retrieval.

## Notebooks

| Notebook | Focus | Storage |
|---|---|---|
| `01_Traditional_RAG_ChromaDB_Pinecone.ipynb` | Traditional RAG with chunking, embeddings, vector search, grounding, and optional Pinecone upload | ChromaDB local persistent vector DB; Pinecone optional hosted vector DB |
| `02_GraphRAG_Neo4j.ipynb` | Entity/relation extraction, triples, Neo4j graph loading, Cypher traversal, graph-grounded answering | Neo4j |
| `03_Hybrid_RAG_ChromaDB_Neo4j.ipynb` | Query routing, vector retrieval + graph traversal, context fusion, and side-by-side comparison | ChromaDB + Neo4j |

## Required keys / services

### OpenAI

All notebooks require an OpenAI API key:

```bash
OPENAI_API_KEY=sk-...
```

In Colab, add it through the Colab Secrets panel or paste it into the setup cell when prompted.

### Neo4j

The GraphRAG and Hybrid notebooks require a Neo4j database. The easiest setup is Neo4j Aura Free:

```bash
NEO4J_URI=neo4j+s://...
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=...
```

### Pinecone, optional

The Traditional RAG notebook includes an optional Pinecone section. ChromaDB works without Pinecone.

```bash
PINECONE_API_KEY=...
```

## Suggested teaching flow

1. Start with the original hands-on notebook in the parent folder.
2. Run `01_Traditional_RAG_ChromaDB_Pinecone.ipynb` to teach chunking, embeddings, vector DBs, and grounded generation.
3. Run `02_GraphRAG_Neo4j.ipynb` to teach entity extraction, triples, graph schema, and multi-hop traversal.
4. Run `03_Hybrid_RAG_ChromaDB_Neo4j.ipynb` to compare vector-only, graph-only, and hybrid retrieval on the same questions.

## GitHub placement

Place this folder at:

```text
sessions/rag-vs-graphrag-vs-hybrid/workbook/
```

## Commit example

```bash
git clone https://github.com/vemannem/AppliedAgenticAI.git
cd AppliedAgenticAI
mkdir -p sessions/rag-vs-graphrag-vs-hybrid/workbook
cp -R /path/to/workbook/* sessions/rag-vs-graphrag-vs-hybrid/workbook/
git checkout -b add-rag-graphrag-hybrid-workbook
git add sessions/rag-vs-graphrag-vs-hybrid/workbook
git commit -m "Add RAG GraphRAG hybrid workbook notebooks"
git push origin add-rag-graphrag-hybrid-workbook
```

Then open a pull request into `main`.
