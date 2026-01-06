from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render

from ..forms import FavoriteForm
from ..models import Favorite, Monster, Spell, Equipment


@login_required
def toggle_favorite(request):
    if request.method == 'POST':
        form = FavoriteForm(request.POST)
        if form.is_valid():
            content_type = form.cleaned_data['content_type']
            object_id = form.cleaned_data['object_id']
            action = form.cleaned_data['action']

            if content_type == 'monster':
                obj = get_object_or_404(Monster, id=object_id)
            elif content_type == 'spell':
                obj = get_object_or_404(Spell, id=object_id)
            elif content_type == 'equipment':
                obj = get_object_or_404(Equipment, id=object_id)
            else:
                return JsonResponse({'success': False, 'error': 'Неверный тип контента'})

            if action == 'add':
                favorite, created = Favorite.objects.get_or_create(
                    user=request.user,
                    content_type=content_type,
                    object_id=object_id
                )
                if created:
                    return JsonResponse({'success': True, 'action': 'added', 'message': f'Добавлено в избранное'})
                else:
                    return JsonResponse({'success': False, 'message': 'Уже в избранном'})

            elif action == 'remove':
                deleted, _ = Favorite.objects.filter(
                    user=request.user,
                    content_type=content_type,
                    object_id=object_id
                ).delete()

                if deleted:
                    return JsonResponse({'success': True, 'action': 'removed', 'message': f'Удалено из избранного'})
                else:
                    return JsonResponse({'success': False, 'message': 'Не было в избранном'})

    return JsonResponse({'success': False, 'error': 'Неверный запрос'})

@login_required
def favorites_list(request):
    favorites = Favorite.objects.filter(user=request.user).order_by('-created_at')

    favorite_monsters = favorites.filter(content_type='monster')
    favorite_spells = favorites.filter(content_type='spell')
    favorite_equipment = favorites.filter(content_type='equipment')

    monsters = []
    spells = []
    equipment_items = []

    for fav in favorite_monsters:
        monster = fav.get_object()
        if monster:
            monsters.append(monster)

    for fav in favorite_spells:
        spell = fav.get_object()
        if spell:
            spells.append(spell)

    for fav in favorite_equipment:
        item = fav.get_object()
        if item:
            equipment_items.append(item)

    context = {
        'favorites_count': favorites.count(),
        'monsters': monsters,
        'spells': spells,
        'equipment_items': equipment_items,
        'total_count': len(monsters) + len(spells) + len(equipment_items),
    }

    return render(request, 'DnDSite/favorites_list.html', context)

@login_required
def check_favorite(request, content_type, object_id):
    if not request.user.is_authenticated:
        return JsonResponse({'is_favorite': False})

    is_favorite = Favorite.objects.filter(
        user=request.user,
        content_type=content_type,
        object_id=object_id
    ).exists()

    return JsonResponse({'is_favorite': is_favorite})