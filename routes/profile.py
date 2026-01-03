from flask import Blueprint, render_template
from flask_login import login_required, current_user
from datebase import db_session
from datebase.classes import Info
from functions import json_to_str


profile_page = Blueprint('profile_page', __name__, template_folder='templates')
@login_required
@profile_page.route('/profile')
def profilepage():
    session_db = db_session.create_session()

    info = session_db.query(Info).filter_by(user_id=current_user.id).first()
    context = {
        'name': current_user.name,
        'surname': current_user.surname,
        'patronymic':  current_user.patronymic,
        'login': current_user.login,
        'balance': info.balance if info else '0 рублей',
        'stud_class': info.stud_class if info else 'не указан',
        'allergies': json_to_str(info.allergies) if info.allergies and json_to_str(info.allergies) != '' else 'нет',
        'preferences': json_to_str(info.preferences) if info.preferences and json_to_str(info.preferences) != '' else 'нет',
    }

    session_db.close()

    return render_template('profile_page.html', **context)
