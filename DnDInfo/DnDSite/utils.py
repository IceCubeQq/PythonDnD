import requests
from django.conf import settings
from .models import Monster, Spell, Equipment, Armor_class, Speed, Component
import logging

logger = logging.getLogger(__name__)


class DndApiClient:
    def __init__(self):
        self.base_url = settings.DND_API_BASE_URL

    def _make_request(self, endpoint):
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Ошибка при запросе к {url}: {e}")
            return None

    def get_monsters_list(self):
        data = self._make_request('monsters')
        return data.get('results', []) if data else []

    def get_monster_detail(self, index):
        return self._make_request(f'monsters/{index}')

    def get_spells_list(self):
        data = self._make_request('spells')
        return data.get('results', []) if data else []

    def get_spell_detail(self, index):
        return self._make_request(f'spells/{index}')

    def get_equipment_list(self):
        data = self._make_request('equipment')
        return data.get('results', []) if data else []

    def get_equipment_detail(self, index):
        return self._make_request(f'equipment/{index}')


class DataImporter:
    def __init__(self):
        self.api_client = DndApiClient()

    def import_monster(self, index):
        data = self.api_client.get_monster_detail(index)
        if not data:
            return None

        try:
            monster, created = Monster.objects.get_or_create(
                name=data['name'],
                defaults={
                    'size': data.get('size', 'Medium'),
                    'type': data.get('type', 'humanoid'),
                    'hit_points': data.get('hit_points', 0),
                    'strength': data.get('strength', 10),
                    'dexterity': data.get('dexterity', 10),
                    'constitution': data.get('constitution', 10),
                    'intelligence': data.get('intelligence', 10),
                    'wisdom': data.get('wisdom', 10),
                    'charisma': data.get('charisma', 10),
                }
            )

            armor_data = data.get('armor_class', [])
            if isinstance(armor_data, list):
                for ac in armor_data:
                    Armor_class.objects.get_or_create(
                        monster=monster,
                        type=ac.get('type', 'natural'),
                        defaults={'value': ac.get('value', 10)}
                    )
            elif isinstance(armor_data, int):
                Armor_class.objects.get_or_create(
                    monster=monster,
                    type='natural',
                    defaults={'value': armor_data}
                )
            speed_data = data.get('speed', {})
            for movement_type, value in speed_data.items():
                if value:
                    Speed.objects.get_or_create(
                        monster=monster,
                        movement_type=movement_type,
                        defaults={'value': str(value)}
                    )

            return monster

        except Exception as e:
            logger.error(f"Ошибка при импорте монстра {index}: {e}")
            return None

    def import_spell(self, index):
        data = self.api_client.get_spell_detail(index)
        if not data:
            return None

        try:
            school_mapping = {
                'abjuration': 'abjuration',
                'conjuration': 'conjuration',
                'divination': 'divination',
                'enchantment': 'enchantment',
                'evocation': 'evocation',
                'illusion': 'illusion',
                'necromancy': 'necromancy',
                'transmutation': 'transmutation'
            }

            school = school_mapping.get(data.get('school', {}).get('name', ''), 'abjuration')
            desc = ' '.join(data.get('desc', [])) if isinstance(data.get('desc'), list) else data.get('desc', '')

            spell, created = Spell.objects.get_or_create(
                name=data['name'],
                defaults={
                    'desc': desc[:1000],
                    'spell_range': data.get('range', ''),
                    'duration': data.get('duration', ''),
                    'casting_time': data.get('casting_time', ''),
                    'level': data.get('level', 0),
                    'school': school,
                    'ritual': data.get('ritual', False),
                    'concentration': data.get('concentration', False),
                }
            )
            components = data.get('components', [])
            component_mapping = {
                'V': 'V',
                'S': 'S',
                'M': 'M'
            }

            for comp in components:
                comp_type = component_mapping.get(comp, 'V')
                Component.objects.get_or_create(
                    spell=spell,
                    type=comp_type
                )

            return spell

        except Exception as e:
            logger.error(f"Ошибка при импорте заклинания {index}: {e}")
            return None

    def import_equipment(self, index):
        data = self.api_client.get_equipment_detail(index)
        if not data:
            return None

        try:
            cost_data = data.get('cost', {})
            cost_quantity = cost_data.get('quantity', 0)
            cost_unit = cost_data.get('unit', 'gp')

            equipment, created = Equipment.objects.get_or_create(
                name=data['name'],
                defaults={
                    'weight': data.get('weight', 0),
                    'cost_quantity': cost_quantity,
                    'cost_unit': cost_unit,
                }
            )
            return equipment
        except Exception as e:
            logger.error(f"Ошибка при импорте снаряжения {index}: {e}")
            return None