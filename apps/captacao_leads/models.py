from django.db import models


class TipoDeOrganizacao(models.TextChoices):
    ASSOCIACAO_DE_MORADORES = "associacao_de_moradores", "Associação de moradores"
    COOPERATIVA = "cooperativa", "Cooperativa"
    ASSOCIACAO_PROFISSIONAL = "associacao_profissional", "Associação profissional"
    OUTRA = "outra", "Outra"


class FaixaDeAssociados(models.TextChoices):
    ATE_100 = "ate_100", "Até 100"
    DE_101_A_500 = "de_101_a_500", "101–500"
    DE_501_A_1000 = "de_501_a_1000", "501–1.000"
    DE_1001_A_5000 = "de_1001_a_5000", "1.001–5.000"
    MAIS_DE_5000 = "mais_de_5000", "Mais de 5.000"


class ObjetivoDoContato(models.TextChoices):
    CONHECER_A_SOLUCAO = "conhecer_a_solucao", "Conhecer a solução"
    SOLICITAR_DEMONSTRACAO = "solicitar_demonstracao", "Solicitar demonstração"
    REDUZIR_INADIMPLENCIA = "reduzir_inadimplencia", "Reduzir inadimplência"
    MELHORAR_GESTAO_FINANCEIRA = "melhorar_gestao_financeira", "Melhorar gestão financeira"
    MELHORAR_TRANSPARENCIA = "melhorar_transparencia", "Melhorar transparência"
    OUTRO = "outro", "Outro"


class ContatoComercial(models.Model):
    """Registro de um contato comercial enviado pelo formulário do site institucional."""

    nome_completo = models.CharField("nome completo", max_length=200)
    email = models.EmailField("e-mail")
    whatsapp = models.CharField("WhatsApp", max_length=20)
    nome_da_organizacao = models.CharField("organização", max_length=200)
    tipo_de_organizacao = models.CharField(
        "tipo de organização", max_length=30, choices=TipoDeOrganizacao.choices
    )
    faixa_de_associados = models.CharField(
        "número aproximado de associados/cooperados",
        max_length=20,
        choices=FaixaDeAssociados.choices,
    )
    objetivo_do_contato = models.CharField(
        "objetivo do contato", max_length=30, choices=ObjetivoDoContato.choices
    )
    mensagem = models.TextField("mensagem", blank=True)
    aceitou_a_politica_em = models.DateTimeField(
        "aceitou a política de privacidade em", null=True, blank=True
    )
    criado_em = models.DateTimeField("criado em", auto_now_add=True)

    class Meta:
        verbose_name = "contato comercial"
        verbose_name_plural = "contatos comerciais"
        ordering = ["-criado_em"]

    def __str__(self) -> str:
        return f"{self.nome_completo} — {self.nome_da_organizacao}"
