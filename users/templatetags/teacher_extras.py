from django import template

register = template.Library()

@register.filter
def label(value):
    if value == 'M':
        return 'Matematik'
    if value == 'S':
        return 'Sosyal'
    if value == 'F':
        return 'Fen'
    if value == 'T':
        return 'Turkce'
    else:
        return 'Brans yok'