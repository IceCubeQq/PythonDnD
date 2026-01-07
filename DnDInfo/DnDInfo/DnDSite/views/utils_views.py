from django.http import JsonResponse
from django.views.decorators.http import require_GET

from ..models import Monster


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