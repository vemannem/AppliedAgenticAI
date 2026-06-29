"""Simple evaluation runner.

This script reads benchmark questions and runs the hybrid system. Learners should
extend it to compare vector-only, graph-only, and hybrid approaches.
"""

from __future__ import annotations

import json
import time
from pathlib import Path

from hybrid_router import answer_question

BENCHMARK_PATH = Path("../benchmark/sample_questions.jsonl")


def load_questions(path: Path = BENCHMARK_PATH) -> list[dict]:
    with path.open("r", encoding="utf-8") as f:
        return [json.loads(line) for line in f]


def evaluate() -> list[dict]:
    results = []
    for q in load_questions():
        start = time.perf_counter()
        try:
            output = answer_question(q["question"])
            error = None
        except Exception as exc:
            output = {"route": None, "answer": "", "vector_hits": [], "graph_hits": []}
            error = str(exc)
        latency = time.perf_counter() - start
        results.append(
            {
                "id": q["id"],
                "category": q["category"],
                "question": q["question"],
                "expected_route": q.get("expected_route"),
                "actual_route": output.get("route"),
                "answer": output.get("answer"),
                "latency_seconds": round(latency, 3),
                "error": error,
            }
        )
    return results


if __name__ == "__main__":
    results = evaluate()
    out = Path("evaluation_results.jsonl")
    with out.open("w", encoding="utf-8") as f:
        for row in results:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
    print(f"Wrote {len(results)} evaluation rows to {out}")
    for row in results[:3]:
        print(json.dumps(row, indent=2)[:1000])
