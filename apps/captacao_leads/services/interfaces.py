"""
Contratos (interfaces) do app de captação de leads.

Duas interfaces pequenas e separadas em vez de uma única genérica (ISP):
  - NotificadorDeNovoContato: avisar um HUMANO que um novo contato chegou.
  - IntegradorDeContatoComSistemaExterno: enviar o dado para OUTRO SISTEMA.

São responsabilidades diferentes. Uma implementação de e-mail não deveria
ser forçada a saber como sincronizar dado com uma API externa, e vice-versa.

Qualquer classe nova que implemente estes contratos pode substituir a atual
em uso sem que o restante do app precise mudar (LSP) — e novas formas de
notificar ou integrar são adicionadas criando uma nova classe, nunca
alterando estas interfaces ou o código que já depende delas (OCP).
"""

from abc import ABC, abstractmethod

from apps.captacao_leads.models import ContatoComercial


class NotificadorDeNovoContato(ABC):
    """Avisa alguém (e-mail, Slack, etc.) que um novo contato comercial chegou."""

    @abstractmethod
    def notificar(self, contato: ContatoComercial) -> None:
        ...


class IntegradorDeContatoComSistemaExterno(ABC):
    """Envia o contato comercial para um sistema externo (CRM, futura
    Plataforma de Associações e Cooperativas etc.)."""

    @abstractmethod
    def enviar(self, contato: ContatoComercial) -> None:
        ...
