from django import template

register = template.Library()


@register.filter(name='ID')
def ID(value: dict):
    return value.get("_id")
