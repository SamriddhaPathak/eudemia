from django import template
import math

register = template.Library()

@register.filter
def index(indexable, i):
    return indexable[i]

@register.filter
def div(value, arg):
    try:
        return int(value) / int(arg)
    except (ValueError, ZeroDivisionError):
        return None

@register.filter
def mult(value, arg):
    return float(value) * float(arg)

@register.filter
def floor(value):
    return math.floor(float(value))

@register.filter
def get_decimal(value):
    return float(value) % 1

@register.filter
def to_feet(value):
    return str(floor(float(value))) + " ft " + str(round(get_decimal(value) * 12.0)) + " in"