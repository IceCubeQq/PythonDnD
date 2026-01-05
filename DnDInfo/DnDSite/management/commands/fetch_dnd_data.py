from django.core.management.base import BaseCommand
from django.db import transaction
from DnDSite.utils import DataImporter
from DnDSite.models import Equipment
import logging

from DnDInfo.DnDSite import models

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
        parser.add_argument(
            '--update-descriptions',
            action='store_true',
            help='Обновить описания существующих записей'
        )

    def handle(self, *args, **options):
        limit = options['limit']
        update_descriptions = options['update_descriptions']
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

                if update_descriptions:
                    self.stdout.write('Обновление описаний существующих записей')
                    self.update_existing_descriptions(importer, limit)

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Ошибка при загрузке данных: {e}'))
            logger.error(f'Ошибка при загрузке данных: {e}')

    def update_existing_descriptions(self, importer, limit):
        equipment_without_description = Equipment.objects.filter(is_homebrew=False).filter(
            models.Q(description__isnull=True) | models.Q(description='')
        )[:limit]

        total_count = equipment_without_description.count()
        updated_count = 0
        skipped_count = 0

        self.stdout.write(f'Найдено {total_count} предметов без описания')

        if total_count == 0:
            self.stdout.write(self.style.WARNING('Нет предметов для обновления описаний'))
            return

        for i, equipment in enumerate(equipment_without_description, 1):
            try:
                self.stdout.write(f'[{i}/{total_count}] Обработка: {equipment.name}')
                equipment_list = importer.api_client.get_equipment_list()
                found = False

                for item in equipment_list:
                    if item['name'].lower() == equipment.name.lower():
                        updated_equipment = importer.import_equipment(item['index'])
                        if updated_equipment and updated_equipment.description:
                            updated_count += 1
                            self.stdout.write(
                                self.style.SUCCESS(f'Обновлено описание')
                            )
                        else:
                            skipped_count += 1
                            self.stdout.write(
                                self.style.WARNING(f'Не удалось получить описание из API')
                            )
                        found = True
                        break

                if not found:
                    skipped_count += 1
                    self.stdout.write(
                        self.style.WARNING(f'Не найдено в API')
                    )

            except Exception as e:
                logger.error(f"Ошибка при обновлении {equipment.name}: {e}")
                self.stdout.write(
                    self.style.ERROR(f'  ✗ Ошибка: {str(e)[:50]}...')
                )
                skipped_count += 1
        self.stdout.write(self.style.SUCCESS(f'Обработано: {total_count}'))
        self.stdout.write(self.style.SUCCESS(f'Обновлено: {updated_count}'))
        self.stdout.write(self.style.WARNING(f'Пропущено: {skipped_count}'))