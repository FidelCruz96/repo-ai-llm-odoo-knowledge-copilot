# Security

## Controles implementados
- API key obligatoria para `/v1/query` y `/v1/ingest`.
- Rate limiting básico por minuto.
- Validación de archivos (extensión y tamaño) en ingesta.
- Exclusión de secretos del repo mediante `.env` + `.gitignore`.

## Escaneo
- Script consolidado: `scripts/security_scan.py`.
- Salida esperada: `reports/security_scan.json`.
- Herramientas consideradas: `bandit`, `pip-audit`, `gitleaks`.
- Última ejecución: `bandit=ok`, `pip-audit=ok`, `gitleaks=ok`.

## Riesgos conocidos
- Rate limiting en memoria (no distribuido).
- No hay WAF ni políticas avanzadas de abuso.
- Falta rotación automática de API keys en esta fase.
