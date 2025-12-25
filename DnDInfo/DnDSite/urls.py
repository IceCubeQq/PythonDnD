from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),

    path('monsters/', views.monster_list, name='monster_list'),
    path('monsters/<int:monster_id>/', views.monster_detail, name='monster_detail'),
    path('monsters/add/', views.add_monster, name='add_monster'),

    path('spells/', views.spell_list, name='spell_list'),
    path('spells/<int:spell_id>/', views.spell_detail, name='spell_detail'),
    path('spells/add/', views.add_spell, name='add_spell'),

    path('equipment/', views.equipment_list, name='equipment_list'),
    path('equipment/<int:equipment_id>/', views.equipment_detail, name='equipment_detail'),
    path('equipment/add/', views.add_equipment, name='add_equipment'),

    path('admin-panel/', views.admin_panel, name='admin_panel'),

    path('api/monsters/filter/', views.monster_filter_api, name='monster_filter_api'),
]