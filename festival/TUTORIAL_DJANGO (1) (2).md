# Tutorial Django — Do Zero ao CRUD com Autenticação

## 1. Instalação

```bash
pip install django
```

---

## 2. Criar o Projeto

```bash
django-admin startproject nome_projeto .
```

> O `.` no final cria o projeto na pasta atual, sem subpasta extra.

Rodar o servidor:

```bash
python manage.py runserver
```

Acesse `http://127.0.0.1:8000` — deve aparecer a página de boas-vindas do Django.

---

## 3. Criar um App

```bash
python manage.py startapp nome_app
```

Registrar o app em `nome_projeto/settings.py`:

```python
INSTALLED_APPS = [
    ...
    'nome_app',
]
```

> **Atenção:** crie o app primeiro, depois registre. Ao contrário gera erro.

Estrutura criada:
```
nome_app/
    migrations/
    admin.py
    apps.py
    models.py
    tests.py
    views.py
```

---

## 4. Models

Em `nome_app/models.py`:

```python
from django.db import models

class Pessoa(models.Model):
    nome = models.CharField(max_length=100)
    idade = models.IntegerField()
    palco = models.ForeignKey(Palco, on_delete=models.CASCADE, related_name="concertos")

    def __str__(self):
        return self.nome

class Tarefa(models.Model):
    titulo = models.CharField(max_length=200)
    descricao = models.TextField(blank=True)
    concluida = models.BooleanField(default=False)
    criada_em = models.DateTimeField(auto_now_add=True)
    pessoa = models.ForeignKey(Pessoa, related_name='tarefas', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.titulo
```

### estilos page 

{% extends 'festival/layout.html' %}

{% block content %}
    
{% for estilo in estilos %}
<h3>{{estilo.nome}}</h3>

    {% for banda in estilo.bandas.all %}
        <article class="card">
           <li>{{ banda.nome }}</li>
        </article>
    {% endfor %}

{% endfor %}

{% endblock %}

### Dias page

{% extends 'festival/layout.html' %}

{% block content %}

<h1>Dias do Festival</h1>

{% for dia in dias %}
    <h2>
        {{ dia.data }}
    </h2>

    {% for concerto in dia.concertos.all %}
        <div class="card">
            {{ concerto.banda.nome }} —
            {{ concerto.hora }} —
            {{ concerto.palco.nome }} 
            {% for estilo in concerto.banda.estilos.all %}
                ({{ estilo.nome }})
            {% empty %}
                
            {% endfor %}
        </div>
    {% empty %}
        <p>Sem concertos neste dia</p>
    {% endfor %}

{% endfor %}
{% endblock %}



### Tipos de campo comuns

| Campo | Uso |
|---|---|
| `CharField(max_length=N)` | Texto curto |
| `TextField()` | Texto longo |
| `IntegerField()` | Número inteiro |
| `BooleanField()` | Verdadeiro/Falso |
| `DateTimeField(auto_now_add=True)` | Data/hora automática na criação |
| `ForeignKey(Model, on_delete=...)` | Relação entre tabelas |

### Opções úteis

- `blank=True` — permite vazio em formulários
- `null=True` — permite NULL no banco de dados
- `default=valor` — valor padrão

### ForeignKey — regra do lado

O `ForeignKey` sempre fica no lado do "muitos":
- Uma `Pessoa` tem várias `Tarefas` → o `ForeignKey` fica em `Tarefa`

### Migrar para o banco

```bash
python manage.py makemigrations   # prepara as mudanças
python manage.py migrate          # aplica ao banco
```

---

## 5. Django Admin

Em `nome_app/admin.py`:

```python
from django.contrib import admin
from .models import Tarefa, Pessoa

admin.site.register(Tarefa)
admin.site.register(Pessoa)
```

Criar superusuário:

```bash
python manage.py createsuperuser
```

Acesse `http://127.0.0.1:8000/admin`.

---

## 6. URLs

Em `nome_projeto/urls.py`:

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),  # login/logout
    path('', include('nome_app.urls')),
]
```

Criar `nome_app/urls.py`:

```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_tarefas, name='lista_tarefas'),
    path('criar/', views.criar_tarefa, name='criar_tarefa'),
    path('editar/<int:pk>/', views.editar_tarefa, name='editar_tarefa'),
    path('deletar/<int:pk>/', views.deletar_tarefa, name='deletar_tarefa'),
]
```

> `<int:pk>` captura um número da URL e passa como argumento `pk` para a view.

---

## 7. Views

Em `nome_app/views.py`:

```python
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Tarefa, Pessoa
from .forms import TarefaForm

