from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from datebase import db_session
from datebase.classes import Info, User
from json import loads


profile_page = Blueprint('profile_page', __name__, template_folder='templates')
@profile_page.route('/profile')
@login_required
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



profile_edit_page = Blueprint('profile/edit', __name__, template_folder='templates')
@profile_edit_page.route('/profile/edit', methods=['POST'])
@login_required
def profile_edit():
    if request.method == 'POST':
        login = request.form.get('login')
        surname = request.form.get('surname')
        name = request.form.get('name')
        patronymic = request.form.get('patronymic')

        user_id = current_user.id
        session_db = db_session.create_session()
        user = session_db.query(User).filter_by(id=user_id).first()

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