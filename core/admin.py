from django.contrib import admin
from core.models import Aluno, AlunosTurma, Professor, ProfessoresTurma, Turma

# Register your models here.

admin.site.register(Professor)
admin.site.register(Aluno)
admin.site.register(Turma)
admin.site.register(ProfessoresTurma)
admin.site.register(AlunosTurma)