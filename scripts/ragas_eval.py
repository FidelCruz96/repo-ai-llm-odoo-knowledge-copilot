from __future__ import annotations

import argparse
import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path
from statistics import mean
from typing import Any

import httpx


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run RAGAS-style evaluation against /v1/query")
    parser.add_argument(
        "--dataset",
        default=os.getenv("EVAL_DATASET_PATH", "data/eval_dataset.json"),
        help="Path to evaluation dataset json file",
    )
    parser.add_argument(
        "--output",
        default=os.getenv("RAGAS_REPORT_PATH", "reports/ragas_report.json"),
        help="Path where report json will be written",
    )
    parser.add_argument(
        "--url",
        default=os.getenv("QUERY_URL", "http://localhost:8000/v1/query"),
        help="Query endpoint URL",
    )
    parser.add_argument(
        "--api-key",
        default=os.getenv("API_KEY", "change-me"),
        help="API key for X-API-Key header",
    )
    parser.add_argument("--timeout", type=float, default=30.0, help="HTTP timeout in seconds")
    return parser.parse_args()


def tokenize(text: str) -> set[str]:
    return {
        token
        for token in re.findall(r"[a-zA-Z0-9_]+", text.lower())
        if len(token) > 2
    }


def score_keyword_recall(answer: str, expected_keywords: list[str]) -> float:
    if not expected_keywords:
        return 0.0
    answer_tokens = tokenize(answer)
    expected_tokens = {keyword.lower() for keyword in expected_keywords}
    hits = len(answer_tokens & expected_tokens)
    return hits / len(expected_tokens)


def score_jaccard(text_a: str, text_b: str) -> float:
    tokens_a = tokenize(text_a)
    tokens_b = tokenize(text_b)
    if not tokens_a or not tokens_b:
        return 0.0
    return len(tokens_a & tokens_b) / len(tokens_a | tokens_b)


def score_context_recall(returned_doc_ids: set[str], expected_doc_ids: list[str]) -> float:
    if not expected_doc_ids:
        return 1.0 if returned_doc_ids else 0.0
    expected = {doc_id.lower() for doc_id in expected_doc_ids}
    hits = len({doc_id.lower() for doc_id in returned_doc_ids} & expected)
    return hits / len(expected)


def score_context_precision(returned_doc_ids: set[str], expected_doc_ids: list[str]) -> float:
    if not returned_doc_ids:
        return 0.0
    expected = {doc_id.lower() for doc_id in expected_doc_ids}
    hits = len({doc_id.lower() for doc_id in returned_doc_ids} & expected)
    return hits / len(returned_doc_ids)


def evaluate_case(client: httpx.Client, url: str, api_key: str, case: dict[str, Any]) -> dict[str, Any]:
    payload = {
        "query": case["question"],
        "filters": case.get("filters"),
        "stream": False,
    }
    headers = {"X-API-Key": api_key}
    try:
        response = client.post(url, json=payload, headers=headers)
    except httpx.HTTPError as exc:
        return {
            "id": case.get("id"),
            "question": case["question"],
            "status_code": 0,
            "error": str(exc),
            "faithfulness": 0.0,
            "answer_relevancy": 0.0,
            "context_recall": 0.0,
            "context_precision": 0.0,
        }

    if response.status_code != 200:
        return {
            "id": case.get("id"),
            "question": case["question"],
            "status_code": response.status_code,
            "error": response.text,
            "faithfulness": 0.0,
            "answer_relevancy": 0.0,
            "context_recall": 0.0,
            "context_precision": 0.0,
        }

    data = response.json()
    answer = data.get("answer", "")
    sources = data.get("sources", [])
    returned_doc_ids = {source.get("doc_id", "") for source in sources if source.get("doc_id")}

    faithfulness = score_keyword_recall(answer, case.get("expected_answer_keywords", []))
    answer_relevancy = score_jaccard(case["question"], answer)
    context_recall = score_context_recall(returned_doc_ids, case.get("expected_doc_ids", []))
    context_precision = score_context_precision(returned_doc_ids, case.get("expected_doc_ids", []))

    return {
        "id": case.get("id"),
        "question": case["question"],
        "status_code": 200,
        "faithfulness": round(faithfulness, 4),
        "answer_relevancy": round(answer_relevancy, 4),
        "context_recall": round(context_recall, 4),
        "context_precision": round(context_precision, 4),
        "latency_ms": data.get("latency_ms"),
        "sources_count": len(sources),
    }


def aggregate_metric(cases: list[dict[str, Any]], key: str) -> float:
    values = [float(item.get(key, 0.0)) for item in cases]
    return round(mean(values), 4) if values else 0.0


def main() -> int:
    args = parse_args()
    dataset_path = Path(args.dataset)
    output_path = Path(args.output)

    if not dataset_path.exists():
        print(f"[ERROR] Dataset not found: {dataset_path}")
        return 1

    dataset = json.loads(dataset_path.read_text(encoding="utf-8"))
    if not isinstance(dataset, list) or not dataset:
        print("[ERROR] Dataset must be a non-empty JSON list")
        return 1

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with httpx.Client(timeout=args.timeout) as client:
        case_results = [evaluate_case(client, args.url, args.api_key, case) for case in dataset]

    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "dataset_path": str(dataset_path),
        "endpoint": args.url,
        "cases_total": len(case_results),
        "cases_failed": len([case for case in case_results if case.get("status_code") != 200]),
        "metrics": {
            "faithfulness": aggregate_metric(case_results, "faithfulness"),
            "answer_relevancy": aggregate_metric(case_results, "answer_relevancy"),
            "context_recall": aggregate_metric(case_results, "context_recall"),
            "context_precision": aggregate_metric(case_results, "context_precision"),
        },
        "notes": [
            "This report computes RAGAS-style proxy metrics from endpoint responses.",
            "For strict academic RAGAS, integrate official ragas package with judge LLM.",
        ],
        "cases": case_results,
    }
    output_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"[OK] Report written to {output_path}")

    return 0 if report["cases_failed"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
