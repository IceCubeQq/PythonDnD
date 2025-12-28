from django.contrib.auth import login, authenticate, logout
from django.db import transaction
from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.db.models import Q, Count, Avg
from .models import Monster, Spell, Equipment, Armor_class, Speed, Component
from .forms import MonsterForm, SpellForm, EquipmentForm, ArmorClassForm, SpeedForm, ComponentForm, MonsterEditForm, \
    SpellEditForm, EquipmentEditForm, CustomUserCreationForm, CustomAuthenticationForm


def is_admin(user):
    return user.is_authenticated and user.is_staff


def apply_filters(request, queryset):
    search = request.GET.get('search', '')
    if search:
        queryset = queryset.filter(name__icontains=search)
    sort_by = request.GET.get('sort', 'name')
    if sort_by in ['name', 'hit_points', 'strength']:
        queryset = queryset.order_by(sort_by)

    return queryset


def index(request):
    context = {
        'monster_count': Monster.objects.count(),
        'spell_count': Spell.objects.count(),
        'equipment_count': Equipment.objects.count(),

        'official_monsters': Monster.objects.filter(is_homebrew=False).order_by('-id')[:5],
        'official_spells': Spell.objects.filter(is_homebrew=False).order_by('-id')[:5],
        'official_equipment': Equipment.objects.filter(is_homebrew=False).order_by('-id')[:5],

        'homebrew_monsters': Monster.objects.filter(is_homebrew=True, is_approved=True).order_by('-id')[:5],
        'homebrew_spells': Spell.objects.filter(is_homebrew=True, is_approved=True).order_by('-id')[:5],
        'homebrew_equipment': Equipment.objects.filter(is_homebrew=True, is_approved=True).order_by('-id')[:5],

        'pending_monsters_count': Monster.objects.filter(is_homebrew=True,
                                                         is_approved=False).count() if request.user.is_staff else 0,
        'pending_spells_count': Spell.objects.filter(is_homebrew=True,
                                                     is_approved=False).count() if request.user.is_staff else 0,
        'pending_equipment_count':
            Equipment.objects.filter(is_homebrew=True, is_approved=False).count() if request.user.is_staff else 0,
    }
    return render(request, 'DnDSite/index.html', context)


def monster_list(request):
    show_homebrew = request.GET.get('show_homebrew', 'false') == 'true'

    if show_homebrew:
        monsters_list = Monster.objects.filter(is_homebrew=True, is_approved=True)
    else:
        monsters_list = Monster.objects.filter(is_homebrew=False)

    search = request.GET.get('search', '')
    if search:
        monsters_list = monsters_list.filter(name__icontains=search)

    size = request.GET.get('size', '')
    if size:
        monsters_list = monsters_list.filter(size=size)

    monster_type = request.GET.get('type', '')
    if monster_type:
        monsters_list = monsters_list.filter(type__icontains=monster_type)

    sort_by = request.GET.get('sort', 'name')
    if sort_by == 'hit_points':
        monsters_list = monsters_list.order_by('-hit_points')
    elif sort_by == 'strength':
        monsters_list = monsters_list.order_by('-strength')
    elif sort_by == 'dexterity':
        monsters_list = monsters_list.order_by('-dexterity')
    elif sort_by == 'constitution':
        monsters_list = monsters_list.order_by('-constitution')
    elif sort_by == 'intelligence':
        monsters_list = monsters_list.order_by('-intelligence')
    elif sort_by == 'wisdom':
        monsters_list = monsters_list.order_by('-wisdom')
    elif sort_by == 'charisma':
        monsters_list = monsters_list.order_by('-charisma')
    else:
        monsters_list = monsters_list.order_by('name')

    paginator = Paginator(monsters_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'monsters': page_obj.object_list,
        'total_count': monsters_list.count(),
        'search_query': search,
        'selected_size': size,
        'selected_type': monster_type,
        'sort_by': sort_by,
        'show_homebrew': show_homebrew,
    }
    return render(request, 'DnDSite/monster_list.html', context)


