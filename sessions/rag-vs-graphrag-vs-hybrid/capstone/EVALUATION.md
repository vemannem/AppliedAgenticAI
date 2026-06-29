# Evaluation Guide

Evaluation is mandatory. A capstone without evaluation is a demo, not an engineering project.

---

## Why evaluate?

RAG systems can appear to work during demos but fail under systematic testing. Evaluation helps answer:

- Did retrieval find the right evidence?
- Did the LLM stay faithful to the evidence?
- Did hybrid retrieval actually improve quality?
- Which question types are weak?
- What is the latency/cost trade-off?

---

## Required evaluation dimensions

## 1. Retrieval relevance

Measure whether the retrieved context contains evidence needed to answer the question.

Simple scoring:

| Score | Meaning |
|---:|---|
| 0 | Retrieved context is irrelevant |
| 1 | Somewhat related but insufficient |
| 2 | Contains partial evidence |
| 3 | Contains complete evidence |

---

## 2. Answer correctness

Measure whether the final answer is correct.

| Score | Meaning |
|---:|---|
| 0 | Wrong |
| 1 | Partially correct |
| 2 | Mostly correct |
| 3 | Fully correct |

---

## 3. Faithfulness

Measure whether the answer is supported by retrieved context.

| Score | Meaning |
|---:|---|
| 0 | Unsupported or hallucinated |
| 1 | Some unsupported claims |
| 2 | Mostly supported |
| 3 | Fully supported |

---

## 4. Citation quality

Measure whether citations point to useful evidence.

| Score | Meaning |
|---:|---|
| 0 | No citations |
| 1 | Citations included but weak |
| 2 | Citations mostly useful |
| 3 | Citations precise and helpful |

---

## 5. Latency

Record latency for each pipeline:

- Vector retrieval time
- Graph retrieval time
- LLM generation time
- Total response time

---

## 6. Cost

Estimate cost using:

- Number of embedding tokens
- Number of prompt tokens
- Number of completion tokens
- Number of graph extraction calls

---

## Benchmark categories

Your benchmark should include at least 20 questions:

| Category | Minimum questions |
|---|---:|
| Definition / semantic | 5 |
| Comparison | 4 |
| Relationship | 4 |
| Multi-hop | 4 |
| Failure / unknown answer | 3 |

---

## Required comparison table

Create a table like this:

| ID | Question | Type | Vector score | Graph score | Hybrid score | Winner | Notes |
|---|---|---|---:|---:|---:|---|---|

---

## LLM-as-judge prompt template

Use this prompt to score answers consistently:

```text
You are evaluating a retrieval-augmented answer.

Question:
{question}

Retrieved context:
{context}

Answer:
{answer}

Score the answer from 0 to 3 for:
1. correctness
2. faithfulness
3. citation quality

Return JSON only:
{
  "correctness": 0-3,
  "faithfulness": 0-3,
  "citation_quality": 0-3,
  "explanation": "brief explanation"
}
```

---

## Pass criteria

A strong project should reach:

- Average correctness >= 2.3 / 3
- Average faithfulness >= 2.5 / 3
- At least 80% of answers include citations
- Hybrid beats or ties both baselines on multi-hop questions
- Unknown-answer questions should not hallucinate
