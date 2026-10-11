# Roadmap técnico — Fase 2: Plataforma de Gestão Financeira de Contribuições

> **Status**: planejamento apenas. Nenhum código deste roadmap existe ainda
> neste repositório (que cobre só o site institucional). Este documento
> existe para que a Fase 2 comece com o mesmo entendimento arquitetural
> definido na Fase 1, sem precisar renegociar decisões já tomadas.

## 1. Objetivo da Fase 2

Um sistema completo de gestão financeira das contribuições dos clientes
(associados/cooperados) da KotasPay: da adesão de uma organização até o
extrato financeiro do associado, passando por cobrança recorrente,
confirmação de pagamento e relatórios gerenciais.

## 2. Decisão de projeto: novo projeto Django, separado deste

Ver `../ARQUITETURA.md` e `CONTEXTO_DO_PROJETO.md` para a justificativa
completa (segurança, ciclo de vida, banco de dados separados). Em resumo:
este repositório permanece só o site institucional; a Fase 2 nasce como um
**novo projeto Django**, em `app.kotaspay.com`.

## 3. Fluxo funcional real da empresa (o que o sistema precisa sustentar)

```
1. Cadastro do cliente/organização
   → área logada, dados de KYC, status da organização

2. Contribuições
   → plano de contribuição, valor, periodicidade/recorrência por
     associado/cooperado

3. Pagamento
   → integração com gateway (Pix, boleto, cartão)
   → confirmação via webhook assíncrono (não bloqueia a requisição do
     usuário — usar fila, ex: Celery + Redis)

4. Ledger financeiro
   → livro-razão: cada lançamento é um registro imutável
   → NUNCA um único campo "saldo" sobrescrito — saldo é sempre calculado
     a partir da soma dos lançamentos (crítico para auditoria)

5. Painéis
   → painel do cliente/associado: extrato e comprovantes
   → painel administrativo/gestor: relatórios e conciliação

6. Notificações / API para integrações futuras
   → app mobile, parceiros, outros sistemas
```

## 4. Apps Django sugeridos (nomenclatura em português, seguindo as
   convenções de `DECISOES_E_CONVENCOES.md`)

| App | Responsabilidade | Exemplos de Models |
|---|---|---|
| `clientes` | Organizações e seus associados/cooperados, KYC | `Organizacao`, `Associado` |
| `contribuicoes` | Planos e regras de contribuição | `PlanoDeContribuicao`, `Contribuicao` |
| `pagamentos` | Transações e integração com gateway | `Transacao`, `MetodoDePagamento` |
| `financeiro` | O ledger — fonte da verdade financeira | `LancamentoFinanceiro` |
| `dashboard` | Views que agregam dados dos apps acima | (sem models próprios, ou só de preferências de visualização) |
| `api` | Exposição via Django REST Framework | serializers sobre os models acima |

Cada app segue a mesma estrutura de pastas descrita em
`DECISOES_E_CONVENCOES.md` (seção 4), incluindo `services/` **apenas** nos
apps onde houver regra de negócio relevante (o candidato mais óbvio é
`pagamentos`, pela mesma razão que `captacao_leads` tem `services/` neste
projeto: é um ponto de integração externa com múltiplas implementações
possíveis — Pix, boleto, cartão — que se beneficia de uma interface comum).

## 5. Onde SOLID deve ser aplicado na Fase 2 (por analogia ao que já foi
   feito na Fase 1)

- **Gateway de pagamento**: candidato natural a uma interface
  `ProcessadorDePagamento` (ISP: talvez separada de
  `ConsultadorDeStatusDePagamento`, já que confirmar um pagamento e
  consultar seu status são responsabilidades diferentes), com uma
  implementação por meio de pagamento (Pix, boleto, cartão) — todas
  substituíveis entre si onde o contrato for respeitado (LSP), e novas
  formas de pagamento adicionadas sem alterar código existente (OCP).
- **Ledger financeiro**: getter de saldo deve ser uma função pura sobre os
  lançamentos, não um campo mutável — isso não é bem um princípio SOLID
  isolado, mas é a mesma filosofia de "abstração no lugar certo" aplicada
  ao domínio financeiro.
- **O que NÃO precisa de interface**: CRUD simples de `Organizacao` ou
  `Associado`, páginas de relatório que só leem dados — mesma lógica da
  Fase 1: abstração onde há variação real, simplicidade onde não há.

## 6. Conexão com o site institucional (este repositório)

- O botão "Acessar plataforma" no cabeçalho do site
  (`templates/includes/cabecalho.html` deste repositório) deve passar a
  apontar para `app.kotaspay.com` assim que a Fase 2 tiver uma URL real.
- `IntegradorComPlataformaDeAssociacoes`
  (`apps/captacao_leads/services/integrador_plataforma_associacoes.py`,
  neste repositório) deve deixar de levantar `NotImplementedError` e passar
  a fazer uma chamada HTTP real para a API da Fase 2, usando a variável de
  ambiente `URL_BASE_PLATAFORMA_ASSOCIACOES` (já existe em
  `config/settings/base.py` e `.env.example` deste repositório).
- Decisão de autenticação entre os dois projetos (SSO compartilhado via
  OAuth2, ou contas totalmente independentes) precisa ser tomada **no
  início** da Fase 2 — está deliberadamente em aberto até lá.

## 7. Coisas técnicas mencionadas na conversa de planejamento, a não
   esquecer

- `django-environ` para variáveis de ambiente desde o primeiro commit do
  novo projeto (mesmo padrão já usado neste repositório).
- Settings divididos por ambiente (`base.py`, `desenvolvimento.py`,
  `producao.py`), mesmo padrão deste repositório.
- Django Admin customizado pode servir como ferramenta interna de
  conciliação/suporte no início da Fase 2, antes de existir um painel
  administrativo dedicado — evita gastar tempo de desenvolvimento cedo
  demais numa interface própria.
- Segurança e LGPD são requisito de primeira classe nesta fase (dados
  financeiros e pessoais de associados), diferente do site institucional.
