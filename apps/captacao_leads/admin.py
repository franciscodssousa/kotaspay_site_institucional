from django.contrib import admin

from apps.captacao_leads.models import ContatoComercial


@admin.register(ContatoComercial)
class ContatoComercialAdmin(admin.ModelAdmin):
    list_display = ("nome_completo", "nome_da_organizacao", "objetivo_do_contato", "criado_em")
    list_filter = ("tipo_de_organizacao", "objetivo_do_contato", "faixa_de_associados")
    search_fields = ("nome_completo", "email", "nome_da_organizacao")
    readonly_fields = ("criado_em", "aceitou_a_politica_em")
