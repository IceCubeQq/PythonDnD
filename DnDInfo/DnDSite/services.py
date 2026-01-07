from django.db.models import Q
from django.urls import reverse

from .models import Monster, Equipment, Spell


class MonsterService:
    @staticmethod
    def get_similar_monsters(monster, limit=5):
        similar = Monster.objects.filter(
            Q(type__icontains=monster.type) | Q(size=monster.size)
        ).exclude(id=monster.id)
        return similar.order_by('-type', 'hit_points')[:limit]

    @staticmethod
    def get_absolute_url(monster):
        return reverse('monster_detail', args=[str(monster.id)])


class SpellService:
    @staticmethod
    def get_level_display(spell):
        return "Заговор" if spell.level == 0 else f"{spell.level} ур."

    @staticmethod
    def get_level_badge_class(spell):
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
        return LEVEL_COLORS.get(spell.level, 'bg-secondary')

    @staticmethod
    def get_absolute_url(spell):
        return reverse('spell_detail', args=[str(spell.id)])

    @staticmethod
    def get_similar_spells(spell, limit=5):
        queries = Q()
        queries |= Q(level=spell.level)
        queries |= Q(school=spell.school)
        name_words = [word for word in spell.name.split() if len(word) > 2]
        for word in name_words[:3]:
            queries |= Q(name__icontains=word)
            queries |= Q(desc__icontains=word)

        if spell.desc:
            effect_keywords = [
                'урон', 'лечение', 'щит', 'невидимость', 'полёт',
                'телепортация', 'огонь', 'лёд', 'молния', 'кислота',
                'яд', 'психический', 'сила', 'ловкость', 'интеллект'
            ]
            for keyword in effect_keywords:
                if keyword in spell.desc.lower():
                    queries |= Q(desc__icontains=keyword)

        similar = Spell.objects.filter(queries).exclude(id=spell.id).distinct()
        similar = similar.order_by(
            '-level',
            '-school',
            'name'
        )[:limit]

        return similar


class EquipmentService:
    @staticmethod
    def get_similar_equipment(equipment, limit=5):
        similar = Equipment.objects.filter(
            Q(name__icontains=equipment.name.split()[0]) |
            Q(description__icontains=equipment.name.split()[0])
        ).exclude(id=equipment.id)

        if equipment.description:
            keywords = equipment.description.split()[:10]
            for keyword in keywords:
                if len(keyword) > 3:
                    similar = similar | Equipment.objects.filter(
                        Q(description__icontains=keyword) |
                        Q(name__icontains=keyword)
                    ).exclude(id=equipment.id)
        return similar.distinct()[:limit]

    @staticmethod
    def get_absolute_url(equipment):
        return reverse('equipment_detail', args=[str(equipment.id)])


class FavoriteService:
    CONTENT_TYPE_MODELS = {
        'monster': 'Monster',
        'spell': 'Spell',
        'equipment': 'Equipment',
    }

    CONTENT_TYPE_URLS = {
        'monster': 'monster_detail',
        'spell': 'spell_detail',
        'equipment': 'equipment_detail',
    }

    @staticmethod
    def get_object(favorite):
        if favorite.content_type == 'monster':
            from .models import Monster
            return Monster.objects.filter(id=favorite.object_id).first()
        elif favorite.content_type == 'spell':
            from .models import Spell
            return Spell.objects.filter(id=favorite.object_id).first()
        elif favorite.content_type == 'equipment':
            from .models import Equipment
            return Equipment.objects.filter(id=favorite.object_id).first()
        return None

    @staticmethod
    def get_object_name(favorite):
        obj = FavoriteService.get_object(favorite)
        return obj.name if obj else f"Объект #{favorite.object_id}"

    @staticmethod
    def get_object_url(favorite):
        view_name = FavoriteService.CONTENT_TYPE_URLS.get(favorite.content_type)
        if not view_name:
            return "#"
        return reverse(view_name, args=[favorite.object_id])

    @staticmethod
    def get_content_type_display_map():
        return {
            'monster': 'Монстр',
            'spell': 'Заклинание',
            'equipment': 'Снаряжение',
        }