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

SIZE_CHOICES = [
    ('', 'Выберите размер'),
    ('Tiny', 'Крошечный'),
    ('Small', 'Маленький'),
    ('Medium', 'Средний'),
    ('Large', 'Большой'),
    ('Huge', 'Огромный'),
    ('Gargantuan', 'Гигантский'),
]

SPEED_TYPES = [
    ('walk', 'Ходьба'),
    ('fly', 'Полёт'),
    ('swim', 'Плавание'),
    ('climb', 'Лазание'),
    ('burrow', 'Рытьё'),
    ('dig', 'Капая'),
    ('hover', 'Парение'),
    ('other', 'Другое'),
]

SPEED_EXAMPLES = {
    'walk': 'Ходьба: 30 футов',
    'fly': 'Полёт: 30 футов',
    'swim': 'Плавание: 20 футов',
    'climb': 'Лазание: 30 футов',
    'burrow': 'Рытьё: 10 футов',
    'dig': 'Капая: 10 футов',
    'hover': 'Парение (не требует перемещения)',
}

SIZES = {
    'Tiny': 'Крошечный',
    'Small': 'Маленький',
    'Medium': 'Средний',
    'Large': 'Большой',
    'Huge': 'Огромный',
    'Gargantuan': 'Гигантский',
}

SIZE_OPTIONS = [
        ('Tiny', 'Крошечный'),
        ('Small', 'Маленький'),
        ('Medium', 'Средний'),
        ('Large', 'Большой'),
        ('Huge', 'Огромный'),
        ('Gargantuan', 'Гигантский'),
    ]

SCHOOLS = {
    'abjuration': 'Ограждение',
    'conjuration': 'Вызов',
    'divination': 'Прорицание',
    'enchantment': 'Очарование',
    'evocation': 'Воплощение',
    'illusion': 'Иллюзия',
    'necromancy': 'Некромантия',
    'transmutation': 'Преобразование',
}

ARMOR_TYPES = [
        ('natural', 'Природная броня'),
        ('armor', 'Доспехи'),
        ('magic', 'Магическая защита'),
        ('dex', 'Ловкость'),
        ('other', 'Другое'),
]

ARMOR_TYPE_DISPLAY = {
    'natural': 'Природная броня',
    'armor': 'Доспехи',
    'magic': 'Магическая защита',
    'dex': 'Ловкость',
    'other': 'Другое',
}

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

CURRENCY_UNITS = [
        ('cp', 'Медные (cp)'),
        ('sp', 'Серебряные (sp)'),
        ('gp', 'Золотые (gp)'),
        ('pp', 'Платиновые (pp)'),
    ]

WEIGHT_OPTIONS = [
        ('light', 'Легкие (< 5 фунт.)'),
        ('medium', 'Средние (5-15 фунт.)'),
        ('heavy', 'Тяжелые (> 15 фунт.)'),
    ]

COMPONENT_TYPES = [
        ('V', 'Вербальный'),
        ('S', 'Соматический'),
        ('M', 'Материальный'),
]

CONTENT_TYPES = [
        ('monster', 'Монстр'),
        ('spell', 'Заклинание'),
        ('equipment', 'Снаряжение'),
]

SORT_OPTIONS_EQUIPMENTS = [
        ('name', 'По названию'),
        ('weight_asc', 'Вес ↑'),
        ('weight_desc', 'Вес ↓'),
        ('price_asc', 'Цена ↑'),
        ('price_desc', 'Цена ↓'),
    ]

SCHOOL_MAPPING = {
        'abjuration': 'abjuration',
        'conjuration': 'conjuration',
        'divination': 'divination',
        'enchantment': 'enchantment',
        'evocation': 'evocation',
        'illusion': 'illusion',
        'necromancy': 'necromancy',
        'transmutation': 'transmutation'
}

SCHOOL_CHOICES_LIST = [
    ('abjuration', 'Ограждение'),
    ('conjuration', 'Вызов'),
    ('divination', 'Прорицание'),
    ('enchantment', 'Очарование'),
    ('evocation', 'Воплощение'),
    ('illusion', 'Иллюзия'),
    ('necromancy', 'Некромантия'),
    ('transmutation', 'Преобразование'),
]

SORT_OPTIONS_SPELLS = [
    ('name', 'По названию'),
    ('level', 'По уровню'),
    ('school', 'По школе'),
]

COMPONENT_MAPPING = {'V': 'V', 'S': 'S', 'M': 'M'}

MONSTER_TYPES = {
        'dragon': 'Дракон',
        'undead': 'Нежить',
        'humanoid': 'Гуманоид',
        'beast': 'Зверь',
        'elemental': 'Элементаль',
        'fiend': 'Исчадие',
        'celestial': 'Небожитель',
        'aberration': 'Аберрация',
        'construct': 'Конструкт',
        'plant': 'Растение',
        'monstrosity': 'Чудовище',
        'ooze': 'Слизь',
        'fey': 'Фея',
        'giant': 'Великан'
    }

TYPE_OPTIONS = [
            ('dragon', 'Дракон'),
            ('undead', 'Нежить'),
            ('humanoid', 'Гуманоид'),
            ('beast', 'Зверь'),
            ('elemental', 'Элементаль'),
            ('fiend', 'Исчадие'),
            ('celestial', 'Небожитель'),
            ('aberration', 'Аберрация'),
            ('construct', 'Конструкт'),
            ('plant', 'Растение'),
            ('monstrosity', 'Чудовище'),
            ('ooze', 'Слизь'),
            ('fey', 'Фея'),
            ('giant', 'Великан'),
        ]

SORT_OPTIONS = [
        ('name', 'По названию'),
        ('hit_points', 'По здоровью'),
        ('strength', 'По силе'),
        ('dexterity', 'По ловкости'),
        ('constitution', 'По телосложению'),
        ('intelligence', 'По интеллекту'),
        ('wisdom', 'По мудрости'),
        ('charisma', 'По харизме'),
    ]

SPECIAL_CASES = {
        'antipathy/sympathy': 'antipathy-sympathy',
        'mordenkainen\'s sword': 'mordenkainens-sword',
        'mordenkainen\'s faithful hound': 'mordenkainens-faithful-hound',
        'mordenkainen\'s private sanctum': 'mordenkainens-private-sanctum',
        'mordenkainen\'s magnificent mansion': 'mordenkainens-magnificent-mansion',
        'tasha\'s hideous laughter': 'tashas-hideous-laughter',
        'tasha\'s otherworldly guise': 'tashas-otherworldly-guise',
        'tasha\'s mind whip': 'tashas-mind-whip',
        'tasha\'s caustic brew': 'tashas-caustic-brew',
        'otiluke\'s resilient sphere': 'otilukes-resilient-sphere',
        'otiluke\'s freezing sphere': 'otilukes-freezing-sphere',
        'leomund\'s tiny hut': 'leomunds-tiny-hut',
        'leomund\'s secret chest': 'leomunds-secret-chest',
        'leomund\'s trap': 'leomunds-trap',
        'melf\'s acid arrow': 'melfs-acid-arrow',
        'bigby\'s hand': 'bigbys-hand',
        'drawmij\'s instant summons': 'drawmijs-instant-summons',
        'nystul\'s magic aura': 'nystuls-magic-aura',
        'ruh\'s hidden path': 'ruhs-hidden-path',
        'arzah\'s black book': 'arzahs-black-book',
}