from flask import Blueprint, render_template, request, redirect
from flask_login import login_required, current_user
from datebase import db_session
from datebase.classes import User, Info
from datetime import datetime, date

food_payment_main = Blueprint('food_payment_main', __name__, template_folder='templates')
@food_payment_main.route('/food_payment', methods=['GET', 'POST'])
@login_required
def food_payment_main_page():
    session_db = db_session.create_session()

    user_info = session_db.query(Info).filter_by(user_id=current_user.id).first()

    context = {
        'balance': user_info.balance
        }

    return render_template('food_payment.html', **context)


edit_balance = Blueprint('edit_balance', __name__, template_folder='templates')
@edit_balance.route("/edit_balance", methods=['GET', 'POST'])
@login_required
def edit_balance_page():
    session_db = db_session.create_session()

    user = session_db.query(User).filter_by(id=current_user.id).first()
    user_info = session_db.query(Info).filter_by(user_id=current_user.id).first()

    if request.method == 'GET':
        context = {
            'balance': user_info.balance
        }

        return render_template('edit_balance.html', **context)

    if request.method == 'POST':
        balance_edit = request.form.get('balance_edit')

        user_info.balance += int(balance_edit)

        session_db.commit()
        session_db.close()

        return redirect("/food_payment")

    return render_template('edit_balance.html')


edit_abonement = Blueprint('edit_abonement', __name__, template_folder='templates')
@edit_abonement.route('/edit_aboniment', methods=['GET', 'POST'])
@login_required
def edit_abonement_page():
    session_db = db_session.create_session()

    user_info = session_db.query(Info).filter_by(user_id=current_user.id).first()

    if request.method == 'GET':
        context = {
            'balance': user_info.balance,
            'today': date.today()
        }

        return render_template('edit_abonement.html', **context)

    if request.method == 'POST':
        datte = request.form.get('date')

        date1 = date.today()
        date2 = datetime.strptime(datte, "%Y-%m-%d").date()

        delta = date2 - date1

        if delta.days > 0:
            cost = 100 * delta.days

            if user_info.balance >= cost:
                user_info.balance -= cost
                user_info.abonement = date2
                session_db.commit()

            else:
                print("Недостаточно средств")

        return redirect("/food_payment")

    return render_template('edit_abonement.html')