@login_required
def lista_tarefas(request):
    pessoas = Pessoa.objects.order_by('nome')
    return render(request, 'nome_app/lista.html', {'pessoas': pessoas})

@login_required
def criar_tarefa(request):
    if request.method == 'POST':
        form = TarefaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_tarefas')
    else:
        form = TarefaForm()
    return render(request, 'nome_app/form.html', {'form': form})

@login_required
def editar_tarefa(request, pk):
    tarefa = get_object_or_404(Tarefa, pk=pk)
    if request.method == 'POST':
        form = TarefaForm(request.POST, instance=tarefa)
        if form.is_valid():
            form.save()
            return redirect('lista_tarefas')
    else:
        form = TarefaForm(instance=tarefa)
    return render(request, 'nome_app/form.html', {'form': form})

@login_required
def deletar_tarefa(request, pk):
    tarefa = get_object_or_404(Tarefa, pk=pk)
    if request.method == 'POST':
        tarefa.delete()
        return redirect('lista_tarefas')
    return render(request, 'nome_app/confirmar_delete.html', {'tarefa': tarefa})
```

### Conceitos importantes

- `render(request, template, contexto)` — renderiza o template com os dados
- `redirect('nome_da_url')` — redireciona para outra página
- `get_object_or_404(Model, pk=pk)` — busca pelo ID ou retorna 404
- `@login_required` — exige login para acessar a view
- `Tarefa.objects.all()` — busca todos os registros
- `Tarefa.objects.order_by('campo')` — ordena (use `-campo` para decrescente)
- `Tarefa.objects.filter(campo=valor)` — filtra registros

---

## 8. Templates

### Estrutura de pastas

```
nome_app/
    templates/
        nome_app/
            base.html
            lista.html
            form.html
            confirmar_delete.html
        registration/
            login.html
```

### base.html

```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{% block titulo %}Meu Site{% endblock %}</title>
</head>
<body>
    <nav>
        <a href="/">Início</a>
        {% if user.is_authenticated %}
            <span>Olá, {{ user.username }}</span>
            <form method="POST" action="/accounts/logout/" style="display:inline">
                {% csrf_token %}
                <button type="submit">Logout</button>
            </form>
        {% else %}
            <a href="/accounts/login/">Login</a>
        {% endif %}
    </nav>

    <main>
        {% block conteudo %}{% endblock %}
    </main>
</body>
</html>
```

### lista.html

```html
{% extends 'nome_app/base.html' %}

{% block titulo %}Lista{% endblock %}

{% block conteudo %}
    <h1>Tarefas</h1>
    <a href="{% url 'criar_tarefa' %}">Nova Tarefa</a>

    <ul>
        {% for pessoa in pessoas %}
            <li>{{ pessoa.nome }}
                <ul>
                    {% for tarefa in pessoa.tarefas.all %}
                        <li>
                            {{ tarefa.titulo }}
                            <a href="{% url 'editar_tarefa' tarefa.pk %}">Editar</a>
                            <a href="{% url 'deletar_tarefa' tarefa.pk %}">Deletar</a>
                        </li>
                    {% empty %}
                        <li>Sem tarefas.</li>
                    {% endfor %}
                </ul>
            </li>
        {% empty %}
            <li>Nenhuma pessoa cadastrada.</li>
        {% endfor %}
    </ul>
{% endblock %}
```

### form.html

```html
{% extends 'nome_app/base.html' %}

{% block titulo %}Formulário{% endblock %}

{% block conteudo %}
    <h1>Formulário</h1>
    <form method="POST">
        {% csrf_token %}
        {{ form.as_p }}
        <button type="submit">Salvar</button>
    </form>
    <a href="{% url 'lista_tarefas' %}">Voltar</a>
{% endblock %}
```

### confirmar_delete.html

```html
{% extends 'nome_app/base.html' %}

{% block titulo %}Deletar{% endblock %}

