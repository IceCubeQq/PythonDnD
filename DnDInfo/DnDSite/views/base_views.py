from django.shortcuts import render, redirect
from ..models import Monster, Spell, Equipment


def is_admin(user):
    return user.is_authenticated and user.is_staff

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