def monster_detail(request, monster_id):
    monster = get_object_or_404(Monster, id=monster_id)
    armor_classes = Armor_class.objects.filter(monster=monster)
    speeds = Speed.objects.filter(monster=monster)
    def calculate_modifier(score):
        return (score - 10) // 2

    context = {
        'monster': monster,
        'armor_classes': armor_classes,
        'speeds': speeds,
        'strength_mod': calculate_modifier(monster.strength),
        'dexterity_mod': calculate_modifier(monster.dexterity),
        'constitution_mod': calculate_modifier(monster.constitution),
        'intelligence_mod': calculate_modifier(monster.intelligence),
        'wisdom_mod': calculate_modifier(monster.wisdom),
        'charisma_mod': calculate_modifier(monster.charisma),
        'can_edit': request.user.is_staff or (request.user == monster.created_by and not monster.is_homebrew),
    }

    return render(request, 'DnDSite/monster_detail.html', context)


def spell_list(request):
    show_homebrew = request.GET.get('show_homebrew', 'false') == 'true'

    if show_homebrew:
        spells_list = Spell.objects.filter(is_homebrew=True, is_approved=True)
    else:
        spells_list = Spell.objects.filter(is_homebrew=False)

    level_filter = request.GET.get('level')
    school = request.GET.get('school', '')
    sort_by = request.GET.get('sort', 'name')

    if level_filter and level_filter.isdigit():
        spells_list = spells_list.filter(level=int(level_filter))

    search = request.GET.get('search', '')
    if search:
        spells_list = spells_list.filter(Q(name__icontains=search) | Q(desc__icontains=search))

    if school:
        spells_list = spells_list.filter(school=school)

    if sort_by == 'name':
        spells_list = spells_list.order_by('name')
    elif sort_by == 'level':
        spells_list = spells_list.order_by('level', 'name')
    elif sort_by == 'school':
        spells_list = spells_list.order_by('school', 'level', 'name')

    paginator = Paginator(spells_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'spells': page_obj.object_list,
        'levels': range(0, 10),
        'selected_level': level_filter,
        'selected_school': school,
        'search_query': search,
        'sort_by': sort_by,
        'show_homebrew': show_homebrew,
    }
    return render(request, 'DnDSite/spell_list.html', context)


def spell_detail(request, spell_id):
    spell = get_object_or_404(Spell, id=spell_id)
    components = Component.objects.filter(spell=spell)

    context = {
        'spell': spell,
        'components': components,
        'can_edit': request.user.is_staff or (request.user == spell.created_by and not spell.is_homebrew),
    }
    return render(request, 'DnDSite/spell_detail.html', context)


def equipment_list(request):
    show_homebrew = request.GET.get('show_homebrew', 'false') == 'true'

    if show_homebrew:
        equipment_list = Equipment.objects.filter(is_homebrew=True, is_approved=True)
    else:
        equipment_list = Equipment.objects.filter(is_homebrew=False)

    search = request.GET.get('search', '')
    if search:
        equipment_list = equipment_list.filter(name__icontains=search)

    cost_unit = request.GET.get('cost_unit', '')
    if cost_unit:
        equipment_list = equipment_list.filter(cost_unit=cost_unit)

    weight_filter = request.GET.get('weight_filter', '')
    if weight_filter:
        if weight_filter == 'light':
            equipment_list = equipment_list.filter(weight__lt=5)
        elif weight_filter == 'medium':
            equipment_list = equipment_list.filter(weight__range=(5, 15))
        elif weight_filter == 'heavy':
            equipment_list = equipment_list.filter(weight__gt=15)

    sort_by = request.GET.get('sort', 'name')
    if sort_by == 'name':
        equipment_list = equipment_list.order_by('name')
    elif sort_by == 'weight_asc':
        equipment_list = equipment_list.order_by('weight')
    elif sort_by == 'weight_desc':
        equipment_list = equipment_list.order_by('-weight')
    elif sort_by == 'price_asc':
        equipment_list = equipment_list.order_by('cost_quantity')
    elif sort_by == 'price_desc':
        equipment_list = equipment_list.order_by('-cost_quantity')
    paginator = Paginator(equipment_list, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'equipment': page_obj.object_list,
        'search_query': search,
        'sort_by': sort_by,
        'selected_cost_unit': cost_unit,
        'selected_weight_filter': weight_filter,
        'total_count': equipment_list.count(),
        'show_homebrew': show_homebrew,
    }
    return render(request, 'DnDSite/equipment_list.html', context)

