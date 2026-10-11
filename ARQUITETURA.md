# Arquitetura — Site Institucional KotasPay

Este documento explica **por que** o projeto foi estruturado assim, para quem for
mantê-lo ou criar o próximo projeto (a Plataforma de Associações e Cooperativas).

## 1. Escopo deste projeto

Este projeto Django cobre **somente o site institucional**: páginas de conteúdo
(`apps/nucleo`) e captação de leads comerciais (`apps/captacao_leads`). Ele
**não** contém autenticação de associados, contribuições, pagamentos ou ledger
financeiro — isso pertence à futura Plataforma de Associações e Cooperativas.

## 2. Por que dois projetos Django separados (e não um só)

- **Superfície de segurança diferente**: o site é público e de baixo risco; a
  plataforma financeira vai lidar com dados sensíveis de associados e
  pagamentos, exigindo rigor de segurança e LGPD bem maior.
- **Ciclos de vida diferentes**: o site muda por conteúdo/marketing; a
  plataforma muda por regra de negócio financeira. Deploys separados evitam
  que um ajuste de texto do site arrisque o sistema financeiro.
- **Bancos de dados separados**: o `ContatoComercial` (lead) não deveria
  morar na mesma base que o ledger financeiro dos associados.

## 3. Como a conexão entre os dois projetos está preparada

- **Subdomínio reservado**: o botão "Acessar plataforma" no cabeçalho
  (`templates/includes/cabecalho.html`) já existe hoje apontando
  provisoriamente para a página de contato. Quando a plataforma nascer em
  `app.kotaspay.com`, é só trocar esse link — nenhuma outra mudança estrutural
  é necessária.
- **Configuração por variável de ambiente**: `URL_BASE_PLATAFORMA_ASSOCIACOES`
  já existe em `config/settings/base.py` e no `.env.example`, vazia por
  enquanto. Nenhuma URL de outro sistema é ou será hardcoded no código.
- **Contrato de integração já definido, sem implementação prematura**: em
  `apps/captacao_leads/services/interfaces.py` existem duas interfaces:
  - `NotificadorDeNovoContato` — avisar um humano sobre um novo contato.
  - `IntegradorDeContatoComSistemaExterno` — enviar o contato para um sistema
    externo (CRM, ou futuramente a própria Plataforma de Associações).

  A classe `IntegradorComPlataformaDeAssociacoes`
  (`services/integrador_plataforma_associacoes.py`) já implementa essa
  segunda interface, mas propositalmente levanta `NotImplementedError` — o
  contrato existe, o código real de integração só é escrito quando a
  plataforma existir. Isso evita abstração prematura sem deixar de preparar
  o ponto de extensão.

## 4. Aplicação dos princípios SOLID (apenas onde importa)

Os princípios não foram aplicados no projeto inteiro — as páginas
institucionais em `apps/nucleo` são propositalmente simples (`TemplateView`
direto, sem camadas extras), porque não há variação nem extensão futura ali.
Onde importa é no ponto de conexão com a futura plataforma:

- **OCP (Aberto para extensão, fechado para modificação)**: `FormularioDeContatoView`
  depende de `NotificadorPorEmail`, que implementa `NotificadorDeNovoContato`.
  Se amanhã quisermos notificar também por Slack ou WhatsApp, basta criar uma
  nova classe implementando a interface — nenhuma linha da view precisa mudar.
- **LSP (Substituição de Liskov)**: qualquer classe que implemente
  `NotificadorDeNovoContato` ou `IntegradorDeContatoComSistemaExterno` pode
  substituir a implementação atual sem quebrar o comportamento esperado por
  quem a usa — é exatamente esse contrato que garante que
  `IntegradorComPlataformaDeAssociacoes` poderá, no futuro, substituir uma
  implementação de CRM (ou vice-versa) sem impacto em outro lugar do código.
- **ISP (Segregação de interface)**: `NotificadorDeNovoContato` e
  `IntegradorDeContatoComSistemaExterno` são duas interfaces pequenas e
  separadas, não uma única interface genérica de "serviço de contato". Uma
  implementação de e-mail não é forçada a saber sincronizar dado com sistema
  externo, e vice-versa.

## 5. Convenções seguidas

- **Nomenclatura em português** em tudo que é código próprio do projeto
  (apps, models, views, variáveis, métodos, templates) — mantendo em inglês
  apenas o que é convenção do Django/Python (`Meta`, `objects`, `CharField`,
  `save()`, nomes de settings, etc.), para não conflitar com o framework nem
  confundir quem já conhece Django.
- **Nomes extensos e claros** em vez de abreviações (`FormularioDeContatoComercial`,
  não `FormContato`), priorizando legibilidade sobre brevidade.
- **Responsabilidade única** por classe/módulo: `views.py` só orquestra
  requisição/resposta; `services/` concentra as regras de notificação e
  integração externa; `models.py` só descreve dados.
- **Estrutura de pastas padrão de mercado**: `config/` para configuração do
  projeto, `apps/` para apps próprios, `templates/` e `static/` globais na
  raiz, `requirements/` dividido por ambiente — facilmente reconhecível por
  qualquer desenvolvedor Django experiente.

## 6. O que fica para quando a Plataforma de Associações começar

1. Criar um novo projeto Django (ou serviço) para a plataforma, com seu
   próprio banco de dados.
2. Decidir o modelo de autenticação (SSO compartilhado via OAuth2, ou contas
   totalmente independentes) — decisão adiada de propósito, sem impacto no
   site institucional.
3. Implementar de fato `IntegradorComPlataformaDeAssociacoes`, apontando para
   a API da nova plataforma via `URL_BASE_PLATAFORMA_ASSOCIACOES`.
4. Atualizar o link "Acessar plataforma" no cabeçalho para o subdomínio real.
