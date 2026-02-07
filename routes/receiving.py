from flask import Blueprint, request, render_template, redirect
from flask_security import login_required, current_user, roles_accepted
from configs.app_configs import db
from datebase.classes import History

receiving = Blueprint('receiving', __name__)


@receiving.route('/receiving', methods=['GET', 'POST'])
@login_required
@roles_accepted('user')
def receiving_view():
    filter_date = request.args.get('date', '')

    if request.method == 'POST':
        received_id = request.form.get('mark_received')
        if received_id:
            history = db.session.query(History).filter_by(id=received_id, user_id=current_user.id).first()
            if history:
                history.status = True
                db.session.commit()

        if filter_date:
            return redirect(f'/receiving?date={filter_date}')
        else:
            return redirect('/receiving')

    query = db.session.query(History).filter_by(user_id=current_user.id)
    if filter_date:
        query = query.filter(History.eat_date == filter_date)

    histories = query.order_by(History.id.desc()).all()

    context = {
        'history_list': histories,
        'filter_date': filter_date,
        'name': current_user.name,
        'surname': current_user.surname
    }

    return render_template('menus/receiving.html', **context)