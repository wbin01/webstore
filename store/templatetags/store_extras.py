# https://docs.djangoproject.com/pt-br/4.1/howto/custom-template-tags/
from django import template

register = template.Library()


@register.filter(name='cut')
def cut(value, arg):
    """Removes all values of arg from the given string

    Ex:
    {{ somevariable|cut:"0" }}
    """
    return value.replace(arg, '')


# Se deixar de passar o argumento name, como no segundo exemplo acima, o
# Django irá usar o nome da função como nome do filtro.
@register.filter
def lower(value):
    return value.lower()


@register.filter(is_safe=True)
def space_to_nbsp(value):
    """Replace all values of arg from the given string"""
    return value.replace(' ', '&nbsp;')


# Registrar sem decorador abaixo
# register.filter('cut', cut)
# register.filter('space_to_nbsp', space_to_nbsp)