{% block conteudo %}
    <h1>Deletar</h1>
    <p>Tem certeza que deseja deletar <strong>{{ tarefa.titulo }}</strong>?</p>
    <form method="POST">
        {% csrf_token %}
        <button type="submit">Sim, deletar</button>
        <a href="{% url 'lista_tarefas' %}">Cancelar</a>
    </form>
{% endblock %}
```

### registration/login.html

```html
{% extends 'nome_app/base.html' %}

{% block titulo %}Login{% endblock %}

{% block conteudo %}
    <h1>Login</h1>
    <form method="POST">
        {% csrf_token %}
        {{ form.as_p }}
        <button type="submit">Entrar</button>
    </form>
{% endblock %}
```

### Sintaxe dos templates

| Sintaxe | Uso |
|---|---|
| `{{ variavel }}` | Imprime o valor |
| `{% tag %}` | Executa lógica |
| `{% extends 'base.html' %}` | Herda de outro template |
| `{% block nome %}{% endblock %}` | Define área substituível |
| `{% for x in lista %}{% endfor %}` | Loop |
| `{% empty %}` | Executado se a lista estiver vazia |
| `{% if condicao %}{% endif %}` | Condicional |
| `{% url 'nome_url' %}` | Gera URL pelo nome |
| `{% csrf_token %}` | Token de segurança (obrigatório em forms POST) |

---

## 9. Forms

Criar `nome_app/forms.py`:

```python
from django import forms
from .models import Tarefa

class TarefaForm(forms.ModelForm):
    class Meta:
        model = Tarefa
        fields = ['titulo', 'descricao', 'concluida', 'pessoa']
```

- `ModelForm` — gera o form automaticamente a partir do model
- `fields` — lista de campos que aparecem no formulário

---

## 10. Autenticação

Adicionar em `settings.py`:

```python
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/accounts/login/'
```

Adicionar em `urls.py` do projeto:

```python
path('accounts/', include('django.contrib.auth.urls')),
```

Isso já fornece as URLs:
- `/accounts/login/` — login
- `/accounts/logout/` — logout

Proteger uma view com `@login_required` — redireciona para o login se não estiver autenticado.

---

## Fluxo resumido

```
URL → urls.py → View → (busca dados do Model) → renderiza Template → resposta ao usuário
```

## Comandos essenciais

```bash
django-admin startproject nome .   # cria o projeto
python manage.py startapp nome     # cria um app
python manage.py makemigrations    # prepara mudanças no banco
python manage.py migrate           # aplica ao banco
python manage.py createsuperuser   # cria usuário admin
python manage.py runserver         # roda o servidor
```
class ConcertoForm(forms.ModelForm):
    class Meta:
        model = Concerto
        fields = ["banda", "dia", "hora", "palco"]

def editar_concerto_view(request, concerto_id):
    concerto = get_object_or_404(Concerto, id=concerto_id)

    if request.method == 'POST':
        form = ConcertoForm(request.POST, instance=concerto)
        if form.is_valid():
            form.save()
            return redirect('concerto', concerto_id=concerto.id)
    else:
        form = ConcertoForm(instance=concerto)

    context = {
        'concerto': concerto,
        'form': form,
    }

    return render(request, 'festival/editar_concerto.html', context)

def criar_concerto_view(request):
    if request.method == 'POST':
        form = ConcertoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dias')  # Redireciona para a lista após criar
    else:
        form = ConcertoForm()
    return render(request, 'festival/editar_concerto.html', {'form': form})


def apagar_concerto_view(request, concerto_id):
    concerto = get_object_or_404(Concerto, id=concerto_id)
    if request.method == 'POST':
        concerto.delete()
        return redirect('dias')
    return redirect('concerto', concerto_id=concerto.id)


urls
path('concertos/<int:concerto_id>/editar/', views.editar_concerto_view, name='editar_concerto'),


concerto.html
    <p><a href="{% url 'editar_concerto' concerto.id %}" class="btn">Editar este concerto</a></p>

editar_concerto.html

{% extends 'festival/layout.html' %}

{% block content %}
<article class="card">
    <h2>Editar concerto</h2>
    <p><strong>Concerto atual:</strong> {{ concerto.banda.nome }} - {{ concerto.dia }} - {{ concerto.hora }}</p>

    <form method="post" style="display: grid; gap: 12px; max-width: 520px;">
        {% csrf_token %}
        {{ form.as_p }}
        <button type="submit" class="btn">Guardar</button>
    </form>
</article>
{% endblock %}
