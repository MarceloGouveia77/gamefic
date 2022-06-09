import json
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render, reverse
from core.constants import QUESTOES
from core.forms import AlunoForm, TurmaForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from core.models import Aluno, AlunosAtividade, AlunosTurma, Atividade, Professor, ProfessoresTurma, Turma
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
from collections import Counter
import uuid

# Create your views here.

rankings = {
    'K': 'Predador',
    'A': 'Realizador',
    'S': 'Socializador',
    'E': 'Explorador',
}

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
    
    next = False
    if request.GET.get("next"):
        next = request.GET.get("next")
    return render(request, 'core/login.html', {'next': next})

def cadastrar_aluno(request):
    data = {}
    if request.method == "POST":
        professor = False
        if request.POST.get('tipoCadastro') == 'professor':
            professor = True
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
        usuario.first_name = request.POST.get("nome")
        usuario.last_name = request.POST.get("sobrenome")
        if professor:
            usuario.is_superuser = True
        usuario.save()
        
        try:
            if professor:
                Professor.objects.create(
                    nome=request.POST.get("nome"),
                    sobrenome=request.POST.get("sobrenome"),
                    usuario=usuario
                )
            else:
                Aluno.objects.create(
                    nome=request.POST.get("nome"),
                    sobrenome=request.POST.get("sobrenome"),
                    usuario=usuario
                )
            data['cadastrado'] = True
        except:
            data['erro'] = "Ocorreu um erro ao cadastrar o aluno"
            
        if data['cadastrado'] and request.GET.get('next'):
            return redirect(request.GET.get('next'))
    return render(request, 'core/cadastrar_aluno.html', data)

def logout_site(request):
    logout(request)
    return redirect('core:login')

@login_required(login_url='/login')
def index(request):
    try:
        aluno = Aluno.objects.get(usuario=request.user)
        if not aluno.confirmado:
            if request.GET.get('next'):
                return redirect(reverse('core:questionario') + '?next=' + request.GET.get('next'))
            return redirect('core:questionario')
    except:
        pass
    data = {
        'pagina': 'Dashboard',
        'nome': 'Gabriel Coutinho'
    }
    return render(request, 'core/index.html', data)

@login_required(login_url='/login')
def alunos(request):
    data = {
        'pagina': 'Alunos',
        'alunos': Aluno.objects.all().order_by('nome')
    }
    return render(request, 'core/alunos/index.html', data)

@login_required(login_url='/login')
def pontuacoes(request):
    data = {
        'pontuacoes_active': 'active'
    }
    return render(request, 'core/pontuacoes.html', data)

@login_required(login_url='/login')
def sugestao(request):
    todas_turmas = Turma.objects.all().order_by('nome')
    turmas = []
    
    for turma in todas_turmas:
        try:
            ProfessoresTurma.objects.get(turma=turma, professor__usuario=request.user)
            turmas.append(turma)
        except:
            continue
        
    data = {
        'turmas': turmas,
        'pagina': 'Sugestão de Gamificação'
    }
    return render(request, 'core/sugestao.html', data)

@csrf_exempt
def graficos_sugestao(request):
    todas_turmas = Turma.objects.all().order_by('nome')
    turmas = []
    
    for turma in todas_turmas:
        categorias = []
        dados = []
        try:
            ProfessoresTurma.objects.get(turma=turma, professor__usuario=request.user)
            alunos_turma = AlunosTurma.objects.filter(turma=turma)
            for at in alunos_turma:
                categorias.append(at.aluno.tipo)
            
            total_alunos = alunos_turma.count()
            for categoria in set(categorias):
                qtd_alunos = alunos_turma.filter(aluno__tipo=categoria).count()
                porcentagem = (qtd_alunos / total_alunos) * 100
                dados.append({
                    'categoria': rankings[categoria],
                    'porcentagem': round(porcentagem, 0)
                })
                
            turmas.append({
                "turma_id": turma.id,
                "turma": turma.nome,
                "dados": dados,
                "grafico_id": f"grafico-{turma.id}"
            })
        except:
            continue
    
    return JsonResponse(turmas, safe=False)

@login_required(login_url='/login')
def turmas(request):
    try:
        aluno = Aluno.objects.get(usuario=request.user)
        if not aluno.confirmado:
            if request.GET.get('next'):
                return redirect(reverse('core:questionario') + '?next=' + request.GET.get('next'))
            return redirect('core:questionario')
    except:
        pass
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
        'pagina': 'Minhas Turmas',
        'turmas': turmas
    }
    return render(request, 'core/turmas/index.html', data)

@login_required(login_url='/login')
def cadastrar_turma(request):
    form = TurmaForm(request.POST or None)
    if form.is_valid():
        turma = form.save()
        turma.ingressar_professor(Professor.objects.get(usuario=request.user))
        return redirect('core:turmas')
    return render(request, 'core/turmas/cadastrar.html', {'form': form, 'btn': 'Cadastrar', 'tela': 'Cadastrar', 'turmas_active': 'active',})

