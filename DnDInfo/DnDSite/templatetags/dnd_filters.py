from django import template
from urllib.parse import urlencode

from django.utils.html import format_html

from ..constants import *
from ..models import Speed, Favorite, Monster

register = template.Library()
@register.filter
def get_field(form, field_name):
    return form.get(field_name)

@register.filter
def get_field_id(form, field_name):
    field = form.get(field_name)
    return field.auto_id if field else ''

@register.filter
def split(value, delimiter=' '):
    if not value:
        return []
    return str(value).split(delimiter)

@register.filter
def calculate_modifier(score):
    return (int(score) - 10) // 2

@register.filter
def modifier_with_sign(score):
    modifier = (int(score) - 10) // 2
    return f"+{modifier}" if modifier >= 0 else str(modifier)

@register.filter
def spell_level_display(level):
    return "Заговор" if level == 0 else f"{level} ур."

@register.filter
def cost_display(equipment):
    if not equipment.cost_quantity:
        return "Бесплатно"
    return f"{equipment.cost_quantity} {equipment.get_cost_unit_display()}"

@register.filter
def truncate_description(text, length=100):
    if not text:
        return ""
    if len(text) <= length:
        return text
    return text[:length] + "..."

@register.filter
def is_favorite(user, obj):
    if not user.is_authenticated:
        return False
    content_type = obj.__class__.__name__.lower()
    return Favorite.objects.filter(
        user=user,
        content_type=content_type,
        object_id=obj.id
    ).exists()

@register.filter
def get_size_display(size):
    return SIZES.get(size, size)

@register.filter
def get_armor_type_display(armor_type):
    return ARMOR_TYPE_DISPLAY.get(armor_type, armor_type)

@register.filter
def get_difficulty(hp):
    hp = int(hp) if hp else 0
    if hp < 50:
        return "Легко"
    elif hp < 100:
        return "Средне"
    elif hp < 200:
        return "Сложно"
    else:
        return "Очень сложно"

@register.filter
def get_estimated_level(hp):
    hp = int(hp) if hp else 0
    if hp < 30:
        return "1-3"
    elif hp < 60:
        return "4-6"
    elif hp < 100:
        return "7-9"
    elif hp < 150:
        return "10-12"
    elif hp < 200:
        return "13-15"
    else:
        return "16+"

@register.filter
def get_estimated_xp(hp):
    hp = int(hp) if hp else 0
    if hp < 30:
        return "~100 XP"
    elif hp < 60:
        return "~200 XP"
    elif hp < 100:
        return "~450 XP"
    elif hp < 150:
        return "~700 XP"
    elif hp < 200:
        return "~1100 XP"
    else:
        return "~1800 XP"


@register.simple_tag
def build_pagination_url(request, page_number=None):
    params = {}
    for key in request.GET:
        if key != 'page' and request.GET.get(key):
            params[key] = request.GET.get(key)
    if page_number:
        params['page'] = page_number
    if params:
        return "?" + urlencode(params)
    return "?"


@register.simple_tag
def build_spell_pagination_url(request, page_number=None, **kwargs):
    params = {}
    for key in ['search', 'level', 'school', 'sort', 'show_homebrew']:
        value = request.GET.get(key, '')
        if value:
            params[key] = value
    for key, value in kwargs.items():
        if value is not None and value != '':
            params[key] = value
    if page_number:
        params['page'] = page_number
    if params:
        return "?" + urlencode(params)
    return "?"


@register.filter
def spell_level_badge_html(spell):
    LEVEL_COLORS = {
        0: 'bg-secondary',
        1: 'bg-primary',
        2: 'bg-success',
        3: 'bg-warning text-dark',
        4: 'bg-danger',
        5: 'bg-info',
        6: 'bg-dark',
        7: 'bg-secondary',
        8: 'bg-secondary',
        9: 'bg-secondary'
    }

    level_text = "Заговор" if spell.level == 0 else f"{spell.level} ур."
    badge_class = LEVEL_COLORS.get(spell.level, 'bg-secondary')

    return format_html(
        '<span class="badge {}">{}</span>',
        badge_class,
        level_text
    )


@register.filter
def equipment_short_info(equipment):
    parts = []

    if equipment.weight:
        parts.append(f"Вес: {equipment.weight} фн.")

    if equipment.cost_quantity:
        parts.append(f"Цена: {equipment.cost_quantity} {equipment.get_cost_unit_display()}")

    return " | ".join(parts) if parts else "Базовый предмет"


@register.filter
def equipment_short_info_html(equipment):
    info = equipment | equipment_short_info
    return format_html('<small class="text-muted">{}</small>', info)


@register.filter
def cost_display(equipment):
    if not equipment.cost_quantity:
        return "Бесплатно"
    cost = equipment.cost_quantity
    if cost == int(cost):
        cost = int(cost)

    return f"{cost} {equipment.get_cost_unit_display()}"


@register.filter
def weight_display(equipment):
    if not equipment.weight:
        return "Не указан"
    if equipment.weight == 1:
        return "1 фунт"
    elif equipment.weight < 5:
        return f"{equipment.weight} фунта"
    else:
        return f"{equipment.weight} фунтов"


@register.filter
def cost_with_currency(equipment, show_full_name=False):
    if not equipment.cost_quantity:
        return "Бесплатно"

    cost = equipment.cost_quantity
    if cost == int(cost):
        cost = int(cost)

    if show_full_name:
        currency_names = {
            'cp': 'медных монет',
            'sp': 'серебряных монет',
            'ep': 'электрумовых монет',
            'gp': 'золотых монет',
            'pp': 'платиновых монет'
        }
        currency = currency_names.get(equipment.cost_unit, equipment.cost_unit)
    else:
        currency = equipment.get_cost_unit_display()

    return f"{cost} {currency}"


@register.filter
def movement_display(movement_type):
    MOVEMENT_TYPES = {
        'walk': 'Ходьба',
        'fly': 'Полёт',
        'swim': 'Плавание',
        'climb': 'Лазание',
        'burrow': 'Рытьё',
        'dig': 'Копая',
        'hover': 'Парение',
        'other': 'Другое',
    }
    key = str(movement_type).lower().strip()
    return MOVEMENT_TYPES.get(key, str(movement_type).title())


@register.filter
def speed_display(speed):
    movement = speed.movement_type | movement_display
    return f"{movement}: {speed.value}"


@register.filter
def movement_with_icon(movement_type):
    MOVEMENT_ICONS = {
        'walk': 'bi-person-walking',
        'fly': 'bi-cloud',
        'swim': 'bi-droplet',
        'climb': 'bi-arrow-up-right',
        'burrow': 'bi-shovel',
        'dig': 'bi-shovel-fill',
        'hover': 'bi-wind',
        'other': 'bi-three-dots',
    }

    key = str(movement_type).lower().strip()
    icon_class = MOVEMENT_ICONS.get(key, 'bi-question-circle')
    display_name = movement_type | movement_display

    return format_html(
        '<i class="bi {} me-1"></i>{}',
        icon_class,
        display_name
    )

@register.filter
def get_movement_display(movement_type):
    movement_map = {
        'walk': 'Ходьба',
        'fly': 'Полёт',
        'swim': 'Плавание',
        'climb': 'Лазание',
        'burrow': 'Рытьё',
        'dig': 'Копая',
        'hover': 'Парение',
    }
    return movement_map.get(str(movement_type).lower(), str(movement_type).title())