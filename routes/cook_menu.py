from flask import Blueprint, render_template
from flask_security import roles_accepted, current_user
from sqlalchemy.orm import joinedload
from datebase.classes import db, Menu, Dish, Product, Requisition
from configs.app_configs import login_required


cook_menu = Blueprint('cook_menu', __name__, template_folder='templates')
@cook_menu.route('/cook_menu')
@login_required
@roles_accepted('cook')
def cook_menu_page():
    menu = db.session.query(Menu).order_by(Menu.date.asc()).all()
    try:
        context = {
            'menus': menu,
            'name': current_user.name,
            'surname': current_user.surname,
        }

        return render_template('cook_menu.html', **context)

    finally:
        db.session.close()


read_dish = Blueprint('read_dish', __name__, template_folder='templates')
@read_dish.route('/read_dish')
@login_required
@roles_accepted('cook')
def read_dish_page():
    breakfasts = db.session.query(Dish).filter_by(category='breakfasts').options(joinedload(Dish.products)).all()
    salads = db.session.query(Dish).filter_by(category='salads').options(joinedload(Dish.products)).all()
    soups = db.session.query(Dish).filter_by(category='soups').options(joinedload(Dish.products)).all()
    main_dishes = db.session.query(Dish).filter_by(category='main_dishes').options(joinedload(Dish.products)).all()
    drinks = db.session.query(Dish).filter_by(category='drinks').options(joinedload(Dish.products)).all()
    bread = db.session.query(Dish).filter_by(category='bread').options(joinedload(Dish.products)).all()

    db.session.close()

    return render_template('read_dish.html', breakfasts=breakfasts, salads=salads, soups=soups,
                            main_dishes=main_dishes, drinks=drinks, bread=bread)



read_product = Blueprint('read_product', __name__, template_folder='templates')
@read_product.route('/read_product')
@login_required
@roles_accepted('cook')
def read_product_page():
    product = db.session.query(Product).all()
    try:
        context = {
            'products': product,
        }
        return render_template('read_product.html', **context)

    finally:
        db.session.close()



read_requisition = Blueprint('read_requisition', __name__, template_folder='templates')
@read_requisition.route('/read_requisition')
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
