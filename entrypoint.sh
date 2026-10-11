#!/bin/sh
set -e

# Aguarda o banco de dados ficar disponível antes de prosseguir.
python - <<'PY'
import os
import socket
import time

host = os.environ.get("POSTGRES_HOST", "db")
port = int(os.environ.get("POSTGRES_PORT", "5432"))

tentativas = 30
while tentativas > 0:
    try:
        with socket.create_connection((host, port), timeout=2):
            print("Banco de dados disponível.")
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
