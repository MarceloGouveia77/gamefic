from django.contrib import admin
from core.models import Aluno, AlunosAtividade, AlunosTurma, Atividade, Professor, ProfessoresTurma, Turma

# Register your models here.

admin.site.register(Professor)
admin.site.register(Aluno)
admin.site.register(Turma)
admin.site.register(ProfessoresTurma)
admin.site.register(AlunosTurma)
admin.site.register(Atividade)
admin.site.register(AlunosAtividade)