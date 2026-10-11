#!/bin/sh
set -e

# Garante que DJANGO_SETTINGS_MODULE esteja definido para todos os comandos
# deste script (migrate, criação de superusuário, collectstatic e gunicorn).
# O valor padrão (homologacao) pode ser sobrescrito via variável de ambiente
# do provedor de hospedagem (ex: Railway, Render).
export DJANGO_SETTINGS_MODULE="${DJANGO_SETTINGS_MODULE:-config.settings.homologacao}"

# Aguarda o banco de dados ficar disponível antes de prosseguir.
# Funciona tanto com DATABASE_URL (provedores de hospedagem) quanto com
# variáveis individuais POSTGRES_HOST/POSTGRES_PORT. Se o banco for SQLite
# (DATABASE_URL iniciando com "sqlite"), a espera é pulada.
python - <<'PY'
import os
import socket
import time
from urllib.parse import urlparse

database_url = os.environ.get("DATABASE_URL", "")

if database_url.startswith("sqlite"):
    print("Banco de dados SQLite detectado — pulando espera de disponibilidade.")
else:
    host = os.environ.get("POSTGRES_HOST")
    port = os.environ.get("POSTGRES_PORT")

    # DATABASE_URL é a fonte da verdade quando definida: sobrescreve
    # POSTGRES_HOST/POSTGRES_PORT para evitar apontar para o container "db"
    # local quando o usuário configurou um banco externo.
    if database_url:
        parsed = urlparse(database_url)
        host = parsed.hostname
        port = parsed.port

    host = host or "db"
    port = int(port or 5432)

    tentativas = 30
    while tentativas > 0:
        try:
            with socket.create_connection((host, port), timeout=2):
                print(f"Banco de dados disponível em {host}:{port}.")
                break
        except OSError:
            tentativas -= 1
            print(f"Aguardando banco de dados em {host}:{port}... ({tentativas} tentativas restantes)")
            time.sleep(2)
    else:
        raise SystemExit("Banco de dados indisponível após múltiplas tentativas.")
PY

python manage.py migrate --noinput

# Cria o superusuário automaticamente se as variáveis estiverem definidas
# e o usuário ainda não existir (idempotente: não recria em reinicializações).
python - <<'PY'
import os

import django

django.setup()

from django.contrib.auth import get_user_model

username = os.environ.get("DJANGO_SUPERUSER_USERNAME")
email = os.environ.get("DJANGO_SUPERUSER_EMAIL", "")
password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")

if username and password:
    User = get_user_model()
    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(username=username, email=email, password=password)
        print(f"Superusuário '{username}' criado com sucesso.")
    else:
        print(f"Superusuário '{username}' já existe — nada a fazer.")
else:
    print("Variáveis DJANGO_SUPERUSER_* não definidas — pulando criação do superusuário.")
PY

python manage.py collectstatic --noinput

exec gunicorn config.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3 \
    --timeout 120 \
    --graceful-timeout 30
