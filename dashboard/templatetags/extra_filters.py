from django import template
register = template.Library()
@register.filter
def attr(obj, name):
    return getattr(obj, name, '')

@register.filter
def is_list(value):
    return isinstance(value, (list, tuple))
