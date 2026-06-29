"""Vector store utilities for Traditional RAG.

Default implementation uses ChromaDB. Learners may add Pinecone, Qdrant,
Weaviate, or another vector DB as an extension.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import chromadb
from openai import OpenAI
from tqdm import tqdm

from config import require_openai_key, settings


client = OpenAI()


def embed_texts(texts: list[str]) -> list[list[float]]:
    require_openai_key()
    response = client.embeddings.create(model=settings.embed_model, input=texts)
    return [item.embedding for item in response.data]


def get_chroma_collection():
    chroma = chromadb.PersistentClient(path=settings.chroma_dir)
    return chroma.get_or_create_collection(name=settings.chroma_collection)


def load_jsonl(path: str | Path) -> list[dict]:
    with Path(path).open("r", encoding="utf-8") as f:
        return [json.loads(line) for line in f]


def index_chunks(chunks_path: str | Path = "processed/chunks.jsonl", batch_size: int = 32) -> None:
    records = load_jsonl(chunks_path)
    collection = get_chroma_collection()

    for start in tqdm(range(0, len(records), batch_size), desc="Indexing chunks"):
        batch = records[start : start + batch_size]
        texts = [r["text"] for r in batch]
        embeddings = embed_texts(texts)
        collection.add(
            ids=[r["id"] for r in batch],
            documents=texts,
            metadatas=[r["metadata"] for r in batch],
            embeddings=embeddings,
        )

    print(f"Chroma collection now contains {collection.count()} chunks")


def retrieve(query: str, k: int = 5) -> list[dict[str, Any]]:
    collection = get_chroma_collection()
    query_embedding = embed_texts([query])[0]
    result = collection.query(query_embeddings=[query_embedding], n_results=k)

    hits = []
    for i in range(len(result["ids"][0])):
        hits.append(
            {
                "id": result["ids"][0][i],
                "text": result["documents"][0][i],
                "metadata": result["metadatas"][0][i],
                "distance": result["distances"][0][i] if result.get("distances") else None,
            }
        )
    return hits


if __name__ == "__main__":
    index_chunks()
    for hit in retrieve("What is retrieval augmented generation?", k=3):
        print("-", hit["metadata"], hit["text"][:200].replace("\n", " "))
