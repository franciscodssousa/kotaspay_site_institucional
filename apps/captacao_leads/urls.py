from django.urls import path

from apps.captacao_leads.views import FormularioDeContatoView

app_name = "captacao_leads"

urlpatterns = [
    path("", FormularioDeContatoView.as_view(), name="contato"),
]
