# Decisões e Convenções de Código

> Regras dadas explicitamente pelo dono do projeto durante o planejamento.
> Qualquer código novo — escrito por humano ou por um copiloto de IA — deve
> seguir isso. Este documento existe para que um modelo de IA local tenha as
> regras por escrito, sem depender de "lembrar" da conversa original.

## 1. Nomenclatura em português

**Regra**: todo nome de código próprio do projeto (apps, models, campos de
model, classes, views, funções, variáveis, templates, URLs nomeadas) deve
ser em **português**, mesmo que fique extenso — desde que continue claro.

**Exceção**: palavras-chave e convenções do Django, Python ou de
bibliotecas de terceiros continuam em inglês, porque mudá-las quebraria o
framework ou confundiria quem já conhece Django. Exemplos do que **não**
se traduz:
- Atributos/métodos que o Django espera por nome: `Meta`, `objects`,
  `save()`, `clean()`, `get_context_data()`, `as_view()`.
- Tipos de campo do ORM: `CharField`, `EmailField`, `TextField`,
  `DateTimeField`, `ForeignKey`.
- Nomes de configuração do `settings.py`: `INSTALLED_APPS`, `MIDDLEWARE`,
  `DATABASES`, `DEBUG`, `ALLOWED_HOSTS`.
- Nomes de pacotes/bibliotecas e seus imports (`django.db.models`,
  `django.views.generic`, etc.).

**Exemplos já aplicados no projeto** (para servir de padrão):

```python
# app: apps/captacao_leads (não "leads_capture")

class ContatoComercial(models.Model):          # não "CommercialContact"
    nome_completo = models.CharField(...)       # não "full_name"
    nome_da_organizacao = models.CharField(...) # não "organization_name"
    criado_em = models.DateTimeField(auto_now_add=True)  # não "created_at"

class FormularioDeContatoComercial(forms.ModelForm):  # não "ContactForm"
    ...

class FormularioDeContatoView(FormView):        # não "ContactFormView"
    ...
```

URLs nomeadas também em português:
```python
path("", FormularioDeContatoView.as_view(), name="contato")
# uso no template: {% url 'captacao_leads:contato' %}
```

## 2. Clean code e responsabilidade única

- **Nomes claros acima de nomes curtos.** `FormularioDeContatoComercial` é
  preferível a `FormContato`, mesmo sendo mais longo — clareza vence
  brevidade neste projeto.
- **Uma responsabilidade por classe/módulo/função.** Exemplos já aplicados:
  - `views.py` só orquestra requisição/resposta (recebe o form, decide o
    que fazer, redireciona).
  - `models.py` só descreve dados (nenhuma regra de notificação ou
    integração externa mora aqui).
  - `services/` concentra regras de notificação e integração externa —
    fora da view, fora do model.
  - `forms.py` só valida/mapeia dados de entrada.

## 3. Princípios SOLID — aplicados **apenas onde importa**

**Regra explícita do dono do projeto**: não aplicar SOLID (nem qualquer
abstração) em todo o código de forma indiscriminada. Onde não há variação
nem extensão futura prevista, o código deve continuar simples e direto.
Exemplo: as páginas institucionais em `apps/nucleo` usam `TemplateView` puro,
sem nenhuma camada de serviço — adicionar uma abstração ali seria
complexidade desnecessária.

Os princípios foram aplicados de forma **especial e deliberada no ponto de
conexão com a futura Plataforma de Associações** (app `captacao_leads`,
pasta `services/`), porque é exatamente ali que:
1. Sabemos que vai existir extensão futura (uma nova forma de notificar, uma
   integração real com a plataforma).
2. Ainda não sabemos os detalhes dessa extensão.

Isso é o cenário ideal para interfaces bem definidas — abstração no lugar
certo, não abstração por precaução genérica.

### O — Open/Closed Principle (Aberto para extensão, fechado para modificação)

> Entidades de software devem estar abertas para extensão, mas fechadas
> para modificação.

**Onde**: `apps/captacao_leads/services/interfaces.py` define o contrato
`NotificadorDeNovoContato`. `FormularioDeContatoView` depende dessa
interface (hoje, via a implementação concreta `NotificadorPorEmail`).

