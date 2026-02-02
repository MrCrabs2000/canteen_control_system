from flask import Blueprint, render_template
from flask_security import roles_accepted
from datebase.classes import User, db
from configs.app_configs import login_required


statistics = Blueprint('statistics', __name__, template_folder='templates')
@statistics.route('/admin/statistics', methods=['GET', 'POST'])
@login_required
@roles_accepted('admin')
def statistics_page():
    return render_template('statistics.html')



statistic_payments = Blueprint('statistic_payments', __name__, template_folder='templates')
@statistic_payments.route('/admin/statistic/payments', methods=['GET', 'POST'])
@login_required
@roles_accepted('admin')
def statistic_payments_page():
    return render_template('statistic_payments.html')



statistic_attendance = Blueprint('statistic_attendance', __name__, template_folder='templates')
@statistic_attendance.route('/admin/statistic/attendance', methods=['GET', 'POST'])
@login_required
@roles_accepted('admin')
def statistic_attendance_page():
    return render_template('statistic_attendance.html')