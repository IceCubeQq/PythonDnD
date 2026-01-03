from django import template

register = template.Library()

@register.filter
def get_movement_display(value):
    movement_map = {
        'walk': 'Ходьба',
        'fly': 'Полёт',
        'swim': 'Плавание',
        'climb': 'Лазание',
        'burrow': 'Рытьё',
        'dig': 'Капая',
        'hover': 'Парение',
        'other': 'Другое',
    }
    return movement_map.get(str(value).lower(), str(value).title())

@register.filter
def split(value, delimiter=' '):
    return value.split(delimiter)