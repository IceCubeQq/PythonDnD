from django.core.management.base import BaseCommand
from django.db import transaction
from DnDSite.utils import DataImporter
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Загружает данные из D&D 5e API в базу данных'

    def add_arguments(self, parser):
        parser.add_argument(
            '--limit',
            type=int,
            default=20,
            help='Количество записей каждого типа для загрузки'
        )

    def handle(self, *args, **options):
        limit = options['limit']
        importer = DataImporter()

        self.stdout.write(self.style.SUCCESS('Начинаем загрузку данных из D&D 5e API...'))

        try:
            with transaction.atomic():
                self.stdout.write('Загрузка монстров')
                monsters = importer.api_client.get_monsters_list()[:limit]
                monster_count = 0

                for monster_data in monsters:
                    monster = importer.import_monster(monster_data['index'])
                    if monster:
                        monster_count += 1

                self.stdout.write(self.style.SUCCESS(f'Загружено монстров: {monster_count}'))
                self.stdout.write('Загрузка заклинаний')
                spells = importer.api_client.get_spells_list()[:limit]
                spell_count = 0

                for spell_data in spells:
                    spell = importer.import_spell(spell_data['index'])
                    if spell:
                        spell_count += 1

                self.stdout.write(self.style.SUCCESS(f'Загружено заклинаний: {spell_count}'))
                self.stdout.write('Загрузка снаряжения')
                equipment_list = importer.api_client.get_equipment_list()[:limit]
                equipment_count = 0

                for equipment_data in equipment_list:
                    equipment = importer.import_equipment(equipment_data['index'])
                    if equipment:
                        equipment_count += 1

                self.stdout.write(self.style.SUCCESS(f'Загружено снаряжения: {equipment_count}'))
                self.stdout.write(self.style.SUCCESS(f'Монстров: {monster_count}'))
                self.stdout.write(self.style.SUCCESS(f'Заклинаний: {spell_count}'))
                self.stdout.write(self.style.SUCCESS(f'Снаряжения: {equipment_count}'))
                self.stdout.write(self.style.SUCCESS(f'Всего записей: {monster_count + spell_count + equipment_count}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Ошибка при загрузке данных: {e}'))
            logger.error(f'Ошибка при загрузке данных: {e}')