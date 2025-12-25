from django import forms
from django.core.exceptions import ValidationError
from .models import Monster, Spell, Equipment, Armor_class, Speed, Component


class MonsterForm(forms.ModelForm):
    class Meta:
        model = Monster
        fields = [
            'name', 'size', 'type', 'hit_points',
            'strength', 'dexterity', 'constitution',
            'intelligence', 'wisdom', 'charisma'
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Название монстра'
            }),
            'size': forms.Select(attrs={'class': 'form-control'}),
            'type': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Тип (дракон, гуманоид и т.д.)'
            }),
            'hit_points': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1
            }),
            'strength': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'max': 30
            }),
            'dexterity': forms.NumberInput(attrs={'class': 'form-control'}),
            'constitution': forms.NumberInput(attrs={'class': 'form-control'}),
            'intelligence': forms.NumberInput(attrs={'class': 'form-control'}),
            'wisdom': forms.NumberInput(attrs={'class': 'form-control'}),
            'charisma': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        hit_points = cleaned_data.get('hit_points')

        if hit_points and hit_points <= 0:
            raise ValidationError({
                'hit_points': 'Уровень жизней должен быть положительным числом'
            })

        return cleaned_data


class SpellForm(forms.ModelForm):
    class Meta:
        model = Spell
        fields = [
            'name', 'desc', 'spell_range', 'duration',
            'casting_time', 'level', 'school',
            'ritual', 'concentration'
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Название заклинания'
            }),
            'desc': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Описание заклинания'
            }),
            'spell_range': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Дальность'
            }),
            'duration': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Продолжительность'
            }),
            'casting_time': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Время накладывания'
            }),
            'level': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
                'max': 9
            }),
            'school': forms.Select(attrs={'class': 'form-control'}),
            'ritual': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'concentration': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean_level(self):
        level = self.cleaned_data.get('level')
        if level is not None and (level < 0 or level > 9):
            raise ValidationError('Уровень заклинания должен быть от 0 до 9')
        return level


class EquipmentForm(forms.ModelForm):
    class Meta:
        model = Equipment
        fields = ['name', 'weight', 'cost_quantity', 'cost_unit']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Название снаряжения'
            }),
            'weight': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'placeholder': 'Вес в фунтах'
            }),
            'cost_quantity': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'placeholder': 'Стоимость'
            }),
            'cost_unit': forms.Select(attrs={'class': 'form-control'}),
        }


class ArmorClassForm(forms.ModelForm):
    class Meta:
        model = Armor_class
        fields = ['type', 'value']
        widgets = {
            'type': forms.Select(attrs={'class': 'form-control'}),
            'value': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0
            }),
        }


class SpeedForm(forms.ModelForm):
    class Meta:
        model = Speed
        fields = ['movement_type', 'value']
        widgets = {
            'movement_type': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Тип (walk, fly, swim)'
            }),
            'value': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Значение'
            }),
        }


class ComponentForm(forms.ModelForm):
    class Meta:
        model = Component
        fields = ['type']
        widgets = {
            'type': forms.Select(attrs={'class': 'form-control'}),
        }