from django.urls import path

from apps.nucleo.views import (
    PaginaComoFuncionaView,
    PaginaDaPoliticaDePrivacidadeView,
    PaginaDaSolucaoView,
    PaginaDeProtecaoDeDadosView,
    PaginaDoPublicoAlvoView,
    PaginaDosTermosDeUsoView,
    PaginaInicialView,
    PaginaSobreAKotasPayView,
)

app_name = "nucleo"

urlpatterns = [
    path("", PaginaInicialView.as_view(), name="inicio"),
    path("solucao/", PaginaDaSolucaoView.as_view(), name="solucao"),
    path(
        "para-associacoes/",
        PaginaDoPublicoAlvoView.as_view(segmento_do_publico="associacao"),
        name="para_associacoes",
    ),
    path(
        "para-cooperativas/",
        PaginaDoPublicoAlvoView.as_view(segmento_do_publico="cooperativa"),
        name="para_cooperativas",
    ),
    path("como-funciona/", PaginaComoFuncionaView.as_view(), name="como_funciona"),
    path("sobre/", PaginaSobreAKotasPayView.as_view(), name="sobre"),
    path(
        "politica-de-privacidade/",
        PaginaDaPoliticaDePrivacidadeView.as_view(),
        name="politica_de_privacidade",
    ),
    path("termos-de-uso/", PaginaDosTermosDeUsoView.as_view(), name="termos_de_uso"),
    path("lgpd/", PaginaDeProtecaoDeDadosView.as_view(), name="lgpd"),
]
