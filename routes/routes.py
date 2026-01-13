from .auth import register_page, login_page, exit_page
from .profile import profile_page, profile_edit_page
from .menu import menu_page
from .main_pages import main_page


def register_all_blueprints(app):
    app.register_blueprint(main_page)
    app.register_blueprint(register_page)
    app.register_blueprint(exit_page)
    app.register_blueprint(login_page)
    app.register_blueprint(profile_page)
    app.register_blueprint(profile_edit_page)
    app.register_blueprint(menu_page)