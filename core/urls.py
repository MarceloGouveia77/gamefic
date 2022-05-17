from django.urls import path
from core import views

app_name = 'core'

urlpatterns = [
    path('', views.index, name='index'),
    path('alunos/', views.alunos, name='alunos'),
    path('alunos/alterar_nota/', views.alterar_nota, name='alterar_nota'),
    path('cadastrar/', views.cadastrar_aluno, name='cadastrar_aluno'),
    path('pontuacoes/', views.pontuacoes, name='pontuacoes'),
    path('sugestao/', views.sugestao, name='sugestao'),
    path('turmas/', views.turmas, name='turmas'),
    path('atividades/nova/', views.cadastrar_atividade, name='cadastrar_atividade'),
    path('turma/<int:pk>/', views.detalhe_turma, name='detalhe_turma'),
    path('turmas/gerar_link/<int:pk>/', views.gerar_link_tuma, name='gerar_link_tuma'),
    path('turmas/entrar/<str:hash>/', views.entrar_turma, name='entrar_turma'),
    path('turmas/cadastrar/', views.cadastrar_turma, name='cadastrar_turma'),
    path('logout/', views.logout_site, name='logout'),
    path('login/', views.login_sistema, name='login'),
    path('questionario/', views.questionario, name='questionario')
]