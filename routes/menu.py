from flask import Blueprint
from flask_login import login_required
from flask import request
from datebase import db_session
from datebase.classes import Menu
from utils.templates_rendering.menu import render_menu_template

menu_page = Blueprint('menu_page', __name__)


@menu_page.route('/menu/<date>')
@login_required
def menupage(date):
    type = request.args.get('type')

    session_db = db_session.create_session()
    menu = session_db.query(Menu).filter_by(date=date, type=type).first()

    session_db.close()

    context = {
        'menu': menu,
        'date': date,
        'type': type
    }

    return render_menu_template(context)