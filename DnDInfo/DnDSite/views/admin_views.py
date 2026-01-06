from django.contrib.auth.decorators import user_passes_test, login_required
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.contrib import messages
from ..models import Monster, Spell, Equipment
from .base_views import is_admin


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