from flask import Blueprint, render_template
from flask_security import roles_accepted, current_user
from datebase.classes import db, Menu, Dish, Product, AssociationDishProduct, Requisition
from configs.app_configs import login_required






cook_menu = Blueprint('cook_menu', __name__, template_folder='templates')
@cook_menu.route('/cook/menu/')
@login_required
@roles_accepted('cook')
def cook_menu_page():
    menu = db.session.query(Menu).order_by(Menu.date.asc()).options(
        db.joinedload(Menu.dishes).joinedload(Dish.products).joinedload(AssociationDishProduct.product)).all()
    try:
        context = {
            'menus': menu,
            'name': current_user.name,
            'surname': current_user.surname,
        }

        return render_template('menus/list.html', **context)

    finally:
        db.session.close()



cook_menus = Blueprint('cook_menus', __name__, template_folder='templates')
@cook_menus.route('/cook/menus')
@login_required
@roles_accepted('cook')
def cook_menus_page():

    context = {
        'name': current_user.name,
        'surname': current_user.surname
    }

    return render_template('menus/list.html', **context)


read_dish = Blueprint('read_dish', __name__, template_folder='templates')
@read_dish.route('/cook/dishes')
@login_required
@roles_accepted('cook')
def read_dish_page():
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

    return render_template('read_dish.html', breakfasts=breakfasts, salads=salads, soups=soups,
                            main_dishes=main_dishes, drinks=drinks, bread=bread)



read_product = Blueprint('read_product', __name__, template_folder='templates')
@read_product.route('/cook/products')
@login_required
@roles_accepted('cook')
def read_product_page():
    product = db.session.query(Product).all()
    try:
        context = {
            'products': product,
            'name': current_user.name,
            'surname': current_user.surname
        }
        print(product)
        return render_template('products/list.html', **context)

    finally:
        db.session.close()



read_requisition = Blueprint('read_requisition', __name__, template_folder='templates')
@read_requisition.route('/cook/requisitions')
@login_required
@roles_accepted('cook')
def read_requisition_page():
    requisitions = db.session.query(Requisition).order_by(Requisition.date.desc()).all()
    products = {}
    for requisition in requisitions:
        product = db.session.query(Product).filter_by(id=requisition.product_id).first()
        products[requisition.product_id] = product
    db.session.close()
    return render_template('read_requisition.html', products=products, requisitions=requisitions)
