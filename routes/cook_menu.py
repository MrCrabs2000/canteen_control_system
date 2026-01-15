from flask import Blueprint, render_template
from flask_login import login_required, current_user
from datebase import db_session
from datebase.classes import Menu, Dish


cook_menu = Blueprint('cook_menu', __name__, template_folder='templates')
@cook_menu.route('/cook_menu')
@login_required
def cook_menu_page():
    if current_user.role == 'cook':
        session_db = db_session.create_session()
        menu = session_db.query(Menu).all()
        context = {
            'menus': menu,
        }

        session_db.close()

        return render_template('cook_menu.html', **context)



read_dish = Blueprint('read_dish', __name__, template_folder='templates')
@read_dish.route('/read_dish')
@login_required
def read_dish_page():
    if current_user.role == 'cook':
        session_db = db_session.create_session()
        breakfasts = session_db.query(Dish).filter_by(category='Breakfasts').all()
        salads = session_db.query(Dish).filter_by(category='Salads').all()
        soups = session_db.query(Dish).filter_by(category='Soups').all()
        main_dishes = session_db.query(Dish).filter_by(category='Main dishes').all()
        drinks = session_db.query(Dish).filter_by(category='Drinks').all()
        bread = session_db.query(Dish).filter_by(category='Bread').all()

        session_db.close()

        return render_template('read_dish.html', breakfasts=breakfasts, salads=salads, soups=soups,
                               main_dishes=main_dishes, drinks=drinks, bread=bread)