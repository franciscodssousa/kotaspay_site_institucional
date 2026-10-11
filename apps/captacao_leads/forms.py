from django import forms

from apps.captacao_leads.models import ContatoComercial


class FormularioDeContatoComercial(forms.ModelForm):
    aceite_da_politica = forms.BooleanField(
        label="Li e concordo com a Política de Privacidade",
        required=True,
        error_messages={
            "required": "Para enviar, é preciso aceitar a Política de Privacidade.",
        },
    )

    class Meta:
        model = ContatoComercial
        fields = [
            "nome_completo",
            "email",
            "whatsapp",
            "nome_da_organizacao",
            "tipo_de_organizacao",
            "faixa_de_associados",
            "objetivo_do_contato",
            "mensagem",
        ]
        widgets = {
            "mensagem": forms.Textarea(attrs={"rows": 4}),
        }
