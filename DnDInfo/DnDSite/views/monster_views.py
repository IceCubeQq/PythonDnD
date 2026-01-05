from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.db import transaction
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

from ..constants import SORT_OPTIONS, TYPE_OPTIONS, SIZE_OPTIONS, SIZE_CHOICES, SPEED_EXAMPLES, SPEED_TYPES
from ..forms import MonsterSpeedsForm, ArmorClassForm, MonsterForm, MonsterEditForm
from ..models import Monster, Armor_class, Speed
from .base_views import is_admin, calculate_modifier


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

    size_options = SIZE_OPTIONS
    if show_homebrew:
        raw_types = monsters_list.values_list('type', flat=True).distinct()
        cleaned_types = set()
        for type_name in raw_types:
            if type_name:
                cleaned = type_name.strip().lower()
                if cleaned:
                    cleaned_types.add(cleaned.title())
        unique_types = sorted(list(cleaned_types))
        type_options = [(t, t) for t in unique_types]
    else:
        type_options = TYPE_OPTIONS

    sort_options = SORT_OPTIONS

    paginator = Paginator(monsters_list, 12)
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
        'size_options': size_options,
        'type_options': type_options,
        'sort_options': sort_options,
    }
    return render(request, 'DnDSite/monster_list.html', context)


def monster_detail(request, monster_id):
    monster = get_object_or_404(Monster, id=monster_id)
    armor_classes = Armor_class.objects.filter(monster=monster)
    speeds = Speed.objects.filter(monster=monster)

    # Локальная функция для расчета модификатора (используем другое имя)
    def calc_mod(score):
        return (score - 10) // 2

    context = {
        'monster': monster,
        'armor_classes': armor_classes,
        'speeds': speeds,
        'strength_mod': calc_mod(monster.strength),
        'dexterity_mod': calc_mod(monster.dexterity),
        'constitution_mod': calc_mod(monster.constitution),
        'intelligence_mod': calc_mod(monster.intelligence),
        'wisdom_mod': calc_mod(monster.wisdom),
        'charisma_mod': calc_mod(monster.charisma),
        'can_edit': request.user.is_staff or (request.user == monster.created_by and not monster.is_homebrew),
    }

    return render(request, 'DnDSite/monster_detail.html', context)


@login_required
def add_monster(request):
    if request.method == 'POST':
        form = MonsterForm(request.POST)
        armor_form = ArmorClassForm(request.POST, prefix='armor')
        speeds_form = MonsterSpeedsForm(request.POST)

        if form.is_valid() and armor_form.is_valid() and speeds_form.is_valid():
            with transaction.atomic():
                monster = form.save(commit=False)
                monster.is_homebrew = True
                monster.created_by = request.user
                monster.is_approved = False
                monster.save()

                if armor_form.cleaned_data.get('value'):
                    armor = armor_form.save(commit=False)
                    armor.monster = monster
                    armor.save()
                speeds_list = speeds_form.cleaned_data.get('speeds', [])
                for movement_type, value in speeds_list:
                    Speed.objects.create(
                        monster=monster,
                        movement_type=movement_type,
                        value=value
                    )

            messages.success(request, 'Монстр успешно добавлен. Он будет рассмотрен администратором.')
            return redirect('monster_detail', monster_id=monster.id)
    else:
        form = MonsterForm()
        armor_form = ArmorClassForm(prefix='armor')
        speeds_form = MonsterSpeedsForm()

    context = {
        'form': form,
        'armor_form': armor_form,
        'speeds_form': speeds_form,
    }
    return render(request, 'DnDSite/add_monster.html', context)

@login_required
def edit_monster(request, monster_id):
    monster = get_object_or_404(Monster, id=monster_id)

    if not request.user.is_staff and monster.created_by != request.user:
        messages.error(request, 'У вас нет прав для редактирования этого монстра')
        return redirect('monster_detail', monster_id=monster_id)

    armor_class = monster.armor_classes.first()
    current_speeds = monster.speeds.all()
    speeds_initial = '\n'.join([f"{speed.movement_type}: {speed.value}" for speed in current_speeds])

    if request.method == 'POST':
        form = MonsterEditForm(request.POST, instance=monster, user=request.user)
        armor_form = ArmorClassForm(request.POST, instance=armor_class, prefix='armor')
        speeds_form = MonsterSpeedsForm(request.POST, initial={'speeds': speeds_initial})

        if form.is_valid() and armor_form.is_valid() and speeds_form.is_valid():
            with transaction.atomic():
                monster = form.save(commit=False)
                if monster.is_homebrew and not request.user.is_staff:
                    monster.is_approved = False
                    messages.info(request, 'Монстр отправлен на повторное рассмотрение администратором')

                monster.save()
                armor = armor_form.save(commit=False)
                armor.monster = monster
                if armor.value:
                    armor.save()
                elif armor.pk:
                    armor.delete()
                Speed.objects.filter(monster=monster).delete()
                speeds_list = speeds_form.cleaned_data.get('speeds', [])
                for movement_type, value in speeds_list:
                    Speed.objects.create(
                        monster=monster,
                        movement_type=movement_type,
                        value=value
                    )

                messages.success(request, 'Монстр успешно обновлен')
                if request.user.is_staff:
                    return redirect('monster_detail', monster_id=monster_id)
                else:
                    return redirect('monster_list')
    else:
        form = MonsterEditForm(instance=monster, user=request.user)
        armor_form = ArmorClassForm(instance=armor_class, prefix='armor')
        speeds_form = MonsterSpeedsForm(initial={'speeds': speeds_initial})

    context = {
        'form': form,
        'armor_form': armor_form,
        'speeds_form': speeds_form,
        'monster': monster,
        'is_admin': request.user.is_staff,
    }
    return render(request, 'DnDSite/edit_monster.html', context)

@login_required
@user_passes_test(is_admin)
def delete_monster(request, monster_id):
    monster = get_object_or_404(Monster, id=monster_id)

    if request.method == 'POST':
        monster.delete()
        messages.success(request, 'Монстр успешно удален')
        return redirect('monster_list')

    return render(request, 'DnDSite/confirm_delete.html', {
        'object': monster,
        'type': 'монстра',
        'back_url': 'monster_detail',
        'back_id': monster_id,
    })