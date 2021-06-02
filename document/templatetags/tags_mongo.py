from django import template
from django.utils.safestring import mark_safe
from json import loads
register = template.Library()


@register.filter(name='ID')
def ID(value: dict):
    return value.get("_id")


@register.simple_tag(name='line_up')
def line_up(values: dict, schema: dict):
    if not isinstance(values, dict):
        print(type(dict))
        values = loads(values)
    if not isinstance(schema, dict):
        schema = loads(schema)
    rows = []
    result = ""
    for key in schema:
        if schema[key].get("position", 0) != 0:
            rows.append([key, schema[key]["position"]])
    if len(rows) == 0:
        for name, value in values.items():
            result += f"{name}: {value} <br>"
    else:
        rows.sort(key=lambda x: x[1], reverse=True)
        for name, position in rows:
            result += schema[name].get(
                "template",
                "{name}: {value} <br>",
            ).format(
                name=name,
                value=values.get(name, "?"),
            )
    return mark_safe(result)
