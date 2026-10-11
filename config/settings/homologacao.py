"""
Configurações do ambiente de homologação (HML) do site institucional da KotasPay.

Este ambiente é uma versão "dockerizada" da aplicação, usada para validar
comportamentos próximos de produção (DEBUG=False, SMTP real, segurança)
sem afetar o ambiente de produção.

Para rodar localmente via Docker Compose, defina:
    DJANGO_SETTINGS_MODULE=config.settings.homologacao

O envio de e-mail e o registro no banco podem ser desabilitados via
variáveis de ambiente (HABILITAR_ENVIO_EMAIL / HABILITAR_REGISTRO_BANCO),
ambas ativas por padrão.

As configurações de segurança/SSL (SECURE_SSL_REDIRECT, cookies seguros,
HSTS) são desativadas por padrão para permitir acesso local via HTTP.
Quando o HML for implantado atrás de um proxy reverso com SSL, ative-as
via variáveis de ambiente (ex: SECURE_SSL_REDIRECT=True).
"""

from config.settings.base import *  # noqa: F401,F403

DEBUG = False

SECURE_SSL_REDIRECT = env.bool("SECURE_SSL_REDIRECT", default=False)
SESSION_COOKIE_SECURE = env.bool("SESSION_COOKIE_SECURE", default=False)
CSRF_COOKIE_SECURE = env.bool("CSRF_COOKIE_SECURE", default=False)
SECURE_HSTS_SECONDS = env.int("SECURE_HSTS_SECONDS", default=0)
SECURE_HSTS_INCLUDE_SUBDOMAINS = env.bool("SECURE_HSTS_INCLUDE_SUBDOMAINS", default=False)

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = env("EMAIL_HOST")
EMAIL_PORT = env.int("EMAIL_PORT", default=587)
EMAIL_HOST_USER = env("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")
EMAIL_USE_TLS = True
