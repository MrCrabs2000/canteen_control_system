from flask import Blueprint, request, redirect, render_template
from flask_security import login_required, current_user
from datetime import datetime, date
from configs.app_configs import db
from datebase.classes import Menu, Info, History
from utils.templates_rendering.menu import render_menu_template



history = Blueprint('history', __name__)
@history.route('/history')
@login_required
def history_view():
    history = db.session.query(History).filter_by(user_id=current_user.id).all()
    context = {
        'history_list': history[::-1]
    }
    db.session.close()
    return render_template('history.html', **context)

