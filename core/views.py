import json
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from core.constants import QUESTOES
from core.forms import AlunoForm, TurmaForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from core.models import Aluno, AlunosTurma, Atividade, Professor, ProfessoresTurma, Turma
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
from collections import Counter
import uuid

# Create your views here.

def login_sistema(request):
    if request.user.is_authenticated:
        return redirect('core:index')
    
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        User = get_user_model()
        
        usuario = None
        try:
            username = (User.objects.get(email=email)).username
            usuario = authenticate(request, username=username, password=password)
        except:
            return render(request, 'core/login.html', {'erro': 'Email não cadastrado'})
        
        if usuario:
            login(request, usuario)
            if request.GET.get("next"):
                destino = request.GET.get("next")
                return redirect(destino)
            try:
                aluno = Aluno.objects.get(usuario=usuario)
                if not aluno.confirmado:
                    return redirect('core:questionario')
                return redirect('core:index')
            except:
                return redirect('core:index')
        else:
            return render(request, 'core/login.html', {'erro': 'Email ou senha inválidos.'})
    
    return render(request, 'core/login.html', {})

def cadastrar_aluno(request):
    form = AlunoForm(request.POST or None)
    data = {
        'form': form
    }
    
    if request.method == "POST":
        User = get_user_model()
        
        email = request.POST.get("email")
        senha = request.POST.get("password")
        senha_confirm = request.POST.get("password_confirm")
        
        try:
            User.objects.get(email=email)
            data['erro'] = "Este email já está cadastrado"
            return render(request, 'core/cadastrar_aluno.html', data)
        except:
            pass
        
        if senha != senha_confirm:
            data['erro'] = "Confirmação de senha inválida"
            return render(request, 'core/cadastrar_aluno.html', data)
        
        usuario = User.objects.create_user(uuid.uuid4(), email, senha)
        
        if form.is_valid():
            aluno = form.save(commit=False)
            aluno.usuario = usuario
            aluno.save()
            data['cadastrado'] = True
    return render(request, 'core/cadastrar_aluno.html', data)

def logout_site(request):
    logout(request)
    return redirect('core:login')

def index(request):
    try:
        aluno = Aluno.objects.get(usuario=request.user)
        if not aluno.confirmado:
            return redirect('core:questionario')
    except:
        pass
    data = {
        'dashboard_active': 'active',
        'nome': 'Gabriel Coutinho'
    }
    return render(request, 'core/index.html', data)

def alunos(request):
    data = {
        'alunos_active': 'active',
        'alunos': Aluno.objects.all().order_by('nome')
    }
    return render(request, 'core/alunos/index.html', data)

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

def turmas(request):
    todas_turmas = Turma.objects.all().order_by('nome')
    turmas = []
    
    for turma in todas_turmas:
        try:
            if request.user.is_superuser:
                ProfessoresTurma.objects.get(turma=turma, professor__usuario=request.user)
                turmas.append(turma)
            else:
                AlunosTurma.objects.get(aluno__usuario=request.user, turma=turma)
                turmas.append(turma)
            continue
        except Exception as e:
            print(e)
            continue
    
    data = {
        'turmas_active': 'active',
        'turmas': turmas
    }
    return render(request, 'core/turmas/index.html', data)

def cadastrar_turma(request):
    form = TurmaForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('core:turmas')
    return render(request, 'core/turmas/cadastrar.html', {'form': form, 'turmas_active': 'active',})

def detalhe_turma(request, pk):
    turma = Turma.objects.get(id=pk)
    
    data = {
        'turmas_active': 'active',
        'turma': turma,
        'alunos_turma': AlunosTurma.objects.filter(turma=turma),
        'professores': ProfessoresTurma.objects.filter(turma=turma),
        'atividades': Atividade.objects.filter(turma=turma)
    }
    return render(request, 'core/turmas/detalhe.html', data)

@csrf_exempt
def gerar_link_tuma(request, pk):
    turma = Turma.objects.get(id=pk)
    turma.hash_convite = uuid.uuid4()
    turma.save()
    return JsonResponse({'link': f'http://localhost:8000/turmas/entrar/{turma.hash_convite}/'}, status=200)

@login_required(login_url='/login')
def entrar_turma(request, hash):
    data = {
        'hash': hash,
    }
    
    try:
        turma = Turma.objects.get(hash_convite=hash)
        data['turma'] = turma
    except:
        data['erro'] = 'Link expirado'
        return render(request, 'core/turmas/entrar.html', data)
    
    if request.method == "GET":
        return render(request, 'core/turmas/entrar.html', data)
    
    elif request.method == "POST":
        turma = Turma.objects.get(hash_convite=hash)
        
        try:
            aluno = Aluno.objects.get(usuario=request.user)
        except:
            aluno = None
        
        try:
            professor = Professor.objects.get(usuario=request.user)
        except:
            professor = None
        
        if professor:
            try:
                ProfessoresTurma.objects.get(turma=turma, professor=professor)
                data['erro'] = 'Você já faz parte desta turma.'
                return render(request, 'core/turmas/entrar.html', data)
            except:
                pass
            
        if aluno:
            try:
                AlunosTurma.objects.get(turma=turma, aluno=aluno)
                data['erro'] = 'Você já faz parte desta turma.'
                return render(request, 'core/turmas/entrar.html', data)
            except:
                pass

        ingresso_aluno = turma.ingressar_aluno(aluno)
        ingresso_professor = turma.ingressar_professor(professor)
        
        if ingresso_aluno or ingresso_professor:
            return redirect('core:detalhe_turma', pk=turma.id)
        else:
            data['erro'] = 'Ocorreu um erro ao juntar-se na turma.'
            return render(request, 'core/turmas/entrar.html', data)
    else:
        return JsonResponse({'msg': 'Método não autorizado'}, status=405)
    
def questionario(request):
    aluno = Aluno.objects.get(usuario=request.user)
    data = {
        'questoes': QUESTOES,
        'aluno': aluno
    }
    
    if request.method == "POST":
        items = request.POST.getlist("respostas")[0].split(",")
        ocorrencias = Counter(items)
        aluno.confirmado = True
        aluno.save()
        return HttpResponse(f"Resultado de seu perfil: {aluno.tipo}")
    return render(request, 'core/questionario.html', data)

@csrf_exempt
def cadastrar_atividade(request):
    conteudo = json.loads(request.body)
    descricao = conteudo['descricao']
    turma_id = int(conteudo['turma'])
    
    atividade = Atividade.objects.create(
        turma_id=turma_id,
        descricao=descricao
    )
    
    atividade.popular()
    return JsonResponse({"msg": "Atividade Cadastrada com sucesso"}, status=200)