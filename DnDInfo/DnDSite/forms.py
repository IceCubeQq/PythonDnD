from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Monster, Spell, Equipment, Armor_class, Speed, Component


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Ваш email'
    }))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Имя пользователя'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})


class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Имя пользователя'
        })
        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Пароль'
        })

class MonsterForm(forms.ModelForm):
    speeds_input = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'walk: 30\nfly: 30\nswim: 20\nclimb: 30'
        }),
        required=False,
        label='Скорости'
    )

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
            'dexterity': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'max': 30
            }),
            'constitution': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'max': 30
            }),
            'intelligence': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'max': 30
            }),
            'wisdom': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'max': 30
            }),
            'charisma': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'max': 30
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        SIZE_CHOICES = [
            ('', 'Выберите размер'),
            ('Tiny', 'Крошечный'),
            ('Small', 'Маленький'),
            ('Medium', 'Средний'),
            ('Large', 'Большой'),
            ('Huge', 'Огромный'),
            ('Gargantuan', 'Гигантский'),
        ]
        self.fields['size'].widget = forms.Select(
            choices=SIZE_CHOICES,
            attrs={'class': 'form-control'}
        )

    def clean(self):
        cleaned_data = super().clean()
        hit_points = cleaned_data.get('hit_points')

        if hit_points and hit_points <= 0:
            raise ValidationError({
                'hit_points': 'Уровень жизней должен быть положительным числом'
            })

        return cleaned_data


class SpellForm(forms.ModelForm):
    components = forms.MultipleChoiceField(
        choices=Component.COMPONENT_TYPES,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        required=False,
        label='Компоненты'
    )

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
        fields = ['name', 'description', 'weight', 'cost_quantity', 'cost_unit']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Название снаряжения'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Описание предмета, его свойств и особенностей'
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

    def clean_weight(self):
        weight = self.cleaned_data.get('weight')
        if weight is not None and weight < 0:
            raise ValidationError('Вес не может быть отрицательным')
        return weight

    def clean_cost_quantity(self):
        cost_quantity = self.cleaned_data.get('cost_quantity')
        if cost_quantity is not None and cost_quantity < 0:
            raise ValidationError('Стоимость не может быть отрицательной')
        return cost_quantity


class ArmorClassForm(forms.ModelForm):
    class Meta:
        model = Armor_class
        fields = ['type', 'value']
        widgets = {
            'type': forms.Select(attrs={'class': 'form-control'}),
            'value': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
                'placeholder': 'Значение брони'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and not self.instance.value:
            self.fields['value'].initial = ''


class SpeedForm(forms.ModelForm):
    class Meta:
        model = Speed
        fields = ['movement_type', 'value']
        widgets = {
            'movement_type': forms.Select(attrs={'class': 'form-control'}),
            'value': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Значение (например: 30 футов)'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and not self.instance.movement_type:
            self.fields['movement_type'].initial = ''
        if self.instance and not self.instance.value:
            self.fields['value'].initial = ''


class ComponentForm(forms.ModelForm):
    class Meta:
        model = Component
        fields = ['type']
        widgets = {
            'type': forms.Select(attrs={'class': 'form-control'}),
        }


class MonsterEditForm(forms.ModelForm):
    speeds_input = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'walk: 30\nfly: 30\nswim: 20\nclimb: 30'
        }),
        required=False,
        label='Скорости'
    )

    class Meta:
        model = Monster
        fields = [
            'name', 'size', 'type', 'hit_points',
            'strength', 'dexterity', 'constitution',
            'intelligence', 'wisdom', 'charisma',
            'is_approved'
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
            'dexterity': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'max': 30
            }),
            'constitution': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'max': 30
            }),
            'intelligence': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'max': 30
            }),
            'wisdom': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'max': 30
            }),
            'charisma': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'max': 30
            }),
            'is_approved': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        SIZE_CHOICES = [
            ('', 'Выберите размер'),
            ('Tiny', 'Крошечный'),
            ('Small', 'Маленький'),
            ('Medium', 'Средний'),
            ('Large', 'Большой'),
            ('Huge', 'Огромный'),
            ('Gargantuan', 'Гигантский'),
        ]
        self.fields['size'].widget = forms.Select(
            choices=SIZE_CHOICES,
            attrs={'class': 'form-control'}
        )
        if user and not user.is_staff:
            self.fields.pop('is_approved')

    def clean(self):
        cleaned_data = super().clean()
        hit_points = cleaned_data.get('hit_points')

        if hit_points and hit_points <= 0:
            raise ValidationError({
                'hit_points': 'Уровень жизней должен быть положительным числом'
            })

        return cleaned_data


