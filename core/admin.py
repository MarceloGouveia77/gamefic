from django.contrib import admin
from core.models import Aluno, Professor

# Register your models here.

admin.site.register(Professor)
admin.site.register(Aluno)