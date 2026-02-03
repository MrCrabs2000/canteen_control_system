from lib2to3.fixes.fix_input import context

from flask import Blueprint, render_template
from flask_security import current_user, roles_accepted
from datebase.classes import db, Menu, Dish, Product, AssociationDishProduct, User, Role
from configs.app_configs import login_required


admin_menu = Blueprint('admin_menu', __name__, template_folder='templates')
@admin_menu.route('/admin/menu')
@login_required
@roles_accepted('admin')
def admin_menu_page():
    try:
        menu = db.session.query(Menu).order_by(Menu.date.asc()).options(
            db.joinedload(Menu.dishes).joinedload(Dish.products).joinedload(AssociationDishProduct.product)).all()
        context = {
            'menus': menu,
            'name': current_user.name,
            'surname': current_user.surname
        }
        return render_template('menus/list.html', **context)

    finally:
        db.session.close()



admin_read_dishes = Blueprint('admin_read_dishes', __name__, template_folder='templates')
@admin_read_dishes.route('/admin/dishes')
@login_required
@roles_accepted('admin')
def admin_read_dishes_page():
    breakfasts = db.session.query(Dish).filter_by(category='breakfasts').options(
        db.joinedload(Dish.products).joinedload(AssociationDishProduct.product)).all()
    salads = db.session.query(Dish).filter_by(category='salads').options(
        db.joinedload(Dish.products).joinedload(AssociationDishProduct.product)).all()
    soups = db.session.query(Dish).filter_by(category='soups').options(
        db.joinedload(Dish.products).joinedload(AssociationDishProduct.product)).all()
    main_dishes = db.session.query(Dish).filter_by(category='main_dishes').options(
        db.joinedload(Dish.products).joinedload(AssociationDishProduct.product)).all()
    drinks = db.session.query(Dish).filter_by(category='drinks').options(
        db.joinedload(Dish.products).joinedload(AssociationDishProduct.product)).all()
    bread = db.session.query(Dish).filter_by(category='bread').options(
        db.joinedload(Dish.products).joinedload(AssociationDishProduct.product)).all()

    db.session.close()

    context = {
        'name': current_user.name,
        'surname': current_user.surname,
        'breakfasts': breakfasts,
        'salads': salads,
        'soups': soups,
        'main_dishes': main_dishes,
        'drinks': drinks,
        'bread': bread
    }

    return render_template('dishes/list.html', ** context)



admin_read_products = Blueprint('admin_read_products', __name__, template_folder='templates')
@admin_read_products.route('/admin/products')
@login_required
@roles_accepted('admin')
def admin_read_product_page():
    product = db.session.query(Product).all()
    try:
        context = {
            'products': product,
            'name': current_user.name,
            'surname': current_user.surname
        }
        return render_template('admin_read_product.html', **context)

    finally:
        db.session.close()



read_users = Blueprint('read_users', __name__, template_folder='templates')
@read_users.route('/admin/users')
@login_required
@roles_accepted('admin')
def read_users_page():
    user = db.session.query(User).filter(User.id != current_user.id).all()
    try:
        context = {
            'users': user,
            'name': current_user.name,
            'surname': current_user.surname
        }
        return render_template('users/list.html', **context)

    finally:
        db.session.close()


read_user = Blueprint('read_user', __name__, template_folder='templates')
@read_user.route('/admin/users/<user_id>')
@login_required
@roles_accepted('admin')
def read_user_page(user_id):
    user = db.session.query(User).filter_by(id=user_id).first()
    try:
        context = {
            'user': user,
            'roles': user.roles,
            'name': current_user.name,
            'surname': current_user.surname
        }
        return render_template('users/user.html', **context)

    finally:
        db.session.close()