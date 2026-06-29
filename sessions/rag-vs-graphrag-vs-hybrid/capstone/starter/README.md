# Capstone Starter Code

This folder provides a lightweight scaffold. It is intentionally incomplete. Learners should fill in the TODO sections as part of the capstone.

## Files

| File | Purpose |
|---|---|
| `config.py` | Loads environment variables and configuration |
| `ingest.py` | Downloads/loads documents and creates chunks |
| `vector_store.py` | Chroma/Pinecone vector storage and retrieval |
| `graph_store.py` | Neo4j schema, node creation, relationship creation, graph retrieval |
| `hybrid_router.py` | Query routing and context fusion |
| `evaluator.py` | Benchmark evaluation utilities |
| `app.py` | Minimal Streamlit demo app |
| `.env.example` | Example environment file |
| `requirements.txt` | Python dependencies |

## Quick start

```bash
cp .env.example .env
pip install -r requirements.txt
python ingest.py
python evaluator.py
streamlit run app.py
```

You must implement the TODO sections before the system is complete.
