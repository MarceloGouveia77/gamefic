from django import forms
from core.models import Turma, Aluno

class TurmaForm(forms.ModelForm):
    
    class Meta:
        model = Turma
        exclude = ('hash_convite',)
        
class AlunoForm(forms.ModelForm):
    
    class Meta:
        model = Aluno
        exclude = ('tipo', 'pontuacao','usuario','confirmado',)