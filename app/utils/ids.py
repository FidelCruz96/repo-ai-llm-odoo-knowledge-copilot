import re
from pathlib import Path


def slugify_filename(filename: str) -> str:
    stem = Path(filename).stem.lower()
    slug = re.sub(r"[^a-z0-9]+", "-", stem).strip("-")
    return slug or "document"


def build_doc_id(filename: str) -> str:
    return slugify_filename(filename)
