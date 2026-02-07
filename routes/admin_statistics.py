from flask import Blueprint, render_template
from flask_security import roles_accepted, current_user
from datebase.classes import db, Menu, AssociationUserMenus, Info
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
    users = db.session.query(AssociationUserMenus).all()
    users_id = [i.user_id for i in users]
    info_user = {}
    if users_id:
        inform = db.session.query(Info).filter(Info.user_id.in_(users_id)).all()
        for info in inform:
            info_user[info.user_id] = info.abonement

    for menu in menus:
        menu_user = []
        for user in users:
            if menu.id == user.menu_id:
                menu_user.append(user.user_id)
        abonement_amount = 0
        for user_id in menu_user:
            abonement = info_user.get(user_id)
            if abonement and abonement >= menu.date:
                abonement_amount += 1
        pay_amount = len(menu_user) - abonement_amount
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
    users = db.session.query(AssociationUserMenus).all()
    users_id = [i.user_id for i in users]
    menu_statistic = []

    for menu in menus:
        menu_user = []
        for user in users:
            if menu.id == user.menu_id:
                menu_user.append(user.user_id)

        classes = {}
        if users_id:
            inform = db.session.query(Info).filter(Info.user_id.in_(users_id)).all()
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