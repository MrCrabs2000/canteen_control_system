from flask import Blueprint, render_template, request, redirect
from werkzeug.security import generate_password_hash
from flask_login import login_required, current_user
from datebase import db_session
from datebase.classes import User


add_user = Blueprint('add_user', __name__, template_folder='templates')
@add_user.route('/add_user', methods=['GET', 'POST'])
@login_required
def add_user_page():
    if current_user.role == 1:
        if request.method == 'POST':
            name = request.form.get('name')
            surname = request.form.get('surname')
            patronymic = request.form.get('patronymic')
            login = request.form.get('login')
            role = request.form.get('role')
            password = request.form.get('password')
            second_password = request.form.get('second_password')

            session_db = db_session.create_session()
            user = session_db.query(User).filter_by(login=login).first()

            if not all([name, surname, patronymic, login, role, password, second_password]) or password != second_password or len(password) < 6 or user:
                return redirect('/add_user')

            new_user = User(name=name, surname=surname, patronymic=patronymic, login=login, role=role,
                                password=generate_password_hash(password))

            session_db.add(new_user)

            try:
                session_db.commit()
            except Exception:
                session_db.rollback()
            finally:
                session_db.close()

            return redirect('/admin_menu')
        else:
            return render_template('add_user.html')
