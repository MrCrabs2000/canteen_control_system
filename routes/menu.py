from flask import Blueprint, render_template
from flask_login import login_required
from datebase import db_session
from sqlalchemy.orm import joinedload
from datebase.classes import Menu, Dish


menu_page = Blueprint('menu_page', __name__, template_folder='templates')
@menu_page.route('/menu')
@login_required
def menupage():
    session_db = db_session.create_session()

    menus = session_db.query(Menu).options(joinedload(Menu.dishes).joinedload(Dish.products)).all()

    context = {
        'menus': menus,
    }

    session_db.close()

    return render_template('menu_page.html', **context)