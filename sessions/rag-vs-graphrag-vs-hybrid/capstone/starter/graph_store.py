"""Neo4j graph store utilities for GraphRAG.

This file provides a minimal schema and graph retrieval functions. Learners
should improve extraction quality, canonicalization, and relationship design.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from neo4j import GraphDatabase
from openai import OpenAI
from tqdm import tqdm

from config import settings, require_openai_key

client = OpenAI()

EXTRACTION_SYSTEM = "You extract knowledge graph facts. Return only valid JSON."
EXTRACTION_PROMPT = """
Extract important entities and relationships from the text.

Return JSON only in this schema:
{
  "triples": [
    {"source": "...", "source_type": "Paper|Author|Method|Dataset|Model|Concept|Organization|Other", "relation": "...", "target": "...", "target_type": "Paper|Author|Method|Dataset|Model|Concept|Organization|Other"}
  ]
}

Rules:
- Use canonical names.
- Keep relation names short and uppercase, such as PROPOSES, USES, EVALUATED_ON, IMPROVES_OVER, RELATED_TO.
- Extract only facts supported by the text.

Text:
{text}
"""


def get_driver():
    if not settings.neo4j_uri or not settings.neo4j_password:
        raise RuntimeError("Neo4j settings are missing. Set NEO4J_URI, NEO4J_USERNAME, and NEO4J_PASSWORD.")
    return GraphDatabase.driver(settings.neo4j_uri, auth=(settings.neo4j_username, settings.neo4j_password))


def run_cypher(query: str, parameters: dict | None = None) -> list[dict]:
    with get_driver() as driver:
        with driver.session(database=settings.neo4j_database) as session:
            result = session.run(query, parameters or {})
            return [dict(record) for record in result]


def create_constraints() -> None:
    queries = [
        "CREATE CONSTRAINT entity_name IF NOT EXISTS FOR (e:Entity) REQUIRE e.name IS UNIQUE",
        "CREATE INDEX entity_type IF NOT EXISTS FOR (e:Entity) ON (e.type)",
    ]
    for q in queries:
        run_cypher(q)


def extract_triples(text: str) -> list[dict[str, Any]]:
    require_openai_key()
    response = client.chat.completions.create(
        model=settings.chat_model,
        temperature=0,
        messages=[
            {"role": "system", "content": EXTRACTION_SYSTEM},
            {"role": "user", "content": EXTRACTION_PROMPT.format(text=text[:6000])},
        ],
    )
    raw = response.choices[0].message.content.strip()
    raw = raw.removeprefix("```json").removeprefix("```").removesuffix("```").strip()
    try:
        return json.loads(raw).get("triples", [])
    except json.JSONDecodeError:
        return []


def upsert_triple(triple: dict, source_metadata: dict) -> None:
    relation = triple.get("relation", "RELATED_TO").upper().replace(" ", "_")
    if not relation.isidentifier():
        relation = "RELATED_TO"

    query = f"""
    MERGE (s:Entity {{name: $source}})
    SET s.type = coalesce(s.type, $source_type)
    MERGE (t:Entity {{name: $target}})
    SET t.type = coalesce(t.type, $target_type)
    MERGE (s)-[r:{relation}]->(t)
    SET r.source_doc = $source_doc,
        r.source_url = $source_url,
        r.page = $page
    """
    run_cypher(
        query,
        {
            "source": triple.get("source", "").strip(),
            "source_type": triple.get("source_type", "Other"),
            "target": triple.get("target", "").strip(),
            "target_type": triple.get("target_type", "Other"),
            "source_doc": source_metadata.get("title"),
            "source_url": source_metadata.get("source_url"),
            "page": source_metadata.get("page"),
        },
    )


def build_graph(chunks_path: str | Path = "processed/chunks.jsonl", limit: int | None = 50) -> None:
    create_constraints()
    records = []
    with Path(chunks_path).open("r", encoding="utf-8") as f:
        for line in f:
            records.append(json.loads(line))
    if limit:
        records = records[:limit]

    for record in tqdm(records, desc="Extracting graph facts"):
        triples = extract_triples(record["text"])
        for tr in triples:
            if tr.get("source") and tr.get("target"):
                upsert_triple(tr, record["metadata"])


def graph_retrieve(query: str, limit: int = 20) -> list[dict]:
    """Simple graph retriever.

    TODO: replace with better entity linking and path search.
    """
    terms = [t.lower() for t in query.split() if len(t) > 3]
    cypher = """
    MATCH (s:Entity)-[r]->(t:Entity)
    WHERE any(term IN $terms WHERE toLower(s.name) CONTAINS term OR toLower(t.name) CONTAINS term)
    RETURN s.name AS source, type(r) AS relation, t.name AS target,
           r.source_doc AS source_doc, r.page AS page
    LIMIT $limit
    """
    return run_cypher(cypher, {"terms": terms, "limit": limit})


if __name__ == "__main__":
    build_graph(limit=20)
    print(graph_retrieve("How is GraphRAG related to retrieval?", limit=5))
