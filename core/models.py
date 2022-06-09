from django.db import models
from django.conf import settings
from django.forms import ValidationError
from django.utils.safestring import mark_safe

from core.constants import SUGESTOES

rankings = {
    'K': 'Predador',
    'A': 'Realizador',
    'S': 'Socializador',
    'E': 'Explorador',
}

TIPOS_ALUNOS = [
    ('K', 'Predador'),
    ('A', 'Realizador'),
    ('S', 'Socializador'),
    ('E', 'Explorador'),
]
class Aluno(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    nome = models.CharField("Nome", max_length=1024, null=False)
    sobrenome = models.CharField("Sobrenome", max_length=1024, null=False)
    pontuacao = models.FloatField("Pontuação", default=0, blank=True, null=True)
    tipo = models.CharField("Tipo", choices=TIPOS_ALUNOS, max_length=1024, default='K', blank=True, null=True)
    confirmado = models.BooleanField('Confirmado', default=False)
    criado_em = models.DateField("Criado Em", auto_now_add=True)

    def __str__(self):
        return f'{self.nome} {self.sobrenome}'
    
    def obter_perfil(self):
        return rankings[self.tipo]
    
    def obter_nome_completo(self):
        return self.nome + ' ' + self.sobrenome
    
    def obter_quantidade_turmas(self):
        return AlunosTurma.objects.filter(aluno=self).count()
    
    def calcular_media(self, turma):
        try:
            atividades = AlunosAtividade.objects.filter(aluno=self, atividade__turma=turma)
            pts = 0
            qtd = atividades.count()
            for atividade in atividades:
                pts += atividade.nota
            return float(pts/qtd)
        except:
            return 0
        
    def calcular_pontuacao_total(self, turma):
        try:
            atividades = AlunosAtividade.objects.filter(aluno=self, atividade__turma=turma)
            total = 0
            for atividade in atividades:
                total += atividade.nota
            aluno_turma = AlunosTurma.objects.get(aluno=self, turma=turma)
            aluno_turma.pontuacao = float(total)
            aluno_turma.save()
            return float(total)
        except:
            return 0
        
class Turma(models.Model):
    nome = models.CharField('Nome', max_length=1024)
    criado_em = models.DateField("Criado Em", auto_now_add=True)
    ativa = models.BooleanField('Ativa', default=True)
    semestre = models.CharField("Semestre", max_length=1024)
    hash_convite = models.CharField('Hash Convite', max_length=1024, blank=True, null=True)
    
    def __str__(self):
        return self.nome
    
    def obter_quantidade_alunos(self):
        return AlunosTurma.objects.filter(turma=self).count()
    
    def obter_alunos(self):
        alunos_turma = AlunosTurma.objects.filter(turma=self)
        alunos = [alunos_t.aluno for alunos_t in alunos_turma]
        return alunos
    
    def ingressar_aluno(self, aluno):
        try:
            AlunosTurma.objects.create(turma=self, aluno=aluno)
            atividades = Atividade.objects.filter(turma=self)
            for at in atividades:
                at.popular()
            return True
        except:
            return False
        
    def ingressar_professor(self, professor):
        try:
            ProfessoresTurma.objects.create(turma=self, professor=professor)
            return True
        except Exception as e:
            print(e)
            return False
        
    def obter_sugestao(self):
        alunos_turma = AlunosTurma.objects.filter(turma=self)
        realizadores = alunos_turma.filter(aluno__tipo='A')
        predadores = alunos_turma.filter(aluno__tipo='K')
        socializadores = alunos_turma.filter(aluno__tipo='S')
        exploradores = alunos_turma.filter(aluno__tipo='E')

        maior, tipo = None, None
        
        if realizadores:
            maior = realizadores.count()
            tipo = 'A'
        if predadores and (predadores.count() > maior):
            maior = predadores.count()
            tipo = 'K'
        if socializadores and (socializadores.count() > maior):
            maior = socializadores.count()
            tipo = 'S'
        if exploradores and (exploradores.count() > maior):
            maior = exploradores.count()
            tipo = 'E'
            
        if tipo:
            return {'tipo': tipo, 'descricao': mark_safe(SUGESTOES[tipo])}
        return ''
class AlunosTurma(models.Model):
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE)
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    pontuacao = models.FloatField('Pontuação', default=0)
    data_criacao = models.DateField("Criado Em", auto_now_add=True)
    
    def __str__(self):
        return f'{self.turma.nome} - {self.aluno.nome}'
class Professor(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    nome = models.CharField("Nome", max_length=1024, null=False)
    sobrenome = models.CharField("Sobrenome", max_length=1024, null=False)
    criado_em = models.DateField("Criado Em", auto_now_add=True)

    def __str__(self):
        return f'{self.nome} {self.sobrenome}'
class ProfessoresTurma(models.Model):
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE)
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    data_criacao = models.DateField("Criado Em", auto_now_add=True)
    
    def __str__(self):
        return f'{self.turma.nome} - {self.professor.nome}'
    
class Atividade(models.Model):
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE)
    descricao = models.CharField('Descricao', max_length=1024)
    data_criacao = models.DateField("Criado Em", auto_now_add=True)
    
    def __str__(self):
        return self.descricao
    
    def popular(self):
        alunos_turma = AlunosTurma.objects.filter(turma=self.turma)
        for aluno_turma in alunos_turma:
            try:
                AlunosAtividade.objects.get(aluno=aluno_turma.aluno, atividade=self)
                continue
            except:
                AlunosAtividade.objects.create(atividade=self, aluno=aluno_turma.aluno)
        return True
    
class AlunosAtividade(models.Model):
    atividade = models.ForeignKey(Atividade, on_delete=models.CASCADE)
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    nota = models.FloatField('Nota', default=0)
    
    def __str__(self):
        return self.atividade.descricao + ' - ' + self.aluno.obter_nome_completo()