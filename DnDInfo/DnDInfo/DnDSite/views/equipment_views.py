from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from ..services import EquipmentService
from .base_views import is_admin
from ..constants import WEIGHT_OPTIONS, CURRENCY_UNITS, SORT_OPTIONS_EQUIPMENTS
from ..forms import EquipmentForm, EquipmentEditForm
from ..models import Equipment


def equipment_list(request):
    show_homebrew = request.GET.get('show_homebrew', 'false') == 'true'

    if show_homebrew:
        equipment_list = Equipment.objects.filter(is_homebrew=True, is_approved=True)
    else:
        equipment_list = Equipment.objects.filter(is_homebrew=False)

    search = request.GET.get('search', '')
    cost_unit = request.GET.get('cost_unit', '')
    weight_filter = request.GET.get('weight_filter', '')
    sort_by = request.GET.get('sort', 'name')

    if search:
        equipment_list = equipment_list.filter(name__icontains=search)

    if cost_unit:
        equipment_list = equipment_list.filter(cost_unit=cost_unit)

    if weight_filter:
        if weight_filter == 'light':
            equipment_list = equipment_list.filter(weight__lt=5)
        elif weight_filter == 'medium':
            equipment_list = equipment_list.filter(weight__range=(5, 15))
        elif weight_filter == 'heavy':
            equipment_list = equipment_list.filter(weight__gt=15)

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

    currency_options = CURRENCY_UNITS

    weight_options = WEIGHT_OPTIONS

    sort_options = SORT_OPTIONS_EQUIPMENTS
    toggle_url = f"{request.path}?show_homebrew={'false' if show_homebrew else 'true'}"

    reset_url = request.path
    if show_homebrew:
        reset_url = f"{request.path}?show_homebrew=true"

    paginator = Paginator(equipment_list, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'equipment': page_obj.object_list,
        'total_count': equipment_list.count(),
        'search_query': search,
        'selected_cost_unit': cost_unit,
        'selected_weight_filter': weight_filter,
        'sort_by': sort_by,
        'show_homebrew': show_homebrew,
        'currency_options': currency_options,
        'weight_options': weight_options,
        'sort_options': sort_options,
        'toggle_url': toggle_url,
        'reset_url': reset_url,
        'request': request,
    }
    return render(request, 'DnDSite/equipment_list.html', context)

def equipment_detail(request, equipment_id):
    equipment = get_object_or_404(Equipment, id=equipment_id)
    similar_equipment = EquipmentService.get_similar_equipment(equipment, limit=3)
    if equipment.cost_quantity:
        cost_display = f"{equipment.cost_quantity} {equipment.get_cost_unit_display()}"
    else:
        cost_display = "Бесплатно"

    context = {
        'equipment': equipment,
        'cost_display': cost_display,
        'can_edit': request.user.is_staff or (request.user == equipment.created_by and not equipment.is_homebrew),
        'similar_equipment': similar_equipment,
    }
    return render(request, 'DnDSite/equipment_detail.html', context)

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
def edit_equipment(request, equipment_id):
    equipment = get_object_or_404(Equipment, id=equipment_id)

    if not request.user.is_staff and equipment.created_by != request.user:
        messages.error(request, 'У вас нет прав для редактирования этого снаряжения.')
        return redirect('equipment_detail', equipment_id=equipment_id)

    if request.method == 'POST':
        form = EquipmentEditForm(request.POST, instance=equipment, user=request.user)

        if form.is_valid():
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