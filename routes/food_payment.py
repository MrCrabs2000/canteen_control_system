from flask import Blueprint, render_template, request, redirect
from flask_security import current_user, roles_accepted
from datetime import date, timedelta
from configs.app_configs import db, login_required
from datebase.classes import Info, Notification

food_payment_main = Blueprint('payment_main', __name__, template_folder='templates')


@food_payment_main.route('/payment', methods=['GET', 'POST'])
@login_required
@roles_accepted('user')
def food_payment_main_page():
    user_info = db.session.query(Info).filter_by(user_id=current_user.id).first()

    abonement_active = user_info.abonement and user_info.abonement >= date.today()

    context = {
        'balance': user_info.balance,
        'user_abonement': user_info.abonement if abonement_active else None,
        'today': date.today(),
        'name': current_user.name,
        'surname': current_user.surname
    }

    return render_template('payment/payment.html', **context)


balance_edit = Blueprint('edit_balance', __name__, template_folder='templates')


@balance_edit.route("/balance/edit", methods=['GET', 'POST'])
@login_required
@roles_accepted('user')
def edit_balance_page():
    user_info = db.session.query(Info).filter_by(user_id=current_user.id).first()

    if request.method == 'GET':
        context = {
            'balance': user_info.balance,
            'name': current_user.name,
            'surname': current_user.surname
        }
        db.session.close()
        return render_template('payment/balance.html', **context)

    if request.method == 'POST':
        balance_edit = request.form.get('balance_edit')

        user_info.balance += int(balance_edit)

        db.session.commit()
        db.session.close()
        return redirect("/payment")

    db.session.close()
    return render_template('payment/balance.html')


edit_abonement = Blueprint('edit_abonement', __name__, template_folder='templates')


@edit_abonement.route('/abonement/edit', methods=['GET', 'POST'])
@login_required
@roles_accepted('user')
def edit_abonement_page():
    user_info = db.session.query(Info).filter_by(user_id=current_user.id).first()

    abonement_active = user_info.abonement and user_info.abonement >= date.today()

    if request.method == 'GET':
        context = {
            'balance': user_info.balance,
            'today': date.today(),
            'user_abonement': user_info.abonement if abonement_active else None,
            'name': current_user.name,
            'surname': current_user.surname
        }
        db.session.close()
        return render_template('payment/abonement.html', **context)

    if request.method == 'POST':
        period = request.form.get('period')

        if not period:
            db.session.close()
            return redirect("/abonement/edit")

        days = int(period)

        if days == 7:
            cost = 700
        elif days == 14:
            cost = 1300
        elif days == 30:
            cost = 2500
        else:
            cost = 0

        if user_info.balance < cost:
            db.session.close()
            return redirect('/payment')

        current_date = date.today()

        if abonement_active and user_info.abonement >= current_date:
            current_date = user_info.abonement

        new_abonement = current_date + timedelta(days=days)

        user_info.balance -= cost
        user_info.abonement = new_abonement

        try:
            abonement_notifications = Notification.query.filter_by(
                receiver_id=current_user.id,
                type='abonement'
            ).all()

            for notification in abonement_notifications:
                db.session.delete(notification)

        except Exception as e:
            print(f"Ошибка при удалении уведомлений: {e}")

        try:
            db.session.commit()
        except Exception as e:
            print(f'Ошибка в абонементе: {e}')
            db.session.rollback()
        finally:
            db.session.close()

        return redirect("/payment")