from flask import Blueprint, render_template
from flask_security import login_required, current_user
from sqlalchemy.orm import joinedload
from datebase.classes import db, Menu, Dish, Product


cook_menu = Blueprint('cook_menu', __name__, template_folder='templates')
@cook_menu.route('/cook_menu')
@login_required
def cook_menu_page():
    if current_user.roles[0].name == 'cook':
        menu = db.session.query(Menu).all()
        try:
            context = {
                'menus': menu,
            }

            return render_template('cook_menu.html', **context)

        finally:
            db.session.close()


read_dish = Blueprint('read_dish', __name__, template_folder='templates')
@read_dish.route('/read_dish')
@login_required
def read_dish_page():
    if current_user.roles[0].name == 'cook':
        breakfasts = db.session.query(Dish).filter_by(category='Breakfasts').all()
        salads = db.session.query(Dish).filter_by(category='Salads').all()
        soups = db.session.query(Dish).filter_by(category='Soups').all()
        main_dishes = db.session.query(Dish).filter_by(category='Main dishes').all()
        drinks = db.session.query(Dish).filter_by(category='Drinks').all()
        bread = db.session.query(Dish).filter_by(category='Bread').all()

        db.session.close()

        return render_template('read_dish.html', breakfasts=breakfasts, salads=salads, soups=soups,
                               main_dishes=main_dishes, drinks=drinks, bread=bread)



read_product = Blueprint('read_product', __name__, template_folder='templates')
@read_product.route('/read_product')
@login_required
def read_product_page():
    if current_user.roles[0].name == 'cook':
        product = db.session.query(Product).all()
        try:
            context = {
                'products': product,
            }
            return render_template('read_product.html', **context)

        finally:
            db.session.close()
