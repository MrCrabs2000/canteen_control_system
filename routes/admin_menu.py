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
        try:
            menu = session_db.query(Menu).all()
            context = {
                'menus': menu,
            }
            return render_template('admin_menu.html', **context)

        finally:
            session_db.close()




admin_read_dish = Blueprint('admin_read_dish', __name__, template_folder='templates')

@admin_read_dish.route('/admin_read_dish')
@login_required
def admin_read_dish_page():
    if current_user.role == 'admin':
        session_db = db_session.create_session()
        breakfasts = session_db.query(Dish).filter_by(category='breakfasts').all()
        salads = session_db.query(Dish).filter_by(category='salads').all()
        soups = session_db.query(Dish).filter_by(category='soups').all()
        main_dishes = session_db.query(Dish).filter_by(category='main_dishes').all()
        drinks = session_db.query(Dish).filter_by(category='drinks').all()
        bread = session_db.query(Dish).filter_by(category='bread').all()

        session_db.close()

        return render_template('admin_read_dish.html', breakfasts=breakfasts, salads=salads, soups=soups,
                               main_dishes=main_dishes, drinks=drinks, bread=bread)