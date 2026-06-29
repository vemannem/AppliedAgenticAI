# Capstone FAQ

## Do I need to use both Chroma and Pinecone?

No. Use at least one vector database. Chroma is easiest for local development. Pinecone is useful if you want a managed cloud vector database.

## Do I need to use Neo4j?

Yes. This capstone requires Neo4j or Neo4j Aura for the graph database component.

## Can I use LangChain or LlamaIndex?

Yes, but you should still be able to explain what each step does. Do not hide the architecture behind a framework.

## Can I use only notebooks?

Yes. A notebook-only submission is acceptable if it is reproducible and clearly documented. A Streamlit or FastAPI app is a bonus.

## What if entity extraction is noisy?

That is expected. You should document your cleaning strategy. Common improvements include:

- canonicalizing names
- filtering generic entities
- enforcing allowed relationship types
- merging duplicates
- validating triples with an LLM

## What if GraphRAG performs worse than vector RAG?

That can happen. Your job is to explain why. GraphRAG usually performs best on relationship and multi-hop questions, not broad semantic summaries.

## Do answers need citations?

Yes. Every final answer should include document names, chunk IDs, page numbers, or graph source metadata.

## Can I use internal company documents?

Only if you have permission and you do not upload sensitive data to public repositories. For public submissions, use public datasets.

## What should I show in the final demo?

Show one question where vector RAG works best, one where GraphRAG works best, one where hybrid retrieval works best, and one failure case.
