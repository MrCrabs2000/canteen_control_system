from flask import Blueprint, render_template
from flask_login import login_required
from datebase import db_session
from sqlalchemy.orm import joinedload
from datebase.classes import Menu, Dish
from functions import get_dates
from datetime import date


menu_page = Blueprint('menu_page', __name__, template_folder='templates')
@login_required
@menu_page.route('/menu')
def menupage():
    session_db = db_session.create_session()

    menus = session_db.query(Menu).options(joinedload(Menu.dishes).joinedload(Dish.products)).all()
    with open('static/menus/menu.txt', 'r', encoding='utf-8') as file:
        for line in file.readlines():
            print(line)
    context = {
        'menus': menus,
    }

    session_db.close()

    return render_template('menu_page.html', **context)



def render_menu_template(menu, name: str = '', surname: str = '', days_back: int = 0, days_forward: int = 0):
    dates = get_dates(days_back, days_forward)

    context = {
        'name': name,
        'surname': surname,
        'today_date': date.today(),
        'dates': dates,
        'selected_date': date.today(),
        'menu': menu
    }

    return render_template('menu/view.html', **context)