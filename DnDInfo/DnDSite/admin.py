from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import Component, Favorite, Speed, Armor_class, Equipment, Spell, Monster


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'content_type', 'object_id', 'created_at')
    list_filter = ('content_type', 'created_at')
    search_fields = ('user__username', 'object_id')
    ordering = ('-created_at',)


@admin.register(Monster)
class MonsterAdmin(admin.ModelAdmin):
    list_display = ('name', 'size', 'type', 'hit_points',
                    'is_homebrew', 'is_approved', 'created_by', 'created_at')
    list_filter = ('is_homebrew', 'is_approved', 'size', 'type')
    search_fields = ('name', 'type', 'created_by__username')
    ordering = ('-is_homebrew', '-created_at', 'name')


@admin.register(Spell)
class SpellAdmin(admin.ModelAdmin):
    list_display = ('name', 'level', 'school', 'ritual', 'concentration', 'is_homebrew', 'is_approved', 'created_by', 'created_at')
    list_filter = ('is_homebrew', 'is_approved', 'level', 'school', 'ritual', 'concentration')
    search_fields = ('name', 'desc', 'created_by__username')
    ordering = ('-is_homebrew', '-created_at', 'name')

    def level(self, obj):
        return f"{obj.level} ур." if obj.level > 0 else "Заговор"

    level.short_description = 'Уровень'

    def school(self, obj):
        return obj.get_school_display()

    school.short_description = 'Школа'


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'weight', 'cost_display', 'is_homebrew',
                    'is_approved', 'created_by', 'created_at')
    list_filter = ('is_homebrew', 'is_approved', 'cost_unit')
    search_fields = ('name', 'description', 'created_by__username')
    ordering = ('-is_homebrew', '-created_at', 'name')

    def cost_display(self, obj):
        if obj.cost_quantity:
            return f"{obj.cost_quantity} {obj.get_cost_unit_display()}"
        return "Бесплатно"

    cost_display.short_description = "Стоимость"


@admin.register(Armor_class)
class ArmorClassAdmin(admin.ModelAdmin):
    list_display = ('monster', 'type', 'value')
    list_filter = ('type',)
    search_fields = ('monster__name',)
    ordering = ('-value',)

    def type(self, obj):
        return obj.get_type_display()

    type.short_description = 'Тип брони'


@admin.register(Speed)
class SpeedAdmin(admin.ModelAdmin):
    list_display = ('monster', 'movement_type', 'value')
    list_filter = ('movement_type',)
    search_fields = ('monster__name', 'movement_type')
    ordering = ('monster',)

    def movement_type(self, obj):
        return obj.movement_type

    movement_type.short_description = 'Тип передвижения'


@admin.register(Component)
class ComponentAdmin(admin.ModelAdmin):
    list_display = ('spell_link', 'get_type_display')
    list_filter = ('type',)
    search_fields = ('spell__name',)
    ordering = ('spell__name',)

    def spell_link(self, obj):
        url = reverse('admin:DnDSite_spell_change', args=[obj.spell.id])
        return format_html('<a href="{}">{}</a>', url, obj.spell.name)

    spell_link.short_description = 'Заклинание'
    spell_link.admin_order_field = 'spell__name'

    def get_type_display(self, obj):
        return obj.get_type_display()

    get_type_display.short_description = 'Тип компонента'

admin.site.register(Favorite, FavoriteAdmin)