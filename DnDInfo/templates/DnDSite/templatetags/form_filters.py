from django import template

register = template.Library()

@register.filter
def get_field(form, field_name):
    return form[field_name]

@register.filter
def get_field_id(form, field_name):
    return form[field_name].auto_id

@register.filter
def split(value, delimiter=' '):
    return value.split(delimiter)