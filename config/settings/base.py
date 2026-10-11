"""
Configurações comuns a todos os ambientes do site institucional da KotasPay.

Este projeto cobre, por enquanto, SOMENTE o site institucional. A futura
Plataforma de Associações e Cooperativas (contribuições, pagamentos, ledger
financeiro) será um projeto Django separado, conectado a este por:
  - subdomínio próprio (app.kotaspay.com), reservado no link do cabeçalho;
  - variáveis de ambiente (ex: URL_BASE_PLATAFORMA_ASSOCIACOES), nunca hardcoded;
  - um contrato de integração já preparado em
    apps/captacao_leads/services/interfaces.py.
Ver ARQUITETURA.md na raiz do projeto para o detalhamento dessa decisão.
"""

from pathlib import Path

import environ

BASE_DIR = Path(__file__).resolve().parent.parent.parent

env = environ.Env(DEBUG=(bool, False))

# Em ambientes containerizados (Railway, Render, etc.) o arquivo .env não é
# copiado para a imagem (.dockerignore); as variáveis vêm do ambiente do
# provedor. Portanto, só tentamos ler .env se ele existir.
_env_file = BASE_DIR / ".env"
if _env_file.exists():
    environ.Env.read_env(_env_file)

SECRET_KEY = env("SECRET_KEY")
DEBUG = env("DEBUG")
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=[])

# Origens confiáveis para requisições com proteção CSRF (ex: login do /admin).
# Obrigatório em ambientes atrás de proxy reverso (Railway, Render, etc.).
# Defina no ambiente: CSRF_TRUSTED_ORIGINS=https://seu-app.up.railway.app
# Múltiplas origens podem ser separadas por vírgula.
CSRF_TRUSTED_ORIGINS = env.list("CSRF_TRUSTED_ORIGINS", default=[])

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sitemaps",
    # apps próprios do site institucional da KotasPay
    "apps.nucleo",
    "apps.captacao_leads",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "apps.nucleo.contexto.dados_da_empresa",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

def _montar_url_banco() -> str:
    """
    Resolve a URL de conexão com o banco de dados.

    Ordem de precedência:
      1. DATABASE_URL — URL completa (ex: postgres://user:senha@host:5432/db).
         Preferida em provedores de hospedagem (Railway, Render, etc.).
      2. Variáveis individuais POSTGRES_HOST, POSTGRES_PORT, POSTGRES_DB,
         POSTGRES_USER, POSTGRES_PASSWORD — usadas quando o banco roda em
         outro container/host (ex: Portainer, serviço gerenciado).
      3. SQLite local — fallback para desenvolvimento rápido.
    """
    database_url = env("DATABASE_URL", default=None)
    if database_url:
        return database_url

    postgres_host = env("POSTGRES_HOST", default=None)
    if postgres_host:
        usuario = env("POSTGRES_USER", default="postgres")
        senha = env("POSTGRES_PASSWORD", default="")
        porta = env.int("POSTGRES_PORT", default=5432)
        banco = env("POSTGRES_DB", default="postgres")
        return f"postgres://{usuario}:{senha}@{postgres_host}:{porta}/{banco}"

    return f"sqlite:///{BASE_DIR / 'db.sqlite3'}"


DATABASES = {
    "default": env.db("DATABASE_URL", default=_montar_url_banco()),
}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "pt-br"
TIME_ZONE = "America/Fortaleza"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# --- Configurações do domínio: e-mails do formulário de contato comercial ---
EMAIL_REMETENTE_PADRAO = env("EMAIL_REMETENTE_PADRAO", default="contato@kotaspay.com")
EMAIL_COMERCIAL_KOTASPAY = env("EMAIL_COMERCIAL_KOTASPAY", default="comercial@kotaspay.com")

# --- Flags de comportamento do formulário de contato comercial ---
# Permitem desabilitar, por ambiente, o envio do e-mail de notificação e/ou
# o registro do lead no banco de dados (útil em homologação/testes).
HABILITAR_ENVIO_EMAIL = env.bool("HABILITAR_ENVIO_EMAIL", default=True)
HABILITAR_REGISTRO_BANCO = env.bool("HABILITAR_REGISTRO_BANCO", default=True)

# --- Reservado para a futura Plataforma de Associações e Cooperativas ---
URL_BASE_PLATAFORMA_ASSOCIACOES = env("URL_BASE_PLATAFORMA_ASSOCIACOES", default="")
