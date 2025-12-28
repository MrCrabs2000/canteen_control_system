from flask import Blueprint, render_template, request, redirect, url_for
from datebase.classes import User, Info
from datebase import db_session
from flask_login import current_user, login_required
from functions import json_to_str, str_to_json


profile_edit_page = Blueprint('profile_edit', __name__, template_folder='templates')

@login_required
@profile_edit_page.route('/profile_edit', methods=['GET', 'POST'])
def profile_edit():
    user_id = current_user.id
    session_db = db_session.create_session()
    user = session_db.query(User).filter_by(id=user_id).first()

    if request.method == 'POST':
        name = request.form.get('name')
        surname = request.form.get('surname')
        patronymic = request.form.get('patronymic')
        login = request.form.get('login')

        if not all([name, surname, patronymic, login]):
            return redirect('/profile')

        user.name, user.surname, user.patronymic, user.login = name, surname, patronymic, login

        if user.role == 'student':
            info = session_db.query(Info).filter_by(user_id=user_id).first()

            if info:
                stud_class = request.form.get('class')
                alergies = request.form.get('alergies')
                preferences = request.form.get('preferences')

                try:
                    info.stud_class, info.alergies, info.preferences = stud_class, str_to_json(alergies), str_to_json(preferences)
                    session_db.commit()
                except Exception:
                    session_db.rollback()
                finally:
                    session_db.close()
                return redirect('/profile')

        try:
            session_db.commit()
        except Exception:
            session_db.rollback()
        finally:
            session_db.close()

        return redirect(url_for('main_page.mainpage'))

    if user.role == 'student':
        info = session_db.query(Info).filter_by(user_id=user_id).first()
        context = {
                'name': user.name,
                'surname': user.surname,
                'patronymic': user.patronymic,
                'class': info.stud_class,
                'login': user.login,
                'balance': info.balance,
                'alergies': json_to_str(info.alergies),
                'preferences': json_to_str(info.preferences)}

    else:
        context = {
            'name': user.name,
            'surname': user.surname,
            'patronymic': user.patronymic,
            'login': user.login
        }

    session_db.close()
    return render_template('profile_edit.html', **context)