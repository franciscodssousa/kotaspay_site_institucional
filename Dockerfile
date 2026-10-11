# syntax=docker/dockerfile:1
FROM python:3.12-alpine

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    DJANGO_SETTINGS_MODULE=config.settings.homologacao

WORKDIR /app

# Dependências de sistema:
#   - build-base + postgresql-dev: necessários para compilar psycopg2 no Alpine (musl)
#   - libpq: biblioteca runtime do PostgreSQL, mantida no container final
RUN apk add --no-cache --virtual .build-deps \
        build-base \
        postgresql-dev \
    && apk add --no-cache \
        libpq

COPY requirements/ ./requirements/

RUN pip install --no-cache-dir -r requirements/producao.txt \
    && apk del .build-deps

COPY . .

RUN chmod +x /app/entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["/app/entrypoint.sh"]
