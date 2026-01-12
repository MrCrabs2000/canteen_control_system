from flask import Blueprint, render_template, request, redirect, url_for
from datebase.classes import User, Info
from datebase import db_session
from flask_login import current_user, login_required
from json import loads


profile_edit_page = Blueprint('profile/edit', __name__, template_folder='templates')

@login_required
@profile_edit_page.route('/profile/edit', methods=['POST'])
def profile_edit():
    user_id = current_user.id
    session_db = db_session.create_session()
    user = session_db.query(User).filter_by(id=user_id).first()

    if request.method == 'POST':
        login = request.form.get('login')
        surname = request.form.get('surname')
        name = request.form.get('name')
        patronymic = request.form.get('patronymic')

        if not all([login, surname, name, patronymic]):
            return redirect('/profile')

        user.login = login
        user.surname = surname
        user.name = name
        user.patronymic = patronymic

        if user.role == 'student':
            info = session_db.query(Info).filter_by(user_id=user_id).first()

            if info:
                allergies = request.form.get('allergies')
                preferences = request.form.get('preferences')
                student_class = request.form.get('class')

                if not student_class:
                    return redirect('/profile')
                
                info.stud_class = student_class

                try:
                    info.allergies, info.preferences = allergies, preferences
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
                'allergies': loads(info.allergies) if info.allergies else '',
                'preferences': loads(info.preferences) if info.preferences else ''}

    else:
        context = {
            'name': user.name,
            'surname': user.surname,
            'patronymic': user.patronymic,
            'login': user.login
        }