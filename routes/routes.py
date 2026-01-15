from .auth import register_page, login_page, exit_page
from .profile import profile_page, profile_edit_page
from .menu import menu_page
from .main_pages import main_page
from .admin_menu import admin_menu, admin_read_dish
from .add_user import add_user
from .cook_menu import cook_menu, read_dish
from .add_dish import add_dish, delete_dish
from .add_menu import add_menu


def register_all_blueprints(app):
    app.register_blueprint(main_page)
    app.register_blueprint(register_page)
    app.register_blueprint(exit_page)
    app.register_blueprint(login_page)
    app.register_blueprint(profile_page)
    app.register_blueprint(profile_edit_page)
    app.register_blueprint(menu_page)
    app.register_blueprint(admin_menu)
    app.register_blueprint(admin_read_dish)
    app.register_blueprint(add_user)
    app.register_blueprint(cook_menu)
    app.register_blueprint(read_dish)
    app.register_blueprint(add_dish)
    app.register_blueprint(delete_dish)
    app.register_blueprint(add_menu)