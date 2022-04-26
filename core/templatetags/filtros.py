from django import template

register = template.Library()

@register.filter(name='verificar_grupo')
def verificar_grupo(usuario, grupo):
    if grupo == "Alunos":
        return True
    return False