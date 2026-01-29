from flask import Blueprint, request, redirect, render_template
from flask_security import login_required, current_user, roles_accepted
from datetime import datetime, date
from configs.app_configs import db
from datebase.classes import Menu, Info, History


history = Blueprint('history', __name__)
@history.route('/history', methods=['GET', 'POST'])
@login_required
@roles_accepted('user')
def history_view():
    histtory = db.session.query(History).filter_by(user_id=current_user.id).all()

    context = {
        'history_list': histtory[::-1]
    }

    db.session.close()
    return render_template('history.html', **context)

