from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),

    path('login/', views.custom_login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.custom_logout, name='logout'),
    path('admin/login/redirect/', views.admin_login_redirect, name='admin_login_redirect'),

    path('monsters/', views.monster_list, name='monster_list'),
    path('monsters/<int:monster_id>/', views.monster_detail, name='monster_detail'),

    path('spells/', views.spell_list, name='spell_list'),
    path('spells/<int:spell_id>/', views.spell_detail, name='spell_detail'),

    path('equipment/', views.equipment_list, name='equipment_list'),
    path('equipment/<int:equipment_id>/', views.equipment_detail, name='equipment_detail'),

    path('monsters/add/', views.add_monster, name='add_monster'),
    path('spells/add/', views.add_spell, name='add_spell'),
    path('equipment/add/', views.add_equipment, name='add_equipment'),

    path('monsters/<int:monster_id>/edit/', views.edit_monster, name='edit_monster'),
    path('spells/<int:spell_id>/edit/', views.edit_spell, name='edit_spell'),
    path('equipment/<int:equipment_id>/edit/', views.edit_equipment, name='edit_equipment'),

    path('monsters/<int:monster_id>/delete/', views.delete_monster, name='delete_monster'),
    path('spells/<int:spell_id>/delete/', views.delete_spell, name='delete_spell'),
    path('equipment/<int:equipment_id>/delete/', views.delete_equipment, name='delete_equipment'),

    path('admin-panel/', views.admin_panel, name='admin_panel'),
    path('admin-panel/approve/<str:content_type>/<int:content_id>/',
         views.approve_content, name='approve_content'),
    path('admin-panel/reject/<str:content_type>/<int:content_id>/',
         views.reject_content, name='reject_content'),
    path('admin-panel/moderate-bulk/',
         views.moderate_bulk, name='moderate_bulk'),

]