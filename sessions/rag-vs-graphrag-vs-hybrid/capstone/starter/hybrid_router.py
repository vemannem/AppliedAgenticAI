"""Hybrid router and answer generation.

The router decides whether a question should use vector retrieval, graph retrieval,
or both. Start with simple rules, then replace with an LLM-based classifier.
"""

from __future__ import annotations

from openai import OpenAI

from config import settings, require_openai_key
from vector_store import retrieve as vector_retrieve
from graph_store import graph_retrieve

client = OpenAI()


def route_query(query: str) -> str:
    q = query.lower()
    graph_keywords = ["connected", "relationship", "related", "author", "authored", "uses", "cites", "path", "between"]
    vector_keywords = ["what is", "define", "summarize", "explain", "overview"]

    if any(k in q for k in graph_keywords) and any(k in q for k in vector_keywords):
        return "hybrid"
    if any(k in q for k in graph_keywords):
        return "graph"
    if any(k in q for k in vector_keywords):
        return "vector"
    return "hybrid"


def format_vector_context(hits: list[dict]) -> str:
    blocks = []
    for h in hits:
        meta = h["metadata"]
        blocks.append(f"[VECTOR source={meta.get('title')} page={meta.get('page')} id={h['id']}]\n{h['text']}")
    return "\n\n".join(blocks)


def format_graph_context(facts: list[dict]) -> str:
    lines = []
    for f in facts:
        lines.append(
            f"[GRAPH source={f.get('source_doc')} page={f.get('page')}] "
            f"{f.get('source')} -[{f.get('relation')}]-> {f.get('target')}"
        )
    return "\n".join(lines)


def answer_question(query: str, k: int = 5) -> dict:
    require_openai_key()
    route = route_query(query)

    vector_hits = vector_retrieve(query, k=k) if route in {"vector", "hybrid"} else []
    graph_hits = graph_retrieve(query, limit=20) if route in {"graph", "hybrid"} else []

    context = ""
    if vector_hits:
        context += "\n# Vector context\n" + format_vector_context(vector_hits)
    if graph_hits:
        context += "\n# Graph context\n" + format_graph_context(graph_hits)
    if not context.strip():
        context = "No relevant context found."

    prompt = f"""
Answer the question using only the supplied context.
If the context is insufficient, say what is missing.
Include concise citations using the source/page markers.

Context:
{context}

Question: {query}
Answer:
"""

    response = client.chat.completions.create(
        model=settings.chat_model,
        temperature=0,
        messages=[{"role": "user", "content": prompt}],
    )
    return {
        "route": route,
        "answer": response.choices[0].message.content.strip(),
        "vector_hits": vector_hits,
        "graph_hits": graph_hits,
    }


if __name__ == "__main__":
    result = answer_question("Compare RAG and GraphRAG.")
    print("Route:", result["route"])
    print(result["answer"])
