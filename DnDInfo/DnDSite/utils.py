import requests
from django.conf import settings
from .models import Monster, Spell, Equipment, Armor_class, Speed, Component
import logging

logger = logging.getLogger(__name__)


class DndApiClient:
    def __init__(self):
        self.base_url = settings.DND_API_URL

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
                    'is_homebrew': False,
                    'is_approved': True,
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
            school_data = data.get('school', {})
            school_key = school_data.get('index', '')

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

            school = school_mapping.get(school_key, 'abjuration')
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
                    'is_homebrew': False,
                    'is_approved': True,
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
            description_parts = []
            if 'desc' in data and data['desc']:
                if isinstance(data['desc'], list):
                    description_parts.extend(data['desc'])
                else:
                    description_parts.append(str(data['desc']))
            if 'properties' in data and data['properties']:
                prop_names = []
                for prop in data.get('properties', []):
                    if 'name' in prop:
                        prop_names.append(prop['name'])
                if prop_names:
                    description_parts.append(f"Свойства: {', '.join(prop_names)}")
            if 'equipment_category' in data:
                category_data = data['equipment_category']
                if 'name' in category_data:
                    description_parts.append(f"Категория: {category_data['name']}")
            if 'weapon_category' in data:
                description_parts.append(f"Тип оружия: {data['weapon_category']}")
            if 'armor_category' in data:
                description_parts.append(f"Тип доспеха: {data['armor_category']}")
            if 'special' in data and data['special']:
                description_parts.append(f"Особое свойство: {data['special']}")
            if 'damage' in data and 'damage_dice' in data['damage']:
                damage_dice = data['damage']['damage_dice']
                damage_type = data['damage']['damage_type']['name'] if 'damage_type' in data['damage'] else ''
                description_parts.append(f"Урон: {damage_dice} ({damage_type})")
            if 'range' in data and 'normal' in data['range']:
                description_parts.append(f"Дальность: {data['range']['normal']} футов")
            if 'armor_class' in data and 'base' in data['armor_class']:
                description_parts.append(f"Класс брони: {data['armor_class']['base']}")
            if 'weight' in data and data['weight']:
                description_parts.append(f"Вес: {data['weight']} фунтов")
            description = ' | '.join(description_parts) if description_parts else None
            if description and len(description) > 2000:
                description = description[:1997] + '...'
            equipment, created = Equipment.objects.get_or_create(
                name=data['name'],
                is_homebrew=False,
                defaults={
                    'description': description,
                    'weight': data.get('weight', 0),
                    'cost_quantity': cost_quantity,
                    'cost_unit': cost_unit,
                    'is_approved': True,
                }
            )
            if not created and not equipment.description and description:
                equipment.description = description
                equipment.save()
                self.stdout.write(f"  ⚡ Обновлено описание для: {equipment.name}")

            return equipment

        except Exception as e:
            logger.error(f"Ошибка при импорте снаряжения {index}: {e}")
            return None

    def update_equipment_descriptions(self, limit=50):
        from .models import Equipment
        import re
        equipment_to_update = Equipment.objects.filter(
            description__isnull=True,
            is_homebrew=False
        )[:limit]

        updated_count = 0

        for equipment in equipment_to_update:
            try:
                equipment_list = self.api_client.get_equipment_list()

                for item in equipment_list:
                    api_name = re.sub(r'[^\w\s-]', '', item['name'].lower())
                    db_name = re.sub(r'[^\w\s-]', '', equipment.name.lower())

                    if api_name == db_name:
                        updated = self.import_equipment(item['index'])
                        if updated:
                            updated_count += 1
                        break

            except Exception as e:
                logger.error(f"Ошибка при обновлении {equipment.name}: {e}")

        return updated_count