def equipment_detail(request, equipment_id):
    equipment = get_object_or_404(Equipment, id=equipment_id)

    if equipment.cost_quantity:
        cost_display = f"{equipment.cost_quantity} {equipment.get_cost_unit_display()}"
    else:
        cost_display = "Бесплатно"

    context = {
        'equipment': equipment,
        'cost_display': cost_display,
        'can_edit': request.user.is_staff or (request.user == equipment.created_by and not equipment.is_homebrew),
    }
    return render(request, 'DnDSite/equipment_detail.html', context)


@login_required
def add_monster(request):
    if request.method == 'POST':
        form = MonsterForm(request.POST)
        armor_form = ArmorClassForm(request.POST, prefix='armor')
        speed_form = SpeedForm(request.POST, prefix='speed')

        if form.is_valid():
            with transaction.atomic():
                monster = form.save(commit=False)
                monster.is_homebrew = True
                monster.created_by = request.user
                monster.is_approved = False
                monster.save()

                if armor_form.is_valid() and armor_form.cleaned_data.get('value'):
                    armor = armor_form.save(commit=False)
                    armor.monster = monster
                    armor.save()

                if speed_form.is_valid() and speed_form.cleaned_data.get('movement_type'):
                    speed = speed_form.save(commit=False)
                    speed.monster = monster
                    speed.save()

            messages.success(request, 'Монстр успешно добавлен. Он будет рассмотрен администратором.')
            return redirect('monster_detail', monster_id=monster.id)
    else:
        form = MonsterForm()
        armor_form = ArmorClassForm(prefix='armor')
        speed_form = SpeedForm(prefix='speed')

    context = {
        'form': form,
        'armor_form': armor_form,
        'speed_form': speed_form,
    }
    return render(request, 'DnDSite/add_monster.html', context)


@login_required
def add_spell(request):
    if request.method == 'POST':
        form = SpellForm(request.POST)

        if form.is_valid():
            with transaction.atomic():
                spell = form.save(commit=False)
                spell.is_homebrew = True
                spell.created_by = request.user
                spell.is_approved = False
                spell.save()

                components = request.POST.getlist('components')
                for comp_type in components:
                    if comp_type in ['V', 'S', 'M']:
                        Component.objects.get_or_create(
                            spell=spell,
                            type=comp_type
                        )

            messages.success(request, 'Заклинание успешно добавлено. Оно будет рассмотрено администратором.')
            return redirect('spell_detail', spell_id=spell.id)
    else:
        form = SpellForm()

    context = {
        'form': form,
        'component_choices': Component.COMPONENT_TYPES,
    }
    return render(request, 'DnDSite/add_spell.html', context)


@login_required
def add_equipment(request):
    if request.method == 'POST':
        form = EquipmentForm(request.POST)

        if form.is_valid():
            equipment = form.save(commit=False)
            equipment.is_homebrew = True
            equipment.created_by = request.user
            equipment.is_approved = False
            equipment.save()

            messages.success(request, 'Снаряжение успешно добавлено. Оно будет рассмотрено администратором.')
            return redirect('equipment_detail', equipment_id=equipment.id)
    else:
        form = EquipmentForm()

    return render(request, 'DnDSite/add_equipment.html', {'form': form})


