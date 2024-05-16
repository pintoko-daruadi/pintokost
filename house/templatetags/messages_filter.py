from django import template

register = template.Library()


@register.filter
def alert_bootstrap(value):
    if value == "error":
        return "danger"
    return value
