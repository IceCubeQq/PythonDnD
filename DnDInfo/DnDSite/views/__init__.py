from .base_views import is_admin, index
from .auth_views import custom_login, register, custom_logout, admin_login_redirect
from .monster_views import monster_list, monster_detail, add_monster, edit_monster, delete_monster
from .spell_views import spell_list, spell_detail, add_spell, edit_spell, delete_spell
from .equipment_views import equipment_list, equipment_detail, add_equipment, edit_equipment, delete_equipment
from .admin_views import admin_panel, approve_content, reject_content, moderate_bulk
from .favorite_views import toggle_favorite, favorites_list, check_favorite
from .utils_views import monster_filter_api