@login_required
def edit_monster(request, monster_id):
    monster = get_object_or_404(Monster, id=monster_id)

    if not request.user.is_staff and monster.created_by != request.user:
        messages.error(request, 'У вас нет прав для редактирования этого монстра.')
        return redirect('monster_detail', monster_id=monster_id)

    armor_class = monster.armor_classes.first()
    speed = monster.speeds.first()

    if request.method == 'POST':
        form = MonsterEditForm(request.POST, instance=monster, user=request.user)
        armor_form = ArmorClassForm(request.POST, instance=armor_class, prefix='armor')
        speed_form = SpeedForm(request.POST, instance=speed, prefix='speed')

        if form.is_valid() and armor_form.is_valid() and speed_form.is_valid():
            with transaction.atomic():
                monster = form.save(commit=False)
                if monster.is_homebrew and not request.user.is_staff:
                    monster.is_approved = False
                    messages.info(request, 'Монстр отправлен на повторное рассмотрение администратором.')

                monster.save()

                armor = armor_form.save(commit=False)
                armor.monster = monster
                if armor.value:
                    armor.save()
                elif armor.pk:
                    armor.delete()

                speed = speed_form.save(commit=False)
                speed.monster = monster
                if speed.value and speed.movement_type:
                    speed.save()
                elif speed.pk:
                    speed.delete()

                messages.success(request, 'Монстр успешно обновлен.')
                if request.user.is_staff:
                    return redirect('monster_detail', monster_id=monster_id)
                else:
                    return redirect('monster_list')
    else:
        form = MonsterEditForm(instance=monster, user=request.user)
        armor_form = ArmorClassForm(instance=armor_class, prefix='armor')
        speed_form = SpeedForm(instance=speed, prefix='speed')

    context = {
        'form': form,
        'armor_form': armor_form,
        'speed_form': speed_form,
        'monster': monster,
        'is_admin': request.user.is_staff,
    }
    return render(request, 'DnDSite/edit_monster.html', context)

@login_required
def edit_spell(request, spell_id):
    spell = get_object_or_404(Spell, id=spell_id)

    if not request.user.is_staff and spell.created_by != request.user:
        messages.error(request, 'У вас нет прав для редактирования этого заклинания.')
        return redirect('spell_detail', spell_id=spell_id)
    current_components = Component.objects.filter(spell=spell).values_list('type', flat=True)

    if request.method == 'POST':
        form = SpellEditForm(request.POST, instance=spell)

        if form.is_valid():
            with transaction.atomic():
                spell = form.save(commit=False)
                if spell.is_homebrew and not request.user.is_staff:
                    spell.is_approved = False
                    messages.info(request, 'Заклинание отправлено на повторное рассмотрение администратором.')

                spell.save()
                Component.objects.filter(spell=spell).delete()
                components = request.POST.getlist('components')
                for comp_type in components:
                    if comp_type in ['V', 'S', 'M']:
                        Component.objects.create(spell=spell, type=comp_type)

                messages.success(request, 'Заклинание успешно обновлено.')
                if request.user.is_staff:
                    return redirect('spell_detail', spell_id=spell_id)
                else:
                    return redirect('spell_list')
    else:
        form = SpellEditForm(instance=spell)
        form.initial['components'] = list(current_components)

    context = {
        'form': form,
        'spell': spell,
        'component_choices': Component.COMPONENT_TYPES,
        'current_components': current_components,
        'is_admin': request.user.is_staff,
    }
    return render(request, 'DnDSite/edit_spell.html', context)


@login_required
def edit_equipment(request, equipment_id):
    equipment = get_object_or_404(Equipment, id=equipment_id)

    if not request.user.is_staff and equipment.created_by != request.user:
        messages.error(request, 'У вас нет прав для редактирования этого снаряжения.')
        return redirect('equipment_detail', equipment_id=equipment_id)

    if request.method == 'POST':
        form = EquipmentEditForm(request.POST, instance=equipment, user=request.user)

        if form.is_valid():
            # Сохраняем снаряжение
            equipment = form.save(commit=False)

            if equipment.is_homebrew and not request.user.is_staff:
                equipment.is_approved = False
                messages.info(request, 'Снаряжение отправлено на повторное рассмотрение администратором.')

            equipment.save()

            messages.success(request, 'Снаряжение успешно обновлено.')
            if request.user.is_staff:
                return redirect('equipment_detail', equipment_id=equipment_id)
            else:
                return redirect('equipment_list')
    else:
        form = EquipmentEditForm(instance=equipment, user=request.user)

    context = {
        'form': form,
        'equipment': equipment,
        'is_admin': request.user.is_staff,
    }
    return render(request, 'DnDSite/edit_equipment.html', context)


