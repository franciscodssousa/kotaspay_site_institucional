from django.apps import AppConfig


class CaptacaoLeadsConfig(AppConfig):
    """App responsável por capturar e processar contatos comerciais vindos do site.

    Este é, propositalmente, o app com a fronteira mais bem definida do
    projeto: é aqui que mora o ponto de conexão com a futura Plataforma de
    Associações e Cooperativas (ver services/interfaces.py e ARQUITETURA.md).
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.captacao_leads"
    verbose_name = "Captação de leads"
