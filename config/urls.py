"""
Roteamento raiz do projeto.

'contato/' é registrado ANTES do include do app `nucleo` de propósito: o app
`nucleo` contém apenas páginas institucionais de conteúdo estático, enquanto
a captação de leads é responsabilidade isolada do app `captacao_leads`
(ver apps/captacao_leads/urls.py e ARQUITETURA.md).
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("contato/", include("apps.captacao_leads.urls")),
    path("", include("apps.nucleo.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
