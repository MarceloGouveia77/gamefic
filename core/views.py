from django.shortcuts import render

# Create your views here.

def index(request):
    data = {
        'dashboard_active': 'active',
        'nome': 'Gabriel Coutinho'
    }
    return render(request, 'core/index.html', data)

def alunos(request):
    data = {
        'alunos_active': 'active'
    }
    return render(request, 'core/alunos.html', data)

def pontuacoes(request):
    data = {
        'pontuacoes_active': 'active'
    }
    return render(request, 'core/pontuacoes.html', data)

def sugestao(request):
    data = {
        'sugestao_active': 'active'
    }
    return render(request, 'core/sugestao.html', data)