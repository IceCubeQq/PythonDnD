from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),

    path('login/', custom_login, name='login'),
    path('register/', register, name='register'),
    path('logout/', custom_logout, name='logout'),
    path('admin/login/redirect/', admin_login_redirect, name='admin_login_redirect'),

    path('monsters/', monster_list, name='monster_list'),
    path('monsters/<int:monster_id>/', monster_detail, name='monster_detail'),
    path('monsters/add/', add_monster, name='add_monster'),
    path('monsters/<int:monster_id>/edit/', edit_monster, name='edit_monster'),
    path('monsters/<int:monster_id>/delete/', delete_monster, name='delete_monster'),

    path('spells/', spell_list, name='spell_list'),
    path('spells/<int:spell_id>/', spell_detail, name='spell_detail'),
    path('spells/add/', add_spell, name='add_spell'),
    path('spells/<int:spell_id>/edit/', edit_spell, name='edit_spell'),
    path('spells/<int:spell_id>/delete/', delete_spell, name='delete_spell'),

    path('equipment/', equipment_list, name='equipment_list'),
    path('equipment/<int:equipment_id>/', equipment_detail, name='equipment_detail'),
    path('equipment/add/', add_equipment, name='add_equipment'),
    path('equipment/<int:equipment_id>/edit/', edit_equipment, name='edit_equipment'),
    path('equipment/<int:equipment_id>/delete/', delete_equipment, name='delete_equipment'),

    path('admin-panel/', admin_panel, name='admin_panel'),
    path('admin-panel/approve/<str:content_type>/<int:content_id>/',
         approve_content, name='approve_content'),
    path('admin-panel/reject/<str:content_type>/<int:content_id>/',
         reject_content, name='reject_content'),
    path('admin-panel/moderate-bulk/', moderate_bulk, name='moderate_bulk'),

    path('favorites/toggle/', toggle_favorite, name='toggle_favorite'),
    path('favorites/', favorites_list, name='favorites_list'),
    path('favorites/check/<str:content_type>/<int:object_id>/',
         check_favorite, name='check_favorite'),

    path('api/monsters/filter/', monster_filter_api, name='monster_filter_api'),
]