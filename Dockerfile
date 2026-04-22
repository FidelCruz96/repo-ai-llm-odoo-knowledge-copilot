FROM python:3.12-slim AS builder

ENV VENV_PATH=/opt/venv
RUN python -m venv "${VENV_PATH}"
ENV PATH="${VENV_PATH}/bin:${PATH}"

WORKDIR /build
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt


FROM python:3.12-slim AS runtime

ENV VENV_PATH=/opt/venv \
    PATH="/opt/venv/bin:${PATH}" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app
COPY --from=builder /opt/venv /opt/venv
COPY app ./app
COPY requirements.txt ./requirements.txt

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/v1/health', timeout=3)"

CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
