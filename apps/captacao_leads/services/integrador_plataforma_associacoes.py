"""
Ponto de extensão RESERVADO para a futura integração com a Plataforma de
Associações e Cooperativas da KotasPay (projeto Django separado).

Quando esse projeto existir, esta classe passa a implementar de fato
`IntegradorDeContatoComSistemaExterno` — por exemplo, fazendo uma chamada
HTTP autenticada para a API da plataforma (URL vinda de
settings.URL_BASE_PLATAFORMA_ASSOCIACOES) e transformando o contato
comercial em um cadastro inicial de organização por lá.

Por enquanto, propositalmente, ela não faz nada além de existir como
contrato: não há necessidade de código de integração antes de existir com
o que integrar (evitar abstração prematura). O que importa hoje é que
qualquer view que precise dessa integração já dependa da interface
`IntegradorDeContatoComSistemaExterno`, não desta classe — trocar a
implementação no futuro não exige tocar em mais nada (OCP).
"""

from apps.captacao_leads.models import ContatoComercial
from apps.captacao_leads.services.interfaces import IntegradorDeContatoComSistemaExterno


class IntegradorComPlataformaDeAssociacoes(IntegradorDeContatoComSistemaExterno):
    def enviar(self, contato: ContatoComercial) -> None:
        raise NotImplementedError(
            "A Plataforma de Associações e Cooperativas ainda não existe. "
            "Implemente esta integração quando o projeto estiver disponível."
        )
