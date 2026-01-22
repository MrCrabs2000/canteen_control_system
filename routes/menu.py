from flask import Blueprint, request
from flask_security import login_required, current_user
from datetime import datetime
from configs.app_configs import db
from datebase.classes import Menu
from utils.templates_rendering.menu import render_menu_template

menu_page = Blueprint('menu_page', __name__)


@menu_page.route('/menu/<date_str>')
@login_required
def menupage(date_str):
    ttype = request.args.get('type', 'breakfast')

    date = datetime.strptime(date_str, '%Y-%m-%d').date()

    menu = db.session.query(Menu).filter_by(date=date, type=ttype).first()

    context = {
        'menu': menu,
        'name': current_user.name,
        'surname': current_user.surname,
        'selected_date': date,
        'days_back': 7,
        'days_forward': 7
    }

    return render_menu_template(**context)