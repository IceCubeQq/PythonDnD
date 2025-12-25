from django.contrib import admin
from .models import (
    Monster, Spell, Equipment,
    Armor_class, Speed, Component
)

@admin.register(Monster)
class MonsterAdmin(admin.ModelAdmin):
    list_display = ('name', 'size', 'type', 'hit_points', 'strength')
    list_filter = ('size', 'type')
    search_fields = ('name', 'type')
    ordering = ('name',)

@admin.register(Spell)
class SpellAdmin(admin.ModelAdmin):
    list_display = ('name', 'level', 'school', 'ritual', 'concentration')
    list_filter = ('level', 'school', 'ritual', 'concentration')
    search_fields = ('name', 'desc')
    ordering = ('name',)

@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'weight', 'cost_quantity', 'cost_unit')
    search_fields = ('name',)
    list_filter = ('cost_unit',)

admin.site.register(Armor_class)
admin.site.register(Speed)
admin.site.register(Component)