from flask import Blueprint, render_template, request, redirect
from flask_security import current_user, roles_accepted
from datetime import date
from datebase.classes import db, Menu, Dish, Product, AssociationDishProduct, User, Info
from configs.app_configs import login_required


admin_menu = Blueprint('admin_menu', __name__, template_folder='templates')


@admin_menu.route('/admin/menu')
@login_required
@roles_accepted('admin')
def admin_menu_redirect():
    return redirect(f'/admin/menu/{date.today()}')


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


admin_read_dish = Blueprint('admin_read_dish', __name__, template_folder='templates')


@admin_read_dish.route('/admin/dishes')
@login_required
@roles_accepted('admin')
def admin_read_dish_page():
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

    return render_template('admin_read_dish.html', breakfasts=breakfasts, salads=salads, soups=soups,
                           main_dishes=main_dishes, drinks=drinks, bread=bread, name=current_user.name,
                           surname=current_user.surname)


admin_read_product = Blueprint('admin_read_product', __name__, template_folder='templates')


@admin_read_product.route('/admin/products')
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
    user_info = db.session.query(Info).filter(Info.user_id != current_user.id).all()
    try:
        context = {
            'users': user,
            'name': current_user.name,
            'surname': current_user.surname
        }
        return render_template('users/list.html', **context)

    finally:
        db.session.close()
