from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
@stringfilter
def norm(value):
    """Removes all values of _ from the given string"""
    return value.replace("_", " ")



