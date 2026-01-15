from flask import Blueprint, render_template
from flask_login import login_required, current_user
from datebase import db_session
from sqlalchemy.orm import joinedload
from datebase.classes import Menu, Dish
from flask_security import roles_accepted


admin_menu = Blueprint('admin_menu', __name__, template_folder='templates')
@admin_menu.route('/admin_menu')
@login_required
def admin_menu_page():
    if current_user.role == 1:
        session_db = db_session.create_session()
        menu = session_db.query(Menu).all()
        context = {
            'menus': menu,
        }

        session_db.close()

        return render_template('admin_menu.html', **context)


@admin_menu.route('/admin_read_dish')
@login_required
@roles_accepted('admin')
def admin_read_dish():
    if current_user.role == 1:
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