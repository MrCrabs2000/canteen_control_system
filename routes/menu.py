from flask import Blueprint, render_template
from flask_login import login_required
from sqlalchemy.orm import joinedload
from datetime import date
from flask import request
from datebase import db_session
from datebase.classes import Menu, Dish
from utils.templates_rendering.menu import render_menu_template


menu_page = Blueprint('menu_page', __name__, template_folder='templates')
@menu_page.route('/menu/<date>')
@login_required
def menupage(date):

    type = request.args.get('type')

    session_db = db_session.create_session()
    menu = session_db.query(Menu).options(joinedload(Menu.dishes).joinedload(Dish.products)).filter_by(date=date, type=type).first()

    context = {
        'menu': menu,
    }

    session_db.close()

    return render_menu_template(**context)

