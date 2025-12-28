from django.contrib import admin
from .models import Monster, Spell, Equipment,Armor_class, Speed, Component


@admin.register(Monster)
class MonsterAdmin(admin.ModelAdmin):
    list_display = ('name', 'size', 'type', 'hit_points', 'strength', 'is_homebrew', 'is_approved', 'created_by',
                    'created_at')
    list_filter = ('size', 'type', 'is_homebrew', 'is_approved')
    search_fields = ('name', 'type')
    ordering = ('-is_homebrew', 'name')
    list_editable = ('is_approved',)
    actions = ['approve_monsters', 'reject_monsters']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(is_homebrew=True)

    def approve_monsters(self, request, queryset):
        queryset.update(is_approved=True)
        self.message_user(request, f"{queryset.count()} монстров одобрено.")

    approve_monsters.short_description = "Одобрить выбранных монстров"

    def reject_monsters(self, request, queryset):
        count = queryset.count()
        queryset.delete()
        self.message_user(request, f"{count} монстров отклонено.")

    reject_monsters.short_description = "Отклонить выбранных монстров"


@admin.register(Spell)
class SpellAdmin(admin.ModelAdmin):
    list_display = ('name', 'level', 'school', 'ritual', 'concentration', 'is_homebrew', 'is_approved', 'created_by',
                    'created_at')
    list_filter = ('level', 'school', 'ritual', 'concentration', 'is_homebrew', 'is_approved')
    search_fields = ('name', 'desc')
    ordering = ('-is_homebrew', 'name')
    list_editable = ('is_approved',)
    actions = ['approve_spells', 'reject_spells']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(is_homebrew=True)

    def approve_spells(self, request, queryset):
        queryset.update(is_approved=True)
        self.message_user(request, f"{queryset.count()} заклинаний одобрено.")

    approve_spells.short_description = "Одобрить выбранные заклинания"

    def reject_spells(self, request, queryset):
        count = queryset.count()
        queryset.delete()
        self.message_user(request, f"{count} заклинаний отклонено.")

    reject_spells.short_description = "Отклонить выбранные заклинания"


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'weight', 'cost_quantity', 'cost_unit', 'is_homebrew', 'is_approved', 'created_by',
                    'created_at')
    search_fields = ('name',)
    list_filter = ('cost_unit', 'is_homebrew', 'is_approved')
    list_editable = ('is_approved',)
    actions = ['approve_equipment', 'reject_equipment']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(is_homebrew=True)

    def approve_equipment(self, request, queryset):
        queryset.update(is_approved=True)
        self.message_user(request, f"{queryset.count()} предметов снаряжения одобрено")

    approve_equipment.short_description = "Одобрить выбранное снаряжение"

    def reject_equipment(self, request, queryset):
        count = queryset.count()
        queryset.delete()
        self.message_user(request, f"{count} предметов снаряжения отклонено")

    reject_equipment.short_description = "Отклонить выбранное снаряжение"

admin.site.register(Armor_class)
admin.site.register(Speed)
admin.site.register(Component)