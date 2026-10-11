from django.conf import settings
from django.contrib import messages
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import FormView

from apps.captacao_leads.forms import FormularioDeContatoComercial
from apps.captacao_leads.services.notificador_por_email import NotificadorPorEmail


class FormularioDeContatoView(FormView):
    """Exibe e processa o formulário de contato comercial do site institucional."""

    template_name = "captacao_leads/contato.html"
    form_class = FormularioDeContatoComercial
    success_url = reverse_lazy("captacao_leads:contato")

    def form_valid(self, form):
        contato = form.save(commit=False)
        contato.aceitou_a_politica_em = timezone.now()

        if settings.HABILITAR_REGISTRO_BANCO:
            contato.save()

        if settings.HABILITAR_ENVIO_EMAIL:
            NotificadorPorEmail().notificar(contato)

        messages.success(
            self.request,
            "Recebemos seu contato! Nossa equipe vai falar com você em breve.",
        )
        return super().form_valid(form)

