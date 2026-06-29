"""Document ingestion pipeline.

This starter file shows the expected structure. Learners should customize the
corpus list, metadata, chunking strategy, and persistence format.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Iterable

import requests
from pypdf import PdfReader
from tqdm import tqdm

DATA_DIR = Path("data")
PROCESSED_DIR = Path("processed")
DATA_DIR.mkdir(exist_ok=True)
PROCESSED_DIR.mkdir(exist_ok=True)

# Replace or expand this list with your chosen corpus.
CORPUS = [
    {
        "id": "rag_2020",
        "title": "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks",
        "url": "https://arxiv.org/pdf/2005.11401.pdf",
    },
    {
        "id": "graphrag_2024",
        "title": "From Local to Global: A GraphRAG Approach to Query-Focused Summarization",
        "url": "https://arxiv.org/pdf/2404.16130.pdf",
    },
]


def download_pdf(url: str, output_path: Path) -> Path:
    if output_path.exists():
        return output_path
    response = requests.get(url, timeout=60)
    response.raise_for_status()
    output_path.write_bytes(response.content)
    return output_path


def extract_pdf_pages(pdf_path: Path) -> list[dict]:
    reader = PdfReader(str(pdf_path))
    pages = []
    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        text = re.sub(r"\s+", " ", text).strip()
        if text:
            pages.append({"page": page_number, "text": text})
    return pages


def chunk_text(text: str, chunk_size: int = 1200, overlap: int = 200) -> list[str]:
    """Simple character-based chunker.

    For production, compare this with token-aware or semantic chunking.
    """
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        start = max(end - overlap, end) if overlap <= 0 else end - overlap
        if start >= len(text):
            break
    return chunks


def build_chunks() -> list[dict]:
    records = []
    for doc in tqdm(CORPUS, desc="Processing documents"):
        pdf_path = download_pdf(doc["url"], DATA_DIR / f"{doc['id']}.pdf")
        pages = extract_pdf_pages(pdf_path)
        for page in pages:
            for i, chunk in enumerate(chunk_text(page["text"]), start=1):
                records.append(
                    {
                        "id": f"{doc['id']}_p{page['page']}_c{i}",
                        "text": chunk,
                        "metadata": {
                            "doc_id": doc["id"],
                            "title": doc["title"],
                            "source_url": doc["url"],
                            "page": page["page"],
                            "chunk": i,
                        },
                    }
                )
    return records


def write_jsonl(records: Iterable[dict], path: Path) -> None:
    with path.open("w", encoding="utf-8") as f:
        for record in records:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    chunks = build_chunks()
    output = PROCESSED_DIR / "chunks.jsonl"
    write_jsonl(chunks, output)
    print(f"Wrote {len(chunks)} chunks to {output}")
    if chunks:
        print("Example chunk:")
        print(json.dumps(chunks[0], indent=2)[:1000])
