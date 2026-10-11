# Contexto do Projeto — KotasPay

> **Para quem/o quê é este documento**: este arquivo foi escrito para dar a um
> assistente de IA (copiloto local) o contexto completo do projeto, tal como
> foi definido em conversa com outro assistente (Claude, Anthropic) durante o
> planejamento inicial. Ele resume a ideia de negócio, o que já foi pedido,
> o que já foi construído, e o que vem depois — para que o copiloto local
> continue o trabalho com o mesmo entendimento, sem precisar redescobrir
> decisões já tomadas.
>
> **Documento-fonte da ideia de negócio**: `BRIEFING_PARA_DESENVOLVIMENTO_DO_SITE.docx`,
> na raiz deste projeto. Este `.md` resume e organiza o que está lá, mas o
> `.docx` é a fonte original enviada pelo dono do projeto — sempre que houver
> dúvida ou detalhe fino de copy/conteúdo, o `.docx` é a referência final.

---

## 1. A ideia de negócio: o que é a KotasPay

A KotasPay é uma **fintech associativa**: uma plataforma digital de gestão de
recebíveis voltada para **associações e cooperativas** (associações de
moradores, associações profissionais, cooperativas em geral).

O problema que resolve, segundo o briefing:
- Controle de mensalidades e contribuições feito de forma manual ou dispersa
  em planilhas.
- Inadimplência difícil de acompanhar.
- Falta de previsibilidade de receita para o gestor da organização.
- Falta de transparência financeira para os associados/cooperados.
- Dificuldade de prestação de contas e geração de relatórios gerenciais.

O posicionamento da marca (frase-síntese usada no site): **"Gestão
financeira mais simples. Receitas mais previsíveis."** — e o diferencial
central destacado no briefing é que **a KotasPay vai além da cobrança**: não
é só um meio de pagamento, é uma plataforma de **inteligência financeira**
para organizações associativas (cobrar → controlar → prever → decidir).

Identidade de marca (retirada do briefing, usada no projeto):
- Cores: verde esmeralda/menta (`--kp-verde: #0FA968`), azul petróleo
  (`--kp-azul-petroleo: #0B3B5C`), cinza chumbo (`--kp-cinza-chumbo: #333B3F`).
- Tipografia: Inter / Plus Jakarta Sans.
- Missão, visão e valores: ver seção "Sobre" do briefing e a página
  `apps/nucleo/templates/nucleo/sobre.html`.

## 2. As duas fases do projeto (isso é a decisão mais importante)

O dono do projeto foi explícito: **por enquanto, só o site institucional**.
A parte de gestão financeira de fato (contribuições, pagamentos, ledger)
**vem depois**, possivelmente como um **projeto Django separado**, que pode
tanto se conectar a este quanto reaproveitar peças dele — mas a decisão
tomada em conjunto foi: **dois projetos Django separados**, conectados por
contrato (não um monólito único crescendo por dentro). O motivo completo
dessa decisão está documentado em `../ARQUITETURA.md`.

### Fase 1 — Site institucional (O QUE JÁ FOI CONSTRUÍDO)

Este repositório. Um projeto Django (padrão MVT) cobrindo:
- Páginas institucionais: Início, Solução, Para Associações, Para
  Cooperativas, Como Funciona, Sobre a KotasPay (app `apps/nucleo`).
- Captação de leads comerciais via formulário de contato (app
  `apps/captacao_leads`), com notificação por e-mail para a equipe
  comercial.
- Um **ponto de conexão já preparado, mas não implementado**, para a futura
  Plataforma de Associações (ver seção 4 abaixo e `../ARQUITETURA.md`).

### Fase 2 — Plataforma de gestão financeira de contribuições (FUTURO, AINDA NÃO CONSTRUÍDO)

Discutida em conversa, ainda não iniciada em código. O fluxo funcional real
da empresa, conforme desenhado, é:

