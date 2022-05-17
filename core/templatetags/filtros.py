from django import template

from core.models import Aluno, AlunosAtividade

register = template.Library()

rankings = {
    'K': 'Predador',
    'A': 'Realizador',
    'S': 'Socializador',
    'E': 'Explorador',
}

@register.filter(name='verificar_grupo')
def verificar_grupo(usuario, grupo):
    if grupo == "Alunos":
        return True
    return False

@register.filter(name='obter_aluno_atividade')
def obter_aluno_atividade(atividade, aluno):
    try:
        aluno_atividade = AlunosAtividade.objects.get(atividade=atividade, aluno=aluno)
        return aluno_atividade
    except Exception as e:
        print(e)
        return None

@register.filter(name='calcular_media')
def calcular_media(aluno, turma):
    try:
        atividades = AlunosAtividade.objects.filter(aluno=aluno, atividade__turma=turma)
        pts = 0
        qtd = atividades.count()
        for atividade in atividades:
            pts += atividade.nota
        return float(pts/qtd)
    except:
        return 0

@register.filter(name='obter_ranking_aluno')
def obter_ranking_aluno(usuario):
    try:
        aluno = Aluno.objects.get(usuario=usuario)
        return rankings[aluno.tipo]
    except:
        return 'Professor'
    
@register.filter(name='calcular_pontuacao_total')
def calcular_pontuacao_total(aluno, turma):
    return aluno.calcular_pontuacao_total(turma)
        