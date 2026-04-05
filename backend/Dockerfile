# syntax=docker/dockerfile:1

FROM python:3.13-slim

# Create non-root user for security
RUN adduser --disabled-password --gecos '' appuser

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chown -R appuser:appuser /app

USER appuser

EXPOSE 8000