# DnDSite/management/commands/fix_spell_schools.py
from django.core.management.base import BaseCommand
from ...models import Spell
import requests
import logging

from ...constants import SPECIAL_CASES, SCHOOL_MAPPING

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Исправляет школы магии у заклинаний по данным из API'
    def add_arguments(self, parser):
        parser.add_argument(
            '--limit',
            type=int,
            default=0,
            help='Количество заклинаний для обновления (0 - все)'
        )

    def get_spell_index_from_name(self, name):
        index = name.lower()
        index = index.replace(' ', '-')
        index = index.replace('/', '-')
        index = index.replace("'", '')
        index = index.replace('"', '')
        index = index.replace(':', '')
        index = index.replace('.', '')
        index = index.replace(',', '')
        index = index.replace('&', '')

        special_cases = SPECIAL_CASES

        name_lower = name.lower()
        if name_lower in special_cases:
            return special_cases[name_lower]

        return index

    def handle(self, *args, **options):
        base_url = 'https://www.dnd5eapi.co/api/2014'
        spells = Spell.objects.all()

        if options['limit'] > 0:
            spells = spells[:options['limit']]

        updated_count = 0
        total_spells = spells.count()
        processed = 0

        for spell in spells:
            try:
                processed += 1
                self.stdout.write(f"[{processed}/{total_spells}] Обработка: {spell.name}")

                index = self.get_spell_index_from_name(spell.name)
                url = f"{base_url}/spells/{index}"
                response = requests.get(url, timeout=10)

                if response.status_code == 200:
                    data = response.json()

                    if 'school' in data:
                        school_data = data['school']
                        school_key = school_data.get('index', '')

                        school_mapping = SCHOOL_MAPPING

                        new_school = school_mapping.get(school_key, spell.school)

                        if spell.school != new_school:
                            spell.school = new_school
                            spell.save()
                            updated_count += 1
                            self.stdout.write(
                                self.style.SUCCESS(f"Обновлено: {spell.name} -> {new_school}")
                            )
                        else:
                            self.stdout.write(
                                self.style.WARNING(f"Без изменений: {spell.name} уже {spell.get_school_display()}")
                            )
                    else:
                        self.stdout.write(
                            self.style.ERROR(f"Нет данных о школе: {spell.name}")
                        )
                else:
                    self.stdout.write(
                        self.style.WARNING(f"Не найдено напрямую (статус {response.status_code}): {spell.name}")
                    )
                    try:
                        list_url = f"{base_url}/spells"
                        list_response = requests.get(list_url, timeout=10)

                        if list_response.status_code == 200:
                            all_spells = list_response.json().get('results', [])

                            found_spell = None
                            for api_spell in all_spells:
                                if api_spell['name'].lower() == spell.name.lower():
                                    found_spell = api_spell
                                    break

                            if found_spell:
                                spell_index = found_spell['index']
                                detail_url = f"{base_url}/spells/{spell_index}"
                                detail_response = requests.get(detail_url, timeout=10)

                                if detail_response.status_code == 200:
                                    detail_data = detail_response.json()
                                    if 'school' in detail_data:
                                        school_key = detail_data['school'].get('index', '')
                                        new_school = school_mapping.get(school_key, spell.school)

                                        if spell.school != new_school:
                                            spell.school = new_school
                                            spell.save()
                                            updated_count += 1
                                            self.stdout.write(
                                                self.style.SUCCESS(
                                                    f"Обновлено через поиск: {spell.name} -> {new_school}")
                                            )
                    except Exception as e:
                        logger.error(f"Ошибка при поиске {spell.name}: {e}")

            except Exception as e:
                logger.error(f"Ошибка при обновлении заклинания {spell.name}: {e}")
                self.stdout.write(
                    self.style.ERROR(f"Ошибка для {spell.name}: {str(e)}")
                )

        self.stdout.write(
            self.style.SUCCESS(f'\nГотово! Обновлено {updated_count} из {total_spells} заклинаний')
        )