```
Site institucional
      │
      ▼
Cadastro do cliente/organização (área logada, KYC)
      │
      ▼
Contribuições (plano, valor, recorrência dos associados/cooperados)
      │
      ▼
Pagamento (gateway — Pix, boleto, cartão) ──► Webhook de confirmação
      │
      ▼
Ledger financeiro (livro-razão: saldo, extrato, histórico — a fonte da
verdade financeira, cada lançamento é um registro imutável, não um saldo
sobrescrito)
      │
      ├──► Painel do cliente/associado (extrato, comprovantes)
      └──► Painel administrativo/gestor (relatórios, conciliação)
      │
      ▼
Notificações / API para integrações futuras (app mobile, parceiros, CRM)
```

Mapeamento sugerido de apps Django para essa fase 2 (para quando o novo
projeto for criado):

| Etapa do fluxo | App Django sugerido | O que o Model guarda |
|---|---|---|
| Cadastro | `clientes` | Organização, associado, dados KYC, status |
| Contribuições | `contribuicoes` | Plano, valor, recorrência |
| Pagamento | `pagamentos` | Transação, integração com gateway |
| Ledger | `financeiro` | Lançamento financeiro, saldo, extrato |
| Painéis | `dashboard` | Views que agregam dados dos apps acima |
| Integrações | `api` (Django REST Framework) | Serializers para app mobile/parceiros |

Pontos técnicos discutidos e que devem ser levados para a Fase 2:
- **Ledger como livro-razão**: modelar como uma sequência de lançamentos
  imutáveis (cada movimentação é um registro novo), nunca um único campo
  `saldo` sobrescrito — crítico para auditoria financeira.
- **Webhooks de pagamento tratados de forma assíncrona** (ex: Celery +
  Redis), para não bloquear a requisição do usuário na confirmação de Pix/
  boleto.
- **Django REST Framework** para expor API quando existir app mobile ou
  integração com parceiros.
- **Django Admin customizado** pode servir, no início da Fase 2, como
  ferramenta interna de conciliação/suporte antes de existir um painel
  administrativo próprio — economiza tempo de desenvolvimento.

## 3. Por que Django e por que o padrão MVT

Foi explicado ao dono do projeto, e vale reforçar aqui como contexto:
Django foi escolhido por ser "baterias inclusas" (ORM, autenticação, admin,
proteção CSRF/SQL injection, migrations prontos), o que permite montar a
base do site institucional já pronta para crescer sem reescrever tudo na
Fase 2.

O padrão **MVT (Model-View-Template)**, variação do Django para o MVC
clássico:
- **Model** — camada de dados (classe Python = tabela no banco, via ORM).
- **View** — lógica de negócio: recebe a requisição, processa dados via
  Models, decide a resposta (equivalente ao "Controller" do MVC).
- **Template** — camada de apresentação (HTML), recebe dados da View e
  renderiza.

Fluxo: `URL (urls.py) → View → Model (se precisar) → Template → Resposta HTML`.

## 4. A decisão de conexão entre Fase 1 e Fase 2

Resumo (detalhe completo em `../ARQUITETURA.md`):
- **Dois projetos Django separados**, não um monólito — por segurança (a
  plataforma financeira lida com dados sensíveis e teria superfície de
  ataque muito maior se estivesse junto do site público), por ciclo de vida
  diferente (o site muda por marketing, a plataforma por regra de negócio),
  e por banco de dados separado (lead comercial ≠ dado financeiro de
  associado).
- **Subdomínio reservado**: `kotaspay.com` para o site, `app.kotaspay.com`
  para a futura plataforma. O botão "Acessar plataforma" no cabeçalho do
  site já existe, apontando provisoriamente para a página de contato.
- **Variável de ambiente reservada**: `URL_BASE_PLATAFORMA_ASSOCIACOES` em
  `config/settings/base.py` e `.env.example`, vazia por enquanto.
