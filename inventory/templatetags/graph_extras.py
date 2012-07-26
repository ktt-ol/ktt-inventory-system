from django import template
from django.template.defaultfilters import stringfilter
register = template.Library()

@register.filter(name='graphescape')
@stringfilter
def graphescape(value):
    return value.replace('"', '\\"')