**Por que atende ao OCP**: se amanhã for preciso notificar também por
Slack, WhatsApp ou push, basta **criar uma nova classe** implementando
`NotificadorDeNovoContato` — nenhuma linha de `views.py` precisa mudar. A
funcionalidade se estende sem modificar código existente.

```python
# Exemplo de extensão futura, sem tocar em views.py:
class NotificadorPorSlack(NotificadorDeNovoContato):
    def notificar(self, contato: ContatoComercial) -> None:
        ...  # implementação nova, código existente intocado
```

### L — Liskov Substitution Principle (Substituição de Liskov)

> Objetos devem poder ser substituídos por instâncias de seus subtipos sem
> alterar a correção do funcionamento do sistema.

**Onde**: qualquer classe que implemente `NotificadorDeNovoContato` ou
`IntegradorDeContatoComSistemaExterno` deve poder substituir a
implementação atual **sem quebrar quem a usa**.

**Por que atende ao LSP**: é esse contrato que garante que, no futuro,
`IntegradorComPlataformaDeAssociacoes` (hoje um stub) poderá substituir uma
eventual implementação de CRM — ou o inverso — sem que o código que os
utiliza precise saber qual implementação específica está por trás da
interface. Nenhuma implementação pode, por exemplo, exigir um parâmetro
extra que as outras não têm, ou lançar uma exceção que quem chama não
espera — isso quebraria a substituibilidade.

### I — Interface Segregation Principle (Segregação de Interface)

> É melhor várias interfaces específicas do que uma única interface
> genérica e gigante que força classes a implementar métodos que não usam.

**Onde**: `NotificadorDeNovoContato` (avisar um humano) e
`IntegradorDeContatoComSistemaExterno` (enviar dado para outro sistema) são
**duas interfaces separadas**, não uma única `IServicoDeContato` genérica.

**Por que atende ao ISP**: uma implementação de e-mail
(`NotificadorPorEmail`) não é forçada a saber como sincronizar dado com uma
API externa. Uma futura implementação de integração com a Plataforma de
Associações não é forçada a saber enviar e-mail. Cada interface tem só o
que quem a implementa realmente precisa usar.

### Onde SOLID **não** foi aplicado, de propósito

- `apps/nucleo` inteiro: páginas estáticas, `TemplateView` direto, sem
  interfaces, sem services. Não há extensão futura prevista ali.
- `FormularioDeContatoComercial` (o `ModelForm`): é só validação de campo,
  não há variação de comportamento a prever.
- Qualquer lugar do projeto onde criar uma interface não teria mais de uma
  implementação real ou prevista — isso seria abstração especulativa, que o
  dono do projeto pediu explicitamente para evitar.

## 4. Convenções de pastas e arquivos

Segue o padrão amplamente adotado pela comunidade Django (não uma
convenção própria do projeto):

```
config/                 configuração do projeto (não é um "app" de negócio)
  settings/
    base.py              comum a todos os ambientes
    desenvolvimento.py    settings de dev
    producao.py           settings de produção
  urls.py                 roteamento raiz
  wsgi.py / asgi.py
apps/                    apps de negócio do projeto, um por responsabilidade
  <nome_do_app>/
    migrations/
    templates/<nome_do_app>/   (templates namespaced pelo nome do app)
    models.py
    views.py
    urls.py
    forms.py
    admin.py
    apps.py
    services/            (só quando o app tem regra de negócio que
                          justifique isolar de views.py/models.py)
templates/               templates GLOBAIS (base.html, includes/)
static/                  CSS/JS/imagens globais
requirements/            dependências separadas por ambiente
```

Motivo de cada escolha:
- `apps/` como pasta contêiner (em vez dos apps soltos na raiz do projeto)
  deixa claro, à primeira vista, o que é "configuração de projeto" (`config/`)
  e o que é "app de negócio" (`apps/*`) — comum em projetos Django maiores.
- `services/` dentro de um app só aparece quando há regra de negócio
  relevante o bastante para não morar em `views.py`/`models.py` — não é um
  padrão aplicado a todo app por padrão (ver `apps/nucleo`, que não tem essa
  pasta).
- `requirements/` dividido por ambiente é convenção comum de mercado para
  evitar instalar dependências de desenvolvimento (`django-extensions`, por
  exemplo) em produção.
