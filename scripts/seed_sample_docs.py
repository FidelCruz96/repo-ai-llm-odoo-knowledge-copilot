from __future__ import annotations

import os
from pathlib import Path
from subprocess import run

MODULE_BY_FILENAME = {
    "odoo_inventory_basics.md": "inventory",
    "odoo_purchase_approvals.md": "purchase",
    "odoo_invoicing_flow.md": "account",
    "odoo_crm_pipeline.md": "crm",
    "odoo_user_admin.md": "security",
    "odoo_support_faq.md": "support",
}


def main() -> int:
    sample_dir = Path("data/sample_docs")
    if not sample_dir.exists():
        print("[ERROR] data/sample_docs no existe")
        return 1

    files = sorted(path for path in sample_dir.iterdir() if path.is_file())
    if not files:
        print("[ERROR] data/sample_docs no tiene archivos")
        return 1

    api_key = os.getenv("API_KEY", "change-me")
    for file_path in files:
        command = [
            ".venv/bin/python",
            "scripts/ingest_local.py",
            str(file_path),
            "--api-key",
            api_key,
        ]
        module = MODULE_BY_FILENAME.get(file_path.name)
        if module:
            command.extend(["--module", module])
            print(f"[INFO] Ingesting {file_path.name} with module={module}")
        else:
            print(f"[INFO] Ingesting {file_path.name} without explicit module")

        process = run(command, check=False)
        if process.returncode != 0:
            return process.returncode

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
