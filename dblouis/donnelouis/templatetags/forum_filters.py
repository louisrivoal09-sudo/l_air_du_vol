from django import template

register = template.Library()

@register.filter
def split(value, separator):
    """Divise une chaîne par un séparateur"""
    if not value:
        return []
    return value.split(separator)
