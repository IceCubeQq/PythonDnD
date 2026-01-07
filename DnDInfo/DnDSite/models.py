from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from .constants import *


class Monster(models.Model):
    name = models.CharField("Название", max_length=50)
    size = models.TextField("Размер")
    type = models.TextField("Тип")
    hit_points = models.IntegerField("Уровни жизней")
    strength = models.IntegerField("Сила")
    dexterity = models.IntegerField("Ловкость")
    constitution = models.IntegerField("Телосложение")
    intelligence = models.IntegerField("Интеллект")
    wisdom = models.IntegerField("Мудрость")
    charisma = models.IntegerField("Харизма")
    is_homebrew = models.BooleanField("Homebrew", default=False)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Автор")
    created_at = models.DateTimeField("Создан", auto_now_add=True)
    is_approved = models.BooleanField("Одобрено", default=False)

    class Meta:
        ordering = ['is_homebrew', 'name']
        verbose_name = 'Монстр'
        verbose_name_plural = 'Монстры'

    def __str__(self):
        prefix = "[Homebrew] " if self.is_homebrew else ""
        return f"{prefix}{self.name}"

class Spell(models.Model):
    LEVEL_COLORS = LEVEL_COLORS

    @property
    def is_cantrip(self):
        return self.level == 0

    SCHOOL_CHOICES = SCHOOLS

    name = models.CharField("Название", max_length=50)
    desc = models.TextField("Описание")
    spell_range  = models.TextField("Дальность")
    duration = models.TextField("Продолжительность")
    casting_time = models.TextField("Время накладывания")
    level = models.IntegerField("Уровень")
    school = models.CharField(max_length=20, choices=SCHOOL_CHOICES, verbose_name='Школа магии')
    ritual = models.BooleanField("Ритуал", default=False)
    concentration = models.BooleanField("Концентрация", default=False)
    is_homebrew = models.BooleanField("Homebrew", default=False)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Автор")
    created_at = models.DateTimeField("Создан", auto_now_add=True)
    is_approved = models.BooleanField("Одобрено", default=False)

    class Meta:
        ordering = ['is_homebrew', 'level', 'name']
        verbose_name = 'Заклинание'
        verbose_name_plural = 'Заклинания'

class Equipment(models.Model):
    def get_short_info_html(self):
        info = self.get_short_info()
        return mark_safe(f'<small class="text-muted">{info}</small>')

    CURRENCY_UNITS = CURRENCY_UNITS

    name = models.CharField("Название", max_length=50)
    description = models.TextField("Описание", blank=True, null=True)
    weight = models.IntegerField("Вес")
    cost_quantity = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    cost_unit = models.CharField(max_length=2, choices=CURRENCY_UNITS, default='gp', blank=True)
    is_homebrew = models.BooleanField("Homebrew", default=False)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Автор")
    created_at = models.DateTimeField("Создан", auto_now_add=True)
    is_approved = models.BooleanField("Одобрено", default=False)

    class Meta:
        ordering = ['is_homebrew', 'name']
        verbose_name = 'Снаряжение'
        verbose_name_plural = 'Снаряжение'

    def __str__(self):
        prefix = "[Homebrew] " if self.is_homebrew else ""
        return f"{prefix}{self.name}"



class Armor_class(models.Model):
    ARMOR_TYPES = ARMOR_TYPES
    monster = models.ForeignKey('Monster', on_delete=models.CASCADE,
        related_name='armor_classes',
        verbose_name='Монстр'
    )
    type = models.CharField(max_length=20,choices=ARMOR_TYPES,default='natural',verbose_name='Тип брони')
    value = models.IntegerField("Значение")

    class Meta:
        verbose_name = 'Класс брони'
        verbose_name_plural = 'Классы брони'
        ordering = ['-value']

    def __str__(self):
        return f"{self.value} ({self.get_type_display()})"


class Speed(models.Model):
    monster = models.ForeignKey('Monster', on_delete=models.CASCADE, related_name='speeds')
    movement_type = models.CharField("Тип", max_length=20)
    value = models.CharField("Значение", max_length=20)

    MOVEMENT_MAP = MOVEMENT_TYPES

    def __str__(self):
        return f"{self.get_display_name()}: {self.value}"


class Component(models.Model):
    COMPONENT_TYPES = [
        ('V', 'Вербальный'),
        ('S', 'Соматический'),
        ('M', 'Материальный'),
    ]
    spell = models.ForeignKey('Spell', on_delete=models.CASCADE, related_name='components')
    type = models.CharField(max_length=1, choices=COMPONENT_TYPES)

    class Meta:
        unique_together = ['spell', 'type']

    def __str__(self):
        return self.get_type_display()


class Favorite(models.Model):
    CONTENT_TYPES = [
        ('monster', 'Монстр'),
        ('spell', 'Заклинание'),
        ('equipment', 'Снаряжение'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites', verbose_name="Пользователь")
    content_type = models.CharField(max_length=20, choices=CONTENT_TYPES, verbose_name="Тип контента")
    object_id = models.PositiveIntegerField(verbose_name="ID объекта")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'
        unique_together = ['user', 'content_type', 'object_id']
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.get_content_type_display()} #{self.object_id}"