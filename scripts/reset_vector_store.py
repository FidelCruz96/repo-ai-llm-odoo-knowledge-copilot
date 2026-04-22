from __future__ import annotations

import os

import psycopg
from dotenv import load_dotenv


def main() -> int:
    load_dotenv()
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        print("[ERROR] DATABASE_URL no está configurada")
        return 1

    conn_url = database_url.replace("postgresql+psycopg://", "postgresql://")
    with psycopg.connect(conn_url) as conn:
        with conn.cursor() as cur:
            cur.execute("TRUNCATE TABLE documents_chunks;")
        conn.commit()

    print("[OK] Tabla documents_chunks limpiada")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
