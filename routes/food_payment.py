from flask import Blueprint, render_template
from flask_login import login_required, current_user
from datebase import db_session
from datebase.classes import User, Info


food_payment = Blueprint('food_payment', __name__, template_folder='templates')
@food_payment.route('/food_payment', methods=['GET', 'POST'])
@login_required
def foodpayment():
    session_db = db_session.create_session()
    user = session_db.query(User).filter_by(id=current_user.id).first()
    user_info = session_db.query(Info).filter_by(user_id=current_user.id).first()
    context = {
        'balance': user_info.balance
    }

    return render_template('foodpayment.html', **context)