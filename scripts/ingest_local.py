from __future__ import annotations

import argparse
import os
from pathlib import Path

import httpx


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Ingest local docs into /v1/ingest")
    parser.add_argument("paths", nargs="+", help="File paths to ingest")
    parser.add_argument("--module", default=None, help="Optional module metadata")
    parser.add_argument("--url", default=os.getenv("INGEST_URL", "http://localhost:8000/v1/ingest"))
    parser.add_argument("--api-key", default=os.getenv("API_KEY", "change-me"))
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    files = []
    for raw_path in args.paths:
        path = Path(raw_path)
        if not path.exists() or not path.is_file():
            print(f"[ERROR] File not found: {path}")
            return 1
        files.append(("files", (path.name, path.read_bytes(), "application/octet-stream")))

    data = {}
    if args.module:
        data["module"] = args.module

    headers = {"X-API-Key": args.api_key}
    with httpx.Client(timeout=30) as client:
        response = client.post(args.url, files=files, data=data, headers=headers)

    if response.status_code >= 400:
        print(f"[ERROR] Ingest failed: {response.status_code} {response.text}")
        return 1

    print(response.text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
