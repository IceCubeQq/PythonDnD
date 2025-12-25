from django.db import models

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

class Spell(models.Model):
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

class Equipment(models.Model):
    CURRENCY_UNITS = [
        ('cp', 'Медные'),
        ('sp', 'Серебряные'),
        ('ep', 'Электрумовые'),
        ('gp', 'Золотые'),
        ('pp', 'Платиновые'),
    ]

    name = models.CharField("Название", max_length=50)
    weight = models.IntegerField("Вес")
    cost_quantity = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    cost_unit = models.CharField(max_length=2, choices=CURRENCY_UNITS, default='gp', blank=True)

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

    class Meta:
        unique_together = ['monster', 'movement_type']

    def __str__(self):
        return f"{self.movement_type}: {self.value}"


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



