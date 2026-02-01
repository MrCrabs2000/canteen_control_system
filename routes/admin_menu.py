from flask import Blueprint, render_template
from flask_security import current_user, roles_accepted
from sqlalchemy.orm import joinedload
from datebase.classes import db, Menu, Dish, Product, User
from configs.app_configs import login_required


admin_menu = Blueprint('admin_menu', __name__, template_folder='templates')
@admin_menu.route('/admin_menu')
@login_required
@roles_accepted('admin')
def admin_menu_page():
    try:
        menu = db.session.query(Menu).order_by(Menu.date.asc()).all()
        context = {
            'menus': menu,
            'name': current_user.name,
            'surname': current_user.surname,
        }
        return render_template('admin_menu.html', **context)

    finally:
        db.session.close()



admin_read_dish = Blueprint('admin_read_dish', __name__, template_folder='templates')
@admin_read_dish.route('/admin_read_dish')
@login_required
@roles_accepted('admin')
def admin_read_dish_page():
    breakfasts = db.session.query(Dish).filter_by(category='breakfasts').options(joinedload(Dish.products)).all()
    salads = db.session.query(Dish).filter_by(category='salads').options(joinedload(Dish.products)).all()
    soups = db.session.query(Dish).filter_by(category='soups').options(joinedload(Dish.products)).all()
    main_dishes = db.session.query(Dish).filter_by(category='main_dishes').options(joinedload(Dish.products)).all()
    drinks = db.session.query(Dish).filter_by(category='drinks').options(joinedload(Dish.products)).all()
    bread = db.session.query(Dish).filter_by(category='bread').options(joinedload(Dish.products)).all()

    db.session.close()

    return render_template('admin_read_dish.html', breakfasts=breakfasts, salads=salads, soups=soups,
                                main_dishes=main_dishes, drinks=drinks, bread=bread)



admin_read_product = Blueprint('admin_read_product', __name__, template_folder='templates')
@admin_read_product.route('/admin_read_product')
@login_required
@roles_accepted('admin')
def admin_read_product_page():
    product = db.session.query(Product).all()
    try:
        context = {
            'products': product,
        }
        return render_template('admin_read_product.html', **context)

    finally:
        db.session.close()



read_users = Blueprint('read_users', __name__, template_folder='templates')
@read_users.route('/read_users')
@login_required
@roles_accepted('admin')
def read_users_page():
    user = db.session.query(User).filter(User.id!=current_user.id).all()
    try:
        context = {
            'users': user,
        }
        return render_template('read_users.html', **context)

    finally:
        db.session.close()