from flask import Blueprint, render_template
from flask_login import login_required, current_user
from datebase import db_session
from sqlalchemy.orm import joinedload
from datebase.classes import Menu, Dish, Product, Requisition


cook_menu = Blueprint('cook_menu', __name__, template_folder='templates')
@cook_menu.route('/cook_menu')
@login_required
def cook_menu_page():
    if current_user.role == 'cook':
        session_db = db_session.create_session()
        menu = session_db.query(Menu).all()
        try:
            context = {
                'menus': menu,
            }

            return render_template('cook_menu.html', **context)

        finally:
            session_db.close()



read_dish = Blueprint('read_dish', __name__, template_folder='templates')
@read_dish.route('/read_dish')
@login_required
def read_dish_page():
    if current_user.role == 'cook':
        session_db = db_session.create_session()
        breakfasts = session_db.query(Dish).filter_by(category='breakfasts').options(joinedload(Dish.products)).all()
        salads = session_db.query(Dish).filter_by(category='salads').options(joinedload(Dish.products)).all()
        soups = session_db.query(Dish).filter_by(category='soups').options(joinedload(Dish.products)).all()
        main_dishes = session_db.query(Dish).filter_by(category='main_dishes').options(joinedload(Dish.products)).all()
        drinks = session_db.query(Dish).filter_by(category='drinks').options(joinedload(Dish.products)).all()
        bread = session_db.query(Dish).filter_by(category='bread').options(joinedload(Dish.products)).all()

        session_db.close()

        return render_template('read_dish.html', breakfasts=breakfasts, salads=salads, soups=soups,
                               main_dishes=main_dishes, drinks=drinks, bread=bread)



read_product = Blueprint('read_product', __name__, template_folder='templates')
@read_product.route('/read_product')
@login_required
def read_product_page():
    if current_user.role == 'cook':
        session_db = db_session.create_session()
        product = session_db.query(Product).all()
        try:
            context = {
                'products': product,
            }
            return render_template('read_product.html', **context)

        finally:
            session_db.close()



read_requisition = Blueprint('read_requisition', __name__, template_folder='templates')
@read_requisition.route('/read_requisition')
@login_required
def read_requisition_page():
    if current_user.role == 'cook':
        session_db = db_session.create_session()
        requisitions = session_db.query(Requisition).order_by(Requisition.date.desc()).all()
        products = {}
        for requisition in requisitions:
            product = session_db.query(Product).filter_by(id=requisition.product_id).first()
            products[requisition.product_id] = product
        session_db.close()
        return render_template('read_requisition.html', products=products, requisitions=requisitions)