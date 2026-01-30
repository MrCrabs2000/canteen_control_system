from flask import Blueprint, render_template, request, redirect
from flask_security import current_user
from json import loads
from configs.app_configs import db
from datebase.classes import Info, User
from configs.app_configs import login_required


profile_page = Blueprint('profile_page', __name__, template_folder='templates')
@profile_page.route('/profile')
@login_required
def profilepage():
    info = db.session.query(Info).filter_by(user_id=current_user.id).first()
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

    db.session.close()

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
        user = db.session.query(User).filter_by(id=user_id).first()

        if not all([login, surname, name, patronymic]):
            return redirect('/profile')
        
        user.login = login
        user.surname = surname
        user.name = name
        user.patronymic = patronymic
        if user.roles[0].name == 'user':
            info = db.session.query(Info).filter_by(user_id=user_id).first()
            if info:
                allergies = request.form.get('allergies')
                preferences = request.form.get('preferences')
                student_class = request.form.get('class')

                if not student_class:
                    return redirect('/profile')
                
                info.stud_class, info.allergies, info.preferences  = student_class, allergies, preferences

        try:
            db.session.commit()
        except Exception:
            db.session.rollback()
        finally:
            db.session.close()
            return redirect('/profile')