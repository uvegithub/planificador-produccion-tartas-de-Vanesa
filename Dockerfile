# Etapa 1: compilación del frontend Vue
FROM node:22-alpine AS frontend-build

WORKDIR /app/frontend

COPY frontend/package*.json ./
RUN npm ci

COPY frontend/ ./
RUN npm run build


# Etapa 2: aplicación FastAPI
FROM python:3.12-slim AS runtime

WORKDIR /app

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONPATH=/app/backend
ENV DATABASE_PATH=/data/app.db

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/app/ ./backend/app/
COPY --from=frontend-build /app/frontend/dist/ ./frontend/dist/

# Directorio persistente y usuario sin privilegios
RUN mkdir -p /data \
    && useradd --system --no-create-home appuser \
    && chown -R appuser:appuser /app /data

USER appuser

EXPOSE 8000

# Comprobación de salud
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health', timeout=3)"

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]