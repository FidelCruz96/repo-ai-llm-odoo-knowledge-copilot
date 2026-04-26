#!/usr/bin/env bash
set -euo pipefail

if [[ -z "${SERVICE_URL:-}" ]]; then
  echo "[ERROR] Falta SERVICE_URL. Ejemplo: export SERVICE_URL=https://odoo-knowledge-copilot-p4rstgvtfa-uc.a.run.app"
  exit 1
fi

if [[ -z "${API_KEY:-}" ]]; then
  echo "[ERROR] Falta API_KEY. Cargala desde Secret Manager o exportala antes de ejecutar el demo."
  exit 1
fi

if ! command -v jq >/dev/null 2>&1; then
  echo "[ERROR] jq no esta instalado."
  exit 1
fi

required_files=(
  "data/sample_docs/odoo_inventory_basics.md"
  "data/sample_docs/odoo_purchase_approvals.md"
  "data/sample_docs/odoo_invoicing_flow.md"
)

for file in "${required_files[@]}"; do
  if [[ ! -f "$file" ]]; then
    echo "[ERROR] No existe archivo requerido: $file"
    exit 1
  fi
done

print_question() {
  echo "Pregunta: $1"
  echo "Respuesta:"
}

echo ""
echo "1) HEALTH CHECK - Cloud Run"
curl -s "$SERVICE_URL/v1/health" | jq

echo ""
echo "2) INGEST - Documento sample de inventario"
curl -s -X POST "$SERVICE_URL/v1/ingest" \
  -H "X-API-Key: $API_KEY" \
  -F "files=@data/sample_docs/odoo_inventory_basics.md" \
  -F "module=inventory" | jq

echo ""
echo "3) INGEST - Documento sample de compras"
curl -s -X POST "$SERVICE_URL/v1/ingest" \
  -H "X-API-Key: $API_KEY" \
  -F "files=@data/sample_docs/odoo_purchase_approvals.md" \
  -F "module=purchase" | jq

echo ""
echo "4) INGEST - Documento sample de facturacion"
curl -s -X POST "$SERVICE_URL/v1/ingest" \
  -H "X-API-Key: $API_KEY" \
  -F "files=@data/sample_docs/odoo_invoicing_flow.md" \
  -F "module=account" | jq

echo ""
echo "5) QUERY 1 - Inventario"
print_question "¿Qué es un picking en Odoo?"
curl -s -X POST "$SERVICE_URL/v1/query" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $API_KEY" \
  -d '{"query":"¿Qué es un picking en Odoo?","filters":{"module":"inventory"},"stream":false}' | jq

echo ""
echo "6) QUERY 2 - Compras"
print_question "¿Cómo se aprueba una orden de compra en Odoo?"
curl -s -X POST "$SERVICE_URL/v1/query" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $API_KEY" \
  -d '{"query":"¿Cómo se aprueba una orden de compra en Odoo?","filters":{"module":"purchase"},"stream":false}' | jq

echo ""
echo "7) QUERY 3 - Facturacion"
print_question "¿Qué estados tiene una factura de cliente en Odoo?"
curl -s -X POST "$SERVICE_URL/v1/query" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $API_KEY" \
  -d '{"query":"¿Qué estados tiene una factura de cliente en Odoo?","filters":{"module":"account"},"stream":false}' | jq

echo ""
echo "8) ERROR CONTROLADO - Sin API Key"
print_question "¿Qué es un picking en Odoo?"
curl -i -X POST "$SERVICE_URL/v1/query" \
  -H "Content-Type: application/json" \
  -d '{"query":"¿Qué es un picking en Odoo?","stream":false}'
