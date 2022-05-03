from django.db import models
from django.conf import settings
from django.forms import ValidationError

TIPOS_ALUNOS = [
    ('P', 'Predador'),
    ('R', 'Realizador'),
    ('S', 'Socializador'),
    ('E', 'Explorador'),
]
class Aluno(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    nome = models.CharField("Nome", max_length=1024, null=False)
    sobrenome = models.CharField("Sobrenome", max_length=1024, null=False)
    pontuacao = models.FloatField("Pontuação", default=0, blank=True, null=True)
    tipo = models.CharField("Tipo", choices=TIPOS_ALUNOS, max_length=1024, default='P', blank=True, null=True)
    confirmado = models.BooleanField('Confirmado', default=False)
    criado_em = models.DateField("Criado Em", auto_now_add=True)

    def __str__(self):
        return f'{self.nome} {self.sobrenome}'
    
    def obter_nome_completo(self):
        return self.nome + ' ' + self.sobrenome
    
    def obter_quantidade_turmas(self):
        return AlunosTurma.objects.filter(aluno=self).count()
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
    
    def ingressar_aluno(self, aluno):
        try:
            AlunosTurma.objects.create(turma=self, aluno=aluno)
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

class AlunosTurma(models.Model):
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE)
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
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
    
