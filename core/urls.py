from django.urls import path
from core import views

app_name = 'core'

urlpatterns = [
    path('', views.index, name='index'),
    path('alunos/', views.alunos, name='alunos'),
    path('pontuacoes/', views.pontuacoes, name='pontuacoes'),
    path('sugestao/', views.sugestao, name='sugestao')
]