@login_required(login_url='/login')
def editar_turma(request, id):
    turma = Turma.objects.get(id=id)
    form = TurmaForm(request.POST or None, instance=turma)
    if form.is_valid():
        turma = form.save()
        return redirect('core:detalhe_turma', pk=turma.id)
    return render(request, 'core/turmas/cadastrar.html', {'form': form, 'btn': 'Salvar', 'tela': 'Editar', 'turmas_active': 'active',})

def excluir_turma(request, id):
    try:
        turma = Turma.objects.get(id=id)
        turma.delete()
        return JsonResponse({'sucesso': True, 'msg': 'Turma excluída com sucesso'})
    except:
        return JsonResponse({'sucesso': False, 'msg': 'Erro ao excluir turma'})

def excluir_aluno_turma(request, id):
    try:
        aluno = AlunosTurma.objects.get(id=id)
        aluno.delete()
        return JsonResponse({'sucesso': True, 'msg': 'Aluno excluído com sucesso'})
    except:
        return JsonResponse({'sucesso': False, 'msg': 'Erro ao excluir aluno'})

@login_required(login_url='/login')
def detalhe_turma(request, pk):
    try:
        aluno = Aluno.objects.get(usuario=request.user)
        if not aluno.confirmado:
            if request.GET.get('next'):
                return redirect(reverse('core:questionario') + '?next=' + request.GET.get('next'))
            return redirect('core:questionario')
    except:
        pass
    turma = Turma.objects.get(id=pk)
    
    alunos = AlunosTurma.objects.filter(turma=turma).order_by('aluno__nome')

    data = {
        'pagina': 'Minhas Turmas',
        'turma': turma,
        'alunos_turma': alunos,
        'alunos_ranking': alunos.order_by('-pontuacao'),
        'professores': ProfessoresTurma.objects.filter(turma=turma),
        'atividades': Atividade.objects.filter(turma=turma)
    }
    return render(request, 'core/turmas/detalhe.html', data)

def obter_sugestao_turma(request, id):
    turma = Turma.objects.get(id=id)
    return JsonResponse({'descricao': turma.obter_sugestao()['descricao'],
                        'tipo': rankings[turma.obter_sugestao()['tipo']]})

@csrf_exempt
def gerar_link_tuma(request, pk):
    turma = Turma.objects.get(id=pk)
    if not turma.hash_convite: 
        turma.hash_convite = uuid.uuid4()
        turma.save()
    return JsonResponse({'link': f'https://gameizi.ddns.net/turmas/entrar/{turma.hash_convite}/'}, status=200)

@login_required(login_url='/login')
def entrar_turma(request, hash):
    try:
        aluno = Aluno.objects.get(usuario=request.user)
        if not aluno.confirmado:
            return redirect(reverse('core:questionario') + '?next=' + f'/turmas/entrar/{hash}')
    except:
        pass
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

@login_required(login_url='/login')
def questionario(request):
    aluno = Aluno.objects.get(usuario=request.user)
    data = {
        'questoes': QUESTOES,
        'aluno': aluno
    }
    
    if request.method == "POST":
        items = request.POST.getlist("respostas")[0].split(",")
        ocorrencias = Counter(items)
        
        lista = []
        lista.append({'rank': 'A', 'ocorrencias': int(ocorrencias['A'])})
        lista.append({'rank': 'K', 'ocorrencias': int(ocorrencias['K'])})
        lista.append({'rank': 'E', 'ocorrencias': int(ocorrencias['E'])})
        lista.append({'rank': 'S', 'ocorrencias': int(ocorrencias['S'])})
        
        maior = 0
        rank = ''
        for item in lista:
            if item['ocorrencias'] > maior:
                maior = item['ocorrencias']
                rank = item['rank']
                
        aluno.tipo = rank
        aluno.confirmado = True
        aluno.save()
        next = "/"
        if request.GET.get('next'):
            next = request.GET.get('next')
            print(next)
        return JsonResponse({'sucesso': True, 'msg': f"Resultado de seu perfil: {rankings[aluno.tipo]}", 'next': next})
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

@csrf_exempt
def alterar_nota(request):
    if request.method == "POST":
        conteudo = json.loads(request.body)
        atividade_id = int(conteudo['atividade_id'])
        nota = float(conteudo['nota'])
        
        try:
            aluno_atividade = AlunosAtividade.objects.get(id=atividade_id)
            aluno_atividade.nota = nota
            aluno_atividade.save()
            media = aluno_atividade.aluno.calcular_media(aluno_atividade.atividade.turma)
            pontuacao = aluno_atividade.aluno.calcular_pontuacao_total(aluno_atividade.atividade.turma)
            return JsonResponse({
                "msg": "Nota alterada com sucesso", 
                'status': "ok", 
                "media": media,
                "pontuacao": pontuacao,
                "aluno_id": aluno_atividade.aluno.id
                }, status=200)
        except:
            return JsonResponse({"msg": "Erro ao alterar nota"}, status=400)
            