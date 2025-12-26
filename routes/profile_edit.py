from flask import Blueprint, render_template, request, redirect, url_for
from datebase.classes import User, Info
from datebase import db_session
from json import dumps, loads
from flask_login import current_user, login_required


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
                balance = request.form.get('balance')
                alergies = request.form.get('alergies')
                preferences = request.form.get('preferences')

                if not all([stud_class, balance, alergies, preferences]):
                    return redirect('profile')
                try:
                    alerg = {}
                    prefer = {}

                    a = 0
                    b = 0

                    for elem in alergies.split():
                        alerg[a] = elem
                        a += 1

                    for elem in preferences.split():
                        prefer[b] = elem
                        b += 1

                    info.stud_class, info.balance, info.alergies, info.preferences = stud_class, balance, dumps(alerg), dumps(prefer)

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

        if all([info.stud_class, info.balance, info.alergies, info.preferences]):
            context = {
                'name': user.name,
                'surname': user.surname,
                'patronymic': user.patronymic,
                'class': info.stud_class,
                'login': user.login,
                'balance': info.balance,
                'alergies': loads(info.alergies),
                'preferences': loads(info.preferences)}

        else:
            context = {
                'name': user.name,
                'surname': user.surname,
                'patronymic': user.patronymic,
                'class': '',
                'login': user.login,
                'balance': '',
                'alergies': '',
                'preferences': ''}

    else:
        context = {
            'name': user.name,
            'surname': user.surname,
            'patronymic': user.patronymic,
            'login': user.login,
            'class': '',
            'balance': '',
            'alergies': '',
            'preferences': ''
        }

    session_db.close()
    return render_template('profile_edit.html', **context)