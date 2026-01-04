from django.contrib import admin
from .models import Monster, Spell, Equipment, Armor_class, Speed, Component, Favorite


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_content_type_display', 'get_object_name', 'created_at')
    list_filter = ('content_type', 'created_at')
    search_fields = ('user__username', 'object_id')
    ordering = ('-created_at',)

    def get_object_name(self, obj):
        return obj.get_object_name()

    get_object_name.short_description = 'Объект'

@admin.register(Monster)
class MonsterAdmin(admin.ModelAdmin):
    list_display = ('name', 'size', 'type', 'hit_points', 'strength', 'is_homebrew', 'is_approved', 'created_by',
                    'created_at')
    list_filter = ('size', 'type', 'is_homebrew', 'is_approved')
    search_fields = ('name', 'type', 'created_by__username')
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
    search_fields = ('name', 'desc', 'created_by__username')
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
    list_display = ('name', 'description_preview', 'weight', 'cost_quantity', 'cost_unit', 'is_homebrew',
                    'is_approved', 'created_by', 'created_at')
    ssearch_fields = ('name', 'description', 'created_by__username')
    list_filter = ('cost_unit', 'is_homebrew', 'is_approved')
    list_editable = ('is_approved',)
    actions = ['approve_equipment', 'reject_equipment']

    def description_preview(self, obj):
        if obj.description:
            return obj.description[:50] + '...' if len(obj.description) > 50 else obj.description
        return "—"

    description_preview.short_description = "Описание"

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

@admin.register(Armor_class)
class ArmorClassAdmin(admin.ModelAdmin):
    list_display = ('monster', 'type', 'value')
    list_filter = ('type',)
    search_fields = ('monster__name',)
    ordering = ('-value',)

@admin.register(Speed)
class SpeedAdmin(admin.ModelAdmin):
    list_display = ('monster', 'movement_type', 'value')
    list_filter = ('movement_type',)
    search_fields = ('monster__name', 'movement_type')
    ordering = ('monster',)

@admin.register(Component)
class ComponentAdmin(admin.ModelAdmin):
    list_display = ('spell', 'type')
    list_filter = ('type',)
    search_fields = ('spell__name',)
    ordering = ('spell',)