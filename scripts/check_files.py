from __future__ import annotations

from pathlib import Path

REQUIRED_PATHS = [
    "README.md",
    ".env.example",
    "Dockerfile",
    "docker-compose.yml",
    "Makefile",
    "REQUIRED_FILES.md",
    "docs/architecture/c4-contexto.png",
    "docs/architecture/c4-contenedores.png",
    "docs/architecture/secuencia-query.png",
    "docs/adr/ADR-001-llm-base.md",
    "docs/adr/ADR-002-vector-store.md",
    "docs/adr/ADR-003-rag-orchestration.md",
    "docs/api/openapi.yaml",
    "docs/final/AI_LLM_Project_Template_Filled.md",
    "reports/coverage.xml",
    "reports/ragas_report.json",
    "reports/security_scan.json",
    "notebooks/eval_dataset.json",
    "notebooks/evaluation.ipynb",
]

ALTERNATIVE_GROUPS = {
    "load test report": [
        "reports/load_test_report.json",
        "reports/load_test_report_10vus_local.json",
        "reports/load_test_report_50vus.json",
    ],
}


def collect_missing_paths(repo_root: Path) -> list[str]:
    missing: list[str] = []

    for relative_path in REQUIRED_PATHS:
        if not (repo_root / relative_path).exists():
            missing.append(relative_path)

    for label, candidates in ALTERNATIVE_GROUPS.items():
        if not any((repo_root / candidate).exists() for candidate in candidates):
            missing.append(f"{label}: one of {', '.join(candidates)}")

    return missing


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    missing = collect_missing_paths(repo_root)

    if missing:
        print("[ERROR] Faltan archivos requeridos:")
        for item in missing:
            print(f" - {item}")
        return 1

    print("[OK] Estructura requerida validada correctamente.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
