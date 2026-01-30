from flask import Blueprint, render_template, request, redirect
from flask_security import current_user, roles_accepted
from datetime import datetime, date
from configs.app_configs import db, login_required
from datebase.classes import Info


food_payment_main = Blueprint('food_payment_main', __name__, template_folder='templates')

@food_payment_main.route('/food_payment', methods=['GET', 'POST'])
@login_required
@roles_accepted('user')
def food_payment_main_page():

    user_info = db.session.query(Info).filter_by(user_id=current_user.id).first()

    context = {
        'balance': user_info.balance
        }

    return render_template('food_payment.html', **context)


edit_balance = Blueprint('edit_balance', __name__, template_folder='templates')

@edit_balance.route("/edit_balance", methods=['GET', 'POST'])
@login_required
@roles_accepted('user')
def edit_balance_page():

    user_info = db.session.query(Info).filter_by(user_id=current_user.id).first()

    if request.method == 'GET':
        context = {
            'balance': user_info.balance
        }
        db.session.close()
        return render_template('edit_balance.html', **context)

    if request.method == 'POST':
        balance_edit = request.form.get('balance_edit')

        user_info.balance += int(balance_edit)

        db.session.commit()
        db.session.close()
        db.session.close()
        return redirect("/food_payment")
    db.session.close()
    return render_template('edit_balance.html')


edit_abonement = Blueprint('edit_abonement', __name__, template_folder='templates')
@edit_abonement.route('/edit_aboniment', methods=['GET', 'POST'])
@login_required
@roles_accepted('user')
def edit_abonement_page():

    user_info = db.session.query(Info).filter_by(user_id=current_user.id).first()

    if request.method == 'GET':
        context = {
            'balance': user_info.balance,
            'today': date.today()
        }
        db.session.close()
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

                try:
                    db.session.commit()
                except Exception as e:
                    print(e)
                    db.session.rollback()
                finally:
                    db.session.close()

            else:
                print("Недостаточно средств")
                db.session.close()

        return redirect("/food_payment")

    db.session.close()
    return render_template('edit_abonement.html')