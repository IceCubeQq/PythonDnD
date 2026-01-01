from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


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