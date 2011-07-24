from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
@stringfilter
def phone(value):
  return value[:3] + "-" + value[3:6] + "-" + value[6:]