@login_required
@user_passes_test(is_admin)
def delete_monster(request, monster_id):
    monster = get_object_or_404(Monster, id=monster_id)

    if request.method == 'POST':
        monster.delete()
        messages.success(request, 'Монстр успешно удален.')
        return redirect('monster_list')

    return render(request, 'DnDSite/confirm_delete.html', {
        'object': monster,
        'type': 'монстра',
        'back_url': 'monster_detail',
        'back_id': monster_id,
    })


@login_required
@user_passes_test(is_admin)
def delete_spell(request, spell_id):
    spell = get_object_or_404(Spell, id=spell_id)

    if request.method == 'POST':
        spell.delete()
        messages.success(request, 'Заклинание успешно удалено.')
        return redirect('spell_list')

    return render(request, 'DnDSite/confirm_delete.html', {
        'object': spell,
        'type': 'заклинания',
        'back_url': 'spell_detail',
        'back_id': spell_id,
    })


@login_required
@user_passes_test(is_admin)
def delete_equipment(request, equipment_id):
    equipment = get_object_or_404(Equipment, id=equipment_id)

    if request.method == 'POST':
        equipment.delete()
        messages.success(request, 'Снаряжение успешно удалено.')
        return redirect('equipment_list')

    return render(request, 'DnDSite/confirm_delete.html', {
        'object': equipment,
        'type': 'снаряжения',
        'back_url': 'equipment_detail',
        'back_id': equipment_id,
    })


@login_required
@user_passes_test(is_admin)
def admin_panel(request):
    total_pending = Monster.objects.filter(is_homebrew=True, is_approved=False).count() + \
                    Spell.objects.filter(is_homebrew=True, is_approved=False).count() + \
                    Equipment.objects.filter(is_homebrew=True, is_approved=False).count()

    context = {
        'pending_monsters': Monster.objects.filter(
            is_homebrew=True,
            is_approved=False
        ).select_related('created_by').order_by('-created_at'),

        'pending_spells': Spell.objects.filter(
            is_homebrew=True,
            is_approved=False
        ).select_related('created_by').order_by('-created_at'),

        'pending_equipment': Equipment.objects.filter(
            is_homebrew=True,
            is_approved=False
        ).select_related('created_by').order_by('-created_at'),

        'recently_approved': {
            'monsters': Monster.objects.filter(
                is_homebrew=True,
                is_approved=True
            ).order_by('-created_at')[:5],
            'spells': Spell.objects.filter(
                is_homebrew=True,
                is_approved=True
            ).order_by('-created_at')[:5],
            'equipment': Equipment.objects.filter(
                is_homebrew=True,
                is_approved=True
            ).order_by('-created_at')[:5],
        },

        'stats': {
            'total_pending': total_pending,
            'total_approved': Monster.objects.filter(is_homebrew=True, is_approved=True).count() +
                              Spell.objects.filter(is_homebrew=True, is_approved=True).count() +
                              Equipment.objects.filter(is_homebrew=True, is_approved=True).count(),
            'monsters_pending': Monster.objects.filter(is_homebrew=True, is_approved=False).count(),
            'spells_pending': Spell.objects.filter(is_homebrew=True, is_approved=False).count(),
            'equipment_pending': Equipment.objects.filter(is_homebrew=True, is_approved=False).count(),
        }
    }

    return render(request, 'DnDSite/admin_panel.html', context)


