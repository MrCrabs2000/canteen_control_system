from flask import Blueprint, render_template
from flask_login import login_required, current_user
from datebase import db_session
from datebase.classes import Menu, Dish


admin_menu = Blueprint('admin_menu', __name__, template_folder='templates')
@admin_menu.route('/admin_menu')
@login_required
def admin_menu_page():
    if current_user.role == 'admin':
        session_db = db_session.create_session()
        menu = session_db.query(Menu).all()
        context = {
            'menus': menu,
        }

        session_db.close()
        return render_template('admin_menu.html', **context)



admin_read_dish = Blueprint('admin_read_dish', __name__, template_folder='templates')

@admin_read_dish.route('/admin_read_dish')
@login_required
def admin_read_dish_page():
    if current_user.role == 'admin':
        session_db = db_session.create_session()
        breakfasts = session_db.query(Dish).filter_by(category='Breakfasts').all()
        salads = session_db.query(Dish).filter_by(category='Salads').all()
        soups = session_db.query(Dish).filter_by(category='Soups').all()
        main_dishes = session_db.query(Dish).filter_by(category='Main dishes').all()
        drinks = session_db.query(Dish).filter_by(category='Drinks').all()
        bread = session_db.query(Dish).filter_by(category='Bread').all()

        session_db.close()

        return render_template('admin_read_dish.html', breakfasts=breakfasts, salads=salads, soups=soups,
                               main_dishes=main_dishes, drinks=drinks, bread=bread)