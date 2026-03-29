# syntax=docker/dockerfile:1

FROM python:3.13-slim

# Create non-root user for security
RUN adduser --disabled-password --gecos '' appuser

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chown -R appuser:appuser /app

USER appuser

EXPOSE 8000

CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]