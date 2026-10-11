from django.conf import settings
from django.core.mail import send_mail

from apps.captacao_leads.models import ContatoComercial
from apps.captacao_leads.services.interfaces import NotificadorDeNovoContato


class NotificadorPorEmail(NotificadorDeNovoContato):
    """Envia um e-mail simples para a equipe comercial da KotasPay a cada novo contato."""

    def notificar(self, contato: ContatoComercial) -> None:
        assunto = f"Novo contato comercial: {contato.nome_da_organizacao}"
        corpo = (
            f"Nome: {contato.nome_completo}\n"
            f"E-mail: {contato.email}\n"
            f"WhatsApp: {contato.whatsapp}\n"
            f"Organização: {contato.nome_da_organizacao}\n"
            f"Tipo: {contato.get_tipo_de_organizacao_display()}\n"
            f"Faixa de associados: {contato.get_faixa_de_associados_display()}\n"
            f"Objetivo: {contato.get_objetivo_do_contato_display()}\n"
            f"Mensagem: {contato.mensagem}\n"
        )
        send_mail(
            assunto,
            corpo,
            settings.EMAIL_REMETENTE_PADRAO,
            [settings.EMAIL_COMERCIAL_KOTASPAY],
        )
