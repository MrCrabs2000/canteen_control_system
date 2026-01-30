from .auth import register_page, login_page, exit_page
from .profile import profile_page, profile_edit_page
from .menu import menu_page, menu_redirect
from .main_pages import main_page
from .admin_menu import admin_menu, admin_read_dish, admin_read_product, read_users
from .add_menu import add_menu
from .cook_menu import cook_menu, read_dish, read_product, read_requisition
from .add_dish import add_dish, edit_dish, delete_dish
from .add_product import add_product, edit_product, delete_product
from .food_payment import food_payment_main, balance_edit, edit_abonement
from .reviews import reviews_main, review_new, review_view
from .add_user import add_user, edit_user, delete_user
from .cook_requisition import cook_requisition
from .admin_requisition import admin_requisition
from .dish import dish_view
from .receiving import receiving


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
    app.register_blueprint(admin_read_product)
    app.register_blueprint(add_menu)
    app.register_blueprint(add_user)
    app.register_blueprint(edit_user)
    app.register_blueprint(delete_user)
    app.register_blueprint(read_users)
    app.register_blueprint(cook_menu)
    app.register_blueprint(read_dish)
    app.register_blueprint(read_product)
    app.register_blueprint(read_requisition)
    app.register_blueprint(add_dish)
    app.register_blueprint(edit_dish)
    app.register_blueprint(delete_dish)
    app.register_blueprint(add_product)
    app.register_blueprint(edit_product)
    app.register_blueprint(delete_product)
    app.register_blueprint(food_payment_main)
    app.register_blueprint(balance_edit)
    app.register_blueprint(edit_abonement)
    app.register_blueprint(reviews_main)
    app.register_blueprint(review_new)
    app.register_blueprint(review_view)
    app.register_blueprint(menu_redirect)
    app.register_blueprint(cook_requisition)
    app.register_blueprint(admin_requisition)
    app.register_blueprint(dish_view)
    app.register_blueprint(receiving)