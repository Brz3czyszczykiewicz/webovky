from django import template
register = template.Library()

@register.filter
def none(value):
    convert_to_str = str(value)
    if convert_to_str == "None":
        return "-"
    else:
        pass
    return value