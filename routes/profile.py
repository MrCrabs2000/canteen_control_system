from flask import Blueprint, render_template
from flask_login import login_required, current_user
from datebase import db_session
from datebase.classes import Info
from json import loads


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
        'class': info.stud_class if info else 'не указан',
        'allergies': loads(info.allergies) if info.allergies and loads(info.allergies) != '' else '',
        'preferences': loads(info.preferences) if info.preferences and loads(info.preferences) != '' else '',
    }

    session_db.close()

    return render_template('profile/view.html', **context)