- **Contrato de integração já definido, sem implementação prematura**: as
  interfaces `NotificadorDeNovoContato` e
  `IntegradorDeContatoComSistemaExterno`, em
  `apps/captacao_leads/services/interfaces.py`. A classe
  `IntegradorComPlataformaDeAssociacoes` já existe implementando a segunda
  interface, mas levanta `NotImplementedError` de propósito — o ponto de
  extensão existe, o código real só é escrito quando a Fase 2 começar.
- **Autenticação entre os dois projetos**: decisão explicitamente **adiada**.
  Quando a Fase 2 começar, será preciso decidir entre SSO compartilhado
  (mesma base de usuários, ou OAuth2 via `django-oauth-toolkit`) ou contas
  totalmente independentes. Essa escolha não trava nada da Fase 1 hoje.

## 5. Regras de código exigidas pelo dono do projeto (aplicadas na Fase 1, e que DEVEM continuar valendo na Fase 2)

Estas regras foram dadas explicitamente e devem ser seguidas por qualquer
copiloto de IA que continue este projeto. O detalhamento completo, com
exemplos de código, está em `DECISOES_E_CONVENCOES.md`. Resumo:

1. **Nomenclatura em português** em tudo que é código próprio do projeto
   (apps, models, views, variáveis, métodos) — com exceção de palavras-chave
   e convenções do Django/Python/bibliotecas (`Meta`, `objects`, `CharField`,
   `save()`, nomes de settings etc., que continuam em inglês).
2. **Clean code**: nomes claros mesmo que extensos, responsabilidade única
   por classe/módulo/função.
3. **SOLID aplicado de modo especial no ponto de conexão com a Fase 2**
   (o app `captacao_leads`, especialmente `services/`):
   - **OCP** (Aberto para extensão, fechado para modificação).
   - **LSP** (Substituição de Liskov).
   - **ISP** (Segregação de interface).
4. **Sem complexidade ou abstração desnecessária** nas partes que não
   precisam (ex: as páginas institucionais em `apps/nucleo` continuam
   simples, `TemplateView` puro, sem camadas de serviço).
5. **Convenções de pastas/arquivos do Django e do mercado**, para que
   qualquer desenvolvedor Django experiente reconheça a estrutura
   imediatamente (`config/`, `apps/`, `templates/`, `static/`,
   `requirements/` por ambiente).

## 6. Estado atual do projeto (o que já existe fisicamente no código)

- Projeto Django funcional (validado por `python manage.py check`,
  `makemigrations` e `migrate` — sintaxe também validada com `py_compile`,
  já que o ambiente de desenvolvimento usado na conversa não tinha acesso à
  rede para instalar o Django e rodar o servidor de fato).
- Apps `nucleo` (páginas institucionais) e `captacao_leads` (formulário de
  contato + ponto de conexão com a Fase 2).
- Templates com o design system inicial da marca (cores/tipografia como CSS
  variables em `static/css/variaveis.css`).
- Documentação: este arquivo, `../ARQUITETURA.md`,
  `DECISOES_E_CONVENCOES.md`, `ROADMAP_PLATAFORMA_FINANCEIRA.md`, e o
  briefing original em `.docx` na raiz.

## 7. O que ainda NÃO existe (para o copiloto local não presumir que existe)

- Qualquer código da Fase 2 (apps `clientes`, `contribuicoes`, `pagamentos`,
  `financeiro`, `dashboard`, `api`) — só existe como planejamento neste
  documento e em `ROADMAP_PLATAFORMA_FINANCEIRA.md`.
- Autenticação de usuários/associados.
- Qualquer integração real com gateway de pagamento.
- Deploy em produção (settings de produção existem em
  `config/settings/producao.py`, mas não foram testadas contra um servidor
  real).
- Teste automatizado do projeto rodando de fato (Django não pôde ser
  instalado no ambiente onde o projeto foi gerado, por falta de acesso à
  rede) — recomenda-se rodar `python manage.py check`, `makemigrations` e
  `migrate` localmente antes de seguir desenvolvendo.
