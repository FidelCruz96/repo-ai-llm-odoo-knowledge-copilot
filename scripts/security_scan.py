from __future__ import annotations

import json
import shutil
import subprocess
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def run_command(command: list[str]) -> tuple[int, str, str]:
    process = subprocess.run(command, capture_output=True, text=True)
    return process.returncode, process.stdout, process.stderr


def is_network_error(stderr: str) -> bool:
    markers = (
        "ConnectionError",
        "NameResolutionError",
        "Temporary failure in name resolution",
        "Failed to resolve",
        "Max retries exceeded",
    )
    return any(marker in stderr for marker in markers)


def scan_bandit() -> dict[str, Any]:
    if shutil.which("bandit") is None:
        return {"tool": "bandit", "status": "missing"}

    code, stdout, stderr = run_command(["bandit", "-r", "app", "-f", "json"])
    payload = {}
    if stdout.strip():
        try:
            payload = json.loads(stdout)
        except json.JSONDecodeError:
            payload = {"raw": stdout}
    return {"tool": "bandit", "status": "ok" if code == 0 else "issues", "exit_code": code, "result": payload, "stderr": stderr}


def scan_pip_audit() -> dict[str, Any]:
    if shutil.which("pip-audit") is None:
        return {"tool": "pip-audit", "status": "missing"}

    code, stdout, stderr = run_command(["pip-audit", "-f", "json"])
    payload = []
    if stdout.strip():
        try:
            payload = json.loads(stdout)
        except json.JSONDecodeError:
            payload = [{"raw": stdout}]
    status = "ok" if code == 0 else "issues"
    if code != 0 and is_network_error(stderr):
        status = "unavailable"
    return {"tool": "pip-audit", "status": status, "exit_code": code, "result": payload, "stderr": stderr}


def scan_gitleaks() -> dict[str, Any]:
    if shutil.which("gitleaks") is None:
        return {"tool": "gitleaks", "status": "missing"}

    with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as temp_file:
        report_path = Path(temp_file.name)
    code, stdout, stderr = run_command(
        [
            "gitleaks",
            "git",
            ".",
            "--no-banner",
            "--report-format",
            "json",
            "--report-path",
            str(report_path),
        ]
    )
    result: list[dict[str, Any]] = []
    if report_path.exists():
        try:
            result = json.loads(report_path.read_text(encoding="utf-8") or "[]")
        except json.JSONDecodeError:
            result = [{"raw": report_path.read_text(encoding="utf-8")}]
        report_path.unlink(missing_ok=True)

    return {"tool": "gitleaks", "status": "ok" if code == 0 else "issues", "exit_code": code, "result": result, "stdout": stdout, "stderr": stderr}


def main() -> int:
    reports_dir = Path("reports")
    reports_dir.mkdir(parents=True, exist_ok=True)
    output_path = reports_dir / "security_scan.json"

    checks = [scan_bandit(), scan_pip_audit(), scan_gitleaks()]
    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "checks": checks,
    }
    output_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"[OK] Security report written to {output_path}")

    if any(item.get("status") == "missing" for item in checks):
        return 1
    if any(item.get("status") == "issues" for item in checks):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
