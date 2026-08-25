# Stufe 1: Vue-Frontend bauen.
# VITE_API_BASE_URL="" -> API-Aufrufe gehen same-origin an denselben Host;
# --base=/app/ entspricht dem Mount-Pfad der SPA in der FastAPI-App.
FROM node:22-alpine AS frontend
WORKDIR /build
COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci
COPY frontend/ ./
ENV VITE_API_BASE_URL=""
# Getrennte Aufrufe statt "npm run build": das run-p-Script reicht --base
# nicht zuverlässig an vite weiter.
RUN npm run type-check && npm run build-only -- --base=/app/

# Stufe 2: FastAPI-Laufzeit mit dem gebauten Frontend.
FROM python:3.14-slim
WORKDIR /srv
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY app ./app
COPY --from=frontend /build/dist ./frontend-dist
ENV FRONTEND_DIST=/srv/frontend-dist
EXPOSE 8080
# Cloud Run injiziert den Port über die Umgebungsvariable PORT.
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8080}"]
