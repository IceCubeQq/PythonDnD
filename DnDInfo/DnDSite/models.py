from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.html import format_html
from django.utils.safestring import mark_safe


class Monster(models.Model):
    def get_similar_monsters(self, limit=5):
        from django.db.models import Q
        similar = Monster.objects.filter(
            Q(type__icontains=self.type) | Q(size=self.size)
        ).exclude(id=self.id)
        return similar.order_by(
            '-type',
            'hit_points'
        )[:limit]

    def get_absolute_url(self):
        return reverse('monster_detail', args=[str(self.id)])

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
    LEVEL_COLORS = {
        0: 'bg-secondary',
        1: 'bg-primary',
        2: 'bg-success',
        3: 'bg-warning',
        4: 'bg-danger',
        5: 'bg-info',
        6: 'bg-dark',
        7: 'bg-secondary',
        8: 'bg-secondary',
        9: 'bg-secondary'
    }

    def get_level_display(self):
        if self.level == 0:
            return "Заговор"
        return f"{self.level} ур."

    def get_level_badge_class(self):
        return self.LEVEL_COLORS.get(self.level, 'bg-secondary')

    def get_level_badge_html(self):
        level_text = self.get_level_display()
        badge_class = self.get_level_badge_class()

        extra_class = "text-dark" if self.level == 3 else ""
        full_class = f"{badge_class} {extra_class}".strip()

        return format_html(
            '<span class="badge {}">{}</span>',
            full_class,
            level_text
        )

    @property
    def is_cantrip(self):
        return self.level == 0

    def get_absolute_url(self):
        return reverse('spell_detail', args=[str(self.id)])

    SCHOOL_CHOICES = [
        ('abjuration', 'Ограждение'),
        ('conjuration', 'Вызов'),
        ('divination', 'Прорицание'),
        ('enchantment', 'Очарование'),
        ('evocation', 'Воплощение'),
        ('illusion', 'Иллюзия'),
        ('necromancy', 'Некромантия'),
        ('transmutation', 'Преобразование')
    ]

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
    def get_short_info(self):
        parts = []

        if self.weight:
            parts.append(f"Вес: {self.weight} фн.")

        if self.cost_quantity:
            parts.append(f"Цена: {self.cost_quantity} {self.get_cost_unit_display()}")

        if not parts:
            return "Базовый предмет"

        return " | ".join(parts)

    def get_short_info_html(self):
        info = self.get_short_info()
        return mark_safe(f'<small class="text-muted">{info}</small>')

    def get_similar_equipment(self, limit=5):
        from django.db.models import Q
        similar = Equipment.objects.filter(
            Q(name__icontains=self.name.split()[0]) |
            Q(description__icontains=self.name.split()[0])
        ).exclude(id=self.id)  # исключаем текущий предмет
        if self.description:
            keywords = self.description.split()[:10]
            for keyword in keywords:
                if len(keyword) > 3:
                    similar = similar | Equipment.objects.filter(
                        Q(description__icontains=keyword) |
                        Q(name__icontains=keyword)
                    ).exclude(id=self.id)
        return similar.distinct()[:limit]

    def get_absolute_url(self):
        return reverse('equipment_detail', args=[str(self.id)])

    CURRENCY_UNITS = [
        ('cp', 'Медные'),
        ('sp', 'Серебряные'),
        ('ep', 'Электрумовые'),
        ('gp', 'Золотые'),
        ('pp', 'Платиновые'),
    ]

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

    def get_cost_display(self):
        if self.cost_quantity:
            return f"{self.cost_quantity} {self.get_cost_unit_display()}"
        return "Бесплатно"

    def get_weight_display(self):
        if self.weight:
            return f"{self.weight} фунтов"
        return "Не указан"

class Armor_class(models.Model):
    ARMOR_TYPES = [
        ('natural', 'Природная броня'),
        ('armor', 'Доспехи'),
        ('magic', 'Магическая защита'),
        ('dex', 'Ловкость'),
        ('other', 'Другое'),
    ]
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

    def get_display_name(self):
        movement_map = {
            'walk': 'Ходьба',
            'fly': 'Полёт',
            'swim': 'Плавание',
            'climb': 'Лазание',
            'burrow': 'Рытьё',
            'dig': 'Копая',
            'hover': 'Парение',
            'other': 'Другое',
        }
        return movement_map.get(self.movement_type.lower(), self.movement_type.title())

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

    def get_object(self):
        if self.content_type == 'monster':
            return Monster.objects.filter(id=self.object_id).first()
        elif self.content_type == 'spell':
            return Spell.objects.filter(id=self.object_id).first()
        elif self.content_type == 'equipment':
            return Equipment.objects.filter(id=self.object_id).first()
        return None

    def get_object_name(self):
        obj = self.get_object()
        return obj.name if obj else f"Объект #{self.object_id}"

    def get_object_url(self):
        if self.content_type == 'monster':
            return f"/monsters/{self.object_id}/"
        elif self.content_type == 'spell':
            return f"/spells/{self.object_id}/"
        elif self.content_type == 'equipment':
            return f"/equipment/{self.object_id}/"
        return "#"