def custom_login(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Добро пожаловать, {username}!')
                return redirect('index')
    else:
        form = CustomAuthenticationForm()

    return render(request, 'registration/login.html', {'form': form})


# Регистрация
def register(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Регистрация успешна! Добро пожаловать, {user.username}!')
            return redirect('index')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки ниже')
    else:
        form = CustomUserCreationForm()

    return render(request, 'registration/register.html', {'form': form})

@login_required
@user_passes_test(is_admin)
@require_POST
def approve_content(request, content_type, content_id):
    try:
        if content_type == 'monster':
            obj = get_object_or_404(Monster, id=content_id, is_homebrew=True, is_approved=False)
            obj.is_approved = True
            obj.save()
            message = f'Монстр "{obj.name}" одобрен'

        elif content_type == 'spell':
            obj = get_object_or_404(Spell, id=content_id, is_homebrew=True, is_approved=False)
            obj.is_approved = True
            obj.save()
            message = f'Заклинание "{obj.name}" одобрено'

        elif content_type == 'equipment':
            obj = get_object_or_404(Equipment, id=content_id, is_homebrew=True, is_approved=False)
            obj.is_approved = True
            obj.save()
            message = f'Снаряжение "{obj.name}" одобрено'
        else:
            return JsonResponse({'success': False, 'error': 'Неверный тип контента'})

        return JsonResponse({'success': True, 'message': message})

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@login_required
@user_passes_test(is_admin)
@require_POST
def reject_content(request, content_type, content_id):
    try:
        if content_type == 'monster':
            obj = get_object_or_404(Monster, id=content_id, is_homebrew=True)
            name = obj.name
            obj.delete()
            message = f'Монстр "{name}" отклонен.'

        elif content_type == 'spell':
            obj = get_object_or_404(Spell, id=content_id, is_homebrew=True)
            name = obj.name
            obj.delete()
            message = f'Заклинание "{name}" отклонено.'

        elif content_type == 'equipment':
            obj = get_object_or_404(Equipment, id=content_id, is_homebrew=True)
            name = obj.name
            obj.delete()
            message = f'Снаряжение "{name}" отклонено.'
        else:
            return JsonResponse({'success': False, 'error': 'Неверный тип контента'})

        return JsonResponse({'success': True, 'message': message})

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@login_required
@user_passes_test(is_admin)
@require_POST
def moderate_bulk(request):
    action = request.POST.get('action')
    content_type = request.POST.get('content_type')
    items = request.POST.getlist('selected_items')

    if not items:
        messages.error(request, 'Выберите хотя бы один элемент.')
        return redirect('admin_panel')

    approved_count = 0
    rejected_count = 0

    try:
        for item_id in items:
            if action == 'approve':
                if content_type == 'monster':
                    obj = Monster.objects.filter(id=item_id, is_homebrew=True, is_approved=False).first()
                elif content_type == 'spell':
                    obj = Spell.objects.filter(id=item_id, is_homebrew=True, is_approved=False).first()
                elif content_type == 'equipment':
                    obj = Equipment.objects.filter(id=item_id, is_homebrew=True, is_approved=False).first()

                if obj:
                    obj.is_approved = True
                    obj.save()
                    approved_count += 1

            elif action == 'reject':
                if content_type == 'monster':
                    obj = Monster.objects.filter(id=item_id, is_homebrew=True).first()
                elif content_type == 'spell':
                    obj = Spell.objects.filter(id=item_id, is_homebrew=True).first()
                elif content_type == 'equipment':
                    obj = Equipment.objects.filter(id=item_id, is_homebrew=True).first()

                if obj:
                    obj.delete()
                    rejected_count += 1

        if action == 'approve':
            messages.success(request, f'Одобрено {approved_count} {content_type}(s).')
        elif action == 'reject':
            messages.success(request, f'Отклонено {rejected_count} {content_type}(s).')

    except Exception as e:
        messages.error(request, f'Ошибка при обработке: {str(e)}')

    return redirect('admin_panel')

@require_GET
def monster_filter_api(request):
    size = request.GET.get('size', '')
    monster_type = request.GET.get('type', '')

    monsters = Monster.objects.all()

    if size:
        monsters = monsters.filter(size__iexact=size)
    if monster_type:
        monsters = monsters.filter(type__icontains=monster_type)
    monsters = monsters[:20]
    data = []
    for monster in monsters:
        armor_class = monster.armor_classes.first()
        data.append({
            'id': monster.id,
            'name': monster.name,
            'size': monster.size,
            'type': monster.type,
            'hit_points': monster.hit_points,
            'armor_class': armor_class.value if armor_class else 10,
            'url': f'/monsters/{monster.id}/',
        })

    return JsonResponse({
        'success': True,
        'count': len(data),
        'filters': {'size': size, 'type': monster_type},
        'monsters': data,
    })

def custom_logout(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, 'Вы успешно вышли из системы')
    return redirect('index')

@login_required
def admin_login_redirect(request):
    if request.user.is_staff:
        return redirect('/admin/')
    else:
        messages.error(request, 'У вас нет прав доступа к админ-панели')
        return redirect('index')