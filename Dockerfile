# ============================================================
# Stage 1: Build frontend
# ============================================================
FROM node:20-alpine AS frontend-build

WORKDIR /app/frontend

COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci

COPY frontend/ ./
RUN npm run build

# ============================================================
# Stage 2: Build backend
# ============================================================
FROM python:3.13-slim AS backend-build

WORKDIR /app/backend

COPY backend/requirements.txt ./
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

COPY backend/ ./

# ============================================================
# Stage 3: Runtime (nginx + gunicorn)
# Uses Debian-based nginx to avoid musl/glibc ABI mismatch
# with Python packages compiled on python:3.13-slim
# ============================================================
FROM nginx:1.27

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 supervisor \
    && rm -rf /var/lib/apt/lists/*

# Copy Python packages from build stage
COPY --from=backend-build /install /usr/local

# Copy backend application
COPY --from=backend-build /app/backend /app/backend

# Copy built frontend
COPY --from=frontend-build /app/frontend/dist /usr/share/nginx/html

# Copy nginx config
COPY nginx/default.conf /etc/nginx/templates/default.conf.template

# Copy supervisord config
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

WORKDIR /app/backend

EXPOSE 8000

CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
