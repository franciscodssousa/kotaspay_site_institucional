"""
Views das páginas institucionais.

Todas herdam de TemplateView porque o conteúdo destas páginas é estático
(vem do briefing de marca), sem necessidade de acesso a regras financeiras complexas.
A página inicial disponibiliza o formulário de captação de leads comerciais.
"""

from django.views.generic import TemplateView
from apps.captacao_leads.forms import FormularioDeContatoComercial


class PaginaInicialView(TemplateView):
    template_name = "nucleo/inicio.html"

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto["form"] = FormularioDeContatoComercial()
        return contexto


class PaginaDaSolucaoView(TemplateView):
    template_name = "nucleo/solucao.html"


class PaginaDoPublicoAlvoView(TemplateView):
    """
    Página reaproveitada para 'Para Associações' e 'Para Cooperativas'.

    Em vez de duas views quase idênticas (violando DRY), uma única view
    recebe o segmento de público como parâmetro fixo na URL
    (ver apps/nucleo/urls.py) e ajusta apenas o contexto.
    """

    template_name = "nucleo/publico_alvo.html"
    segmento_do_publico = None

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto["segmento_do_publico"] = self.segmento_do_publico
        return contexto


class PaginaComoFuncionaView(TemplateView):
    template_name = "nucleo/como_funciona.html"


class PaginaSobreAKotasPayView(TemplateView):
    template_name = "nucleo/sobre.html"


class PaginaDaPoliticaDePrivacidadeView(TemplateView):
    template_name = "nucleo/politica_de_privacidade.html"


class PaginaDosTermosDeUsoView(TemplateView):
    template_name = "nucleo/termos_de_uso.html"


class PaginaDeProtecaoDeDadosView(TemplateView):
    template_name = "nucleo/protecao_de_dados.html"
