# Site institucional — KotasPay

Projeto Django (padrão MVT) do site institucional da KotasPay. Cobre **só o
site institucional** — a gestão financeira de contribuições dos clientes é
uma fase futura, ainda não construída (ver `docs/ROADMAP_PLATAFORMA_FINANCEIRA.md`).

> ## 📌 Para um copiloto de IA local lendo este repositório
>
> Leia os documentos abaixo **nesta ordem** antes de sugerir ou escrever
> qualquer código. Eles registram o que foi decidido em planejamento e o
> porquê — evita retrabalho e decisões contraditórias com o que já existe.
>
> 1. **`BRIEFING_PARA_DESENVOLVIMENTO_DO_SITE.docx`** (nesta pasta) — a ideia
>    de negócio original, na íntegra, como enviada pelo dono do projeto.
>    Fonte primária de tudo: posicionamento de marca, público-alvo, copy do
>    site, identidade visual, requisitos funcionais do site institucional.
> 2. **`docs/CONTEXTO_DO_PROJETO.md`** — resumo de todo o planejamento: a
>    ideia de negócio, as duas fases do projeto (site institucional agora,
>    plataforma financeira depois), por que Django/MVT, e o estado atual do
>    código.
> 3. **`docs/DECISOES_E_CONVENCOES.md`** — as regras de código exigidas
>    pelo dono do projeto: nomenclatura em português, clean code,
>    responsabilidade única, e onde/como os princípios SOLID (OCP, LSP, ISP)
>    devem ser aplicados — com exemplos reais do código já escrito.
> 4. **`ARQUITETURA.md`** — por que o projeto é (e continuará sendo) um
>    projeto Django separado da futura plataforma financeira, e como a
>    conexão entre os dois já está preparada no código.
> 5. **`docs/ROADMAP_PLATAFORMA_FINANCEIRA.md`** — planejamento técnico da
>    Fase 2 (ainda não implementada): fluxo funcional completo, apps
>    Django sugeridos, onde aplicar SOLID por lá também.
>
> Nenhum desses documentos é opcional para entender o projeto — cada um
> cobre uma camada diferente (negócio → regras de código → arquitetura →
> futuro).

## Como rodar localmente

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

pip install -r requirements/desenvolvimento.txt

cp .env.example .env
# gere uma SECRET_KEY nova e cole no .env, por exemplo com:
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Acesse `http://127.0.0.1:8000/`. O painel administrativo (para ver os
contatos recebidos pelo formulário) fica em `/admin/`.

> ⚠️ Este projeto foi gerado num ambiente sem acesso à rede, então não foi
> possível instalar o Django e rodar `check`/`migrate`/`runserver` de fato
> durante a criação. A sintaxe de todos os arquivos `.py` foi validada com
> `py_compile`, e o código foi revisado manualmente — mas rode os comandos
> acima e confira antes de seguir desenvolvendo em cima.

## Estrutura

```
BRIEFING_PARA_DESENVOLVIMENTO_DO_SITE.docx   ideia de negócio original (fonte primária)
docs/
  CONTEXTO_DO_PROJETO.md         resumo do planejamento e das duas fases
  DECISOES_E_CONVENCOES.md       regras de código e SOLID, com exemplos
  ROADMAP_PLATAFORMA_FINANCEIRA.md   planejamento técnico da fase futura
ARQUITETURA.md                   por que dois projetos Django, e como se conectam
config/                          configuração do projeto (settings, urls, wsgi/asgi)
  settings/
    base.py                      configurações comuns
    desenvolvimento.py           configurações de dev
    producao.py                  configurações de produção
apps/
  nucleo/                        páginas institucionais (home, solução, sobre, etc.)
  captacao_leads/                formulário de contato comercial
    services/
      interfaces.py              contratos (ponto de conexão com a futura plataforma)
      notificador_por_email.py
      integrador_plataforma_associacoes.py   (stub, aguardando a plataforma)
templates/                       templates globais (base, cabeçalho, rodapé)
static/                          CSS com os tokens de marca da KotasPay
requirements/                    dependências por ambiente
```
