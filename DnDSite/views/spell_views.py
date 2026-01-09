from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from ..services import SpellService
from ..constants import SCHOOL_CHOICES_LIST, SORT_OPTIONS_SPELLS
from ..forms import SpellForm, SpellEditForm
from ..models import Spell, Component
from .base_views import is_admin


def spell_list(request):
    search_query = request.GET.get('search', '').strip()
    show_homebrew = request.GET.get('show_homebrew', 'false') == 'true'
    level_filter = request.GET.get('level', '')
    school = request.GET.get('school', '')
    sort_by = request.GET.get('sort', 'name')

    if show_homebrew:
        spells_list = Spell.objects.filter(is_homebrew=True, is_approved=True)
    else:
        spells_list = Spell.objects.filter(is_homebrew=False)

    if level_filter and level_filter.isdigit():
        spells_list = spells_list.filter(level=int(level_filter))

    if search_query:
        search_terms = search_query.split()
        query = Q()

        for term in search_terms:
            if term:
                term_lower = term.lower()
                term_upper = term.upper()
                term_title = term.title()

                query |= Q(name__icontains=term)

                query |= Q(name__icontains=term_lower)
                query |= Q(name__icontains=term_upper)
                query |= Q(name__icontains=term_title)

                query |= Q(desc__icontains=term)
                query |= Q(desc__icontains=term_lower)
                query |= Q(desc__icontains=term_upper)
                query |= Q(desc__icontains=term_title)

        spells_list = spells_list.filter(query).distinct()

        if spells_list.count() == 0 and search_terms:
            from django.db.models.functions import Lower
            spells_list_tmp = spells_list.annotate(
                name_lower=Lower('name'),
                desc_lower=Lower('desc')
            )

            query_lower = Q()
            for term in search_terms:
                term_lower = term.lower()
                query_lower |= Q(name_lower__icontains=term_lower)
                query_lower |= Q(desc_lower__icontains=term_lower)

            spells_list = spells_list_tmp.filter(query_lower)

    if school:
        spells_list = spells_list.filter(school=school)

    if sort_by == 'level':
        spells_list = spells_list.order_by('level', 'name')
    elif sort_by == 'school':
        spells_list = spells_list.order_by('school', 'level', 'name')
    else:
        spells_list = spells_list.order_by('name')

    paginator = Paginator(spells_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    toggle_url = f"{request.path}?show_homebrew={'false' if show_homebrew else 'true'}"

    reset_url = request.path
    if show_homebrew:
        reset_url = f"{request.path}?show_homebrew=true"

    context = {
        'page_obj': page_obj,
        'spells': page_obj.object_list,
        'levels': range(0, 10),
        'selected_level': level_filter,
        'selected_school': school,
        'search_query': search_query,
        'sort_by': sort_by,
        'show_homebrew': show_homebrew,
        'toggle_url': toggle_url,
        'reset_url': reset_url,
        'school_options': SCHOOL_CHOICES_LIST,
        'sort_options': SORT_OPTIONS_SPELLS,
        'filter_params': {
            'show_homebrew': show_homebrew,
            'search': search_query,
            'level': level_filter,
            'school': school,
            'sort': sort_by,
        }
    }
    return render(request, 'DnDSite/spell_list.html', context)

def spell_detail(request, spell_id):
    spell = get_object_or_404(Spell, id=spell_id)
    components = Component.objects.filter(spell=spell)
    similar_spells = SpellService.get_similar_spells(spell, limit=3)
    context = {
        'spell': spell,
        'components': components,
        'can_edit': request.user.is_staff or (request.user == spell.created_by and not spell.is_homebrew),
        'similar_spells': similar_spells,
    }
    return render(request, 'DnDSite/spell_detail.html', context)

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