class SpellEditForm(forms.ModelForm):
    components = forms.MultipleChoiceField(
        choices=Component.COMPONENT_TYPES,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        required=False,
        label='Компоненты'
    )

    class Meta:
        model = Spell
        fields = [
            'name', 'desc', 'spell_range', 'duration',
            'casting_time', 'level', 'school',
            'ritual', 'concentration', 'is_approved'
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
            'is_approved': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user = kwargs.pop('user', None)
        if user and not user.is_staff:
            self.fields.pop('is_approved')

    def clean_level(self):
        level = self.cleaned_data.get('level')
        if level is not None and (level < 0 or level > 9):
            raise ValidationError('Уровень заклинания должен быть от 0 до 9')
        return level


class EquipmentEditForm(forms.ModelForm):
    class Meta:
        model = Equipment
        fields = ['name', 'description', 'weight', 'cost_quantity', 'cost_unit', 'is_approved']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Название снаряжения'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Описание предмета, его свойств и особенностей...'
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
            'is_approved': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user and not user.is_staff:
            self.fields.pop('is_approved')

    def clean_weight(self):
        weight = self.cleaned_data.get('weight')
        if weight is not None and weight < 0:
            raise ValidationError('Вес не может быть отрицательным')
        return weight

    def clean_cost_quantity(self):
        cost_quantity = self.cleaned_data.get('cost_quantity')
        if cost_quantity is not None and cost_quantity < 0:
            raise ValidationError('Стоимость не может быть отрицательной')
        return cost_quantity

class MultipleSpeedForm(forms.Form):
    speeds = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'walk: 30\nfly: 30\nswim: 20\nclimb: 30'
        }),
        required=False,
        label='Скорости',
        help_text='Введите каждую скорость с новой строки в формате: "тип: значение"'
    )


class MonsterSpeedsForm(forms.Form):
    speeds = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'walk: 30\nfly: 30\nswim: 20\ndig: 10'
        }),
        required=False,
        label='Скорости',
        help_text='Введите каждую скорость с новой строки в формате: "тип: значение".<br>'
                  'Доступные типы: walk (ходьба), fly (полёт), swim (плавание), '
                  'climb (лазание), burrow (рытьё), dig (капая), hover (парение)'
    )

    def clean_speeds(self):
        speeds_text = self.cleaned_data.get('speeds', '')
        valid_types = ['walk', 'fly', 'swim', 'climb', 'burrow', 'dig', 'hover', 'other']

        if speeds_text:
            speeds_list = []
            for i, line in enumerate(speeds_text.split('\n')):
                line = line.strip()
                if line:
                    if ':' not in line:
                        raise ValidationError(
                            f'Строка {i + 1}: "{line}" - неверный формат. Используйте "тип: значение"')

                    movement_type, value = line.split(':', 1)
                    movement_type = movement_type.strip().lower()
                    value = value.strip()

                    if movement_type not in valid_types:
                        raise ValidationError(
                            f'Строка {i + 1}: тип "{movement_type}" не поддерживается. '
                            f'Доступные типы: {", ".join(valid_types)}'
                        )

                    speeds_list.append((movement_type, value))

            return speeds_list
        return []