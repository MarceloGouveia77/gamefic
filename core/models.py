from django.db import models
from django.conf import settings

TIPOS_ALUNOS = [
    ('P', 'Predador'),
    ('R', 'Realizador'),
    ('S', 'Socializador'),
    ('E', 'Explorador'),
]
class Aluno(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    nome = models.CharField("Nome", max_length=1024, null=False)
    sobrenome = models.CharField("Sobrenome", max_length=1024, null=False)
    pontuacao = models.FloatField("Pontuação", default=0)
    tipo = models.CharField("Tipo", choices=TIPOS_ALUNOS, max_length=1024, default='P')
    criado_em = models.DateField("Criado Em", auto_now_add=True)

    def __str__(self):
        return f'{self.nome} {self.sobrenome}'

class Turma(models.Model):
    nome = models.CharField('Nome', max_length=1024)
    criado_em = models.DateField("Criado Em", auto_now_add=True)
    
    def __str__(self):
        return self.nome

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