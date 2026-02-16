from flask import Blueprint, render_template
from flask_security import roles_accepted, current_user
from datebase.classes import db, Menu, Info, History
from configs.app_configs import login_required
from datetime import date, timedelta


statistics = Blueprint('statistics', __name__, template_folder='templates')
@statistics.route('/admin/statistics', methods=['GET', 'POST'])
@login_required
@roles_accepted('admin')
def statistics_page():
    context = {
        'name': current_user.name,
        'surname': current_user.surname
    }
    return render_template('statistics/statistics.html', **context)



statistic_payments = Blueprint('statistic_payments', __name__, template_folder='templates')
@statistic_payments.route('/admin/statistic/payments', methods=['GET', 'POST'])
@login_required
@roles_accepted('admin')
def statistic_payments_page():
    day_get_amount = 0
    week_get_amount = 0
    month_get_amount = 0
    day_pay_amount, day_abonement_amount, day_amount = 0, 0, 0
    week_pay_amount, week_abonement_amount, week_amount = 0, 0, 0
    month_pay_amount, month_abonement_amount, month_amount = 0, 0, 0

    date1 = date.today()
    weekday = date1.weekday()
    first_week = date1 - timedelta(days=weekday)
    menus = db.session.query(Menu).all()
    history = db.session.query(History).all()
    history_user = {}
    for buy in history:
        if buy.menu_id not in history_user:
            history_user[buy.menu_id] = []
        history_user[buy.menu_id].append(buy)

    for menu in menus:
        this_menu = history_user.get(menu.id, [])
        abonement_amount, pay_amount = 0, 0
        for buy in this_menu:
            if buy.cost == 0:
                abonement_amount += 1
            else:
                pay_amount += 1

        if menu.date == date1:
            day_get_amount += menu.get_amount * menu.price
            day_amount += menu.get_amount
            day_abonement_amount += abonement_amount
            day_pay_amount += pay_amount

        for i in range(7):
            current_date = first_week + timedelta(days=i)
            if menu.date == current_date:
                week_get_amount += menu.get_amount * menu.price
                week_amount += menu.get_amount
                week_abonement_amount += abonement_amount
                week_pay_amount += pay_amount

        if menu.date.month == date1.month and menu.date.year == date1.year:
            month_get_amount += menu.get_amount * menu.price
            month_amount += menu.get_amount
            month_abonement_amount += abonement_amount
            month_pay_amount += pay_amount

    try:
        context = {
            'day_get_amount': day_get_amount,
            'week_get_amount': week_get_amount,
            'month_get_amount': month_get_amount,
            'day_pay_amount': day_pay_amount,
            'day_abonement_amount': day_abonement_amount,
            'day_amount': day_amount,
            'week_pay_amount': week_pay_amount,
            'week_abonement_amount': week_abonement_amount,
            'week_amount': week_amount,
            'month_pay_amount': month_pay_amount,
            'month_abonement_amount': month_abonement_amount,
            'month_amount': month_amount,
            'menus': menus,
            'name': current_user.name,
            'surname': current_user.surname
        }
        return render_template('statistics/payments.html', **context)

    finally:
        db.session.close()



statistic_attendance = Blueprint('statistic_attendance', __name__, template_folder='templates')
@statistic_attendance.route('/admin/statistic/attendance', methods=['GET', 'POST'])
@login_required
@roles_accepted('admin')
def statistic_attendance_page():
    menus = db.session.query(Menu).order_by(Menu.date.desc()).all()
    history = db.session.query(History).all()
    menu_statistic = []

    for menu in menus:
        menu_history = [x for x in history if x.menu_id == menu.id]
        menu_user = [x.user_id for x in menu_history]

        classes = {}
        if menu_user:
            inform = db.session.query(Info).filter(Info.user_id.in_(menu_user)).all()
            for info in inform:
                stud_class = info.stud_class if info.stud_class else 'Не указан'
                if stud_class not in classes:
                    classes[stud_class] = 0
                classes[stud_class] += 1

        menu_statistic.append({
            'menu': menu,
            'classes': classes,
        })

    try:
        context = {
            'menu_statistic': menu_statistic,
            'name': current_user.name,
            'surname': current_user.surname
        }
        return render_template('statistics/attendance.html', **context)

    finally:
        db.session.close()