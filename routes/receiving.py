from flask import Blueprint, request, redirect, render_template
from flask_security import login_required, current_user, roles_accepted
from configs.app_configs import db
from datebase.classes import History


receiving = Blueprint('receiving', __name__)
@receiving.route('/receiving', methods=['GET', 'POST'])
@login_required
@roles_accepted('user')
def receiving_view():
    histtory = db.session.query(History).filter_by(user_id=current_user.id).all()

    context = {
        'history_list': histtory[::-1]
    }

    if request.method == 'GET':
        db.session.close()
        return render_template('receiving.html', **context)

    if request.method == 'POST':
        history_ids = request.form.getlist('history_ids')
        return render_template('receiving.html', **context)

