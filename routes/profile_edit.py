from flask import Blueprint, render_template, request, redirect, url_for
from datebase.classes import User, Info
from datebase import db_session
from flask_login import login_user, current_user


profile_edit_page = Blueprint('profile_edit', __name__, template_folder='templates')
@profile_edit_page.route('/profile_edit', methods=['GET', 'POST'])
def profile_edit():
    if current_user.is_authenticated:
        user_id = current_user.id
        session_db = db_session.create_session()

        user = session_db.query(User).filter_by(id=user_id).first()

        if user.role == 'student':
            info = session_db.query(Info).filter_by(user_id=user_id).first()
            context = {'name': user.name,
                        'surname': user.surname,
                        'patronymic': user.patronymic,
                        'class': info.stud_class,
                        'login': user.login,
                        'balance': info.balance,
                        'alergies': info.alergies,
                        'preferences': info.preferences}

        else:
            context = {'name': user.name,
                        'surname': user.surname,
                       'patronymic': user.patronymic,
                       'login': user.login}

        session_db.close()

        return render_template('profile_edit.html', **context)
    return render_template('base.html')