from flask import Blueprint, render_template, request, redirect
from werkzeug.security import generate_password_hash
from flask_login import login_required, current_user
from datebase import db_session
from datebase.classes import User, Info


add_user = Blueprint('add_user', __name__, template_folder='templates')
@add_user.route('/add_user', methods=['GET', 'POST'])
@login_required
def add_user_page():
    if current_user.role == 'admin':
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


edit_user = Blueprint('edit_user', __name__, template_folder='templates')
@edit_user.route('/<id>/edit_user', methods=['GET', 'POST'])
@login_required
def edit_user_page(id):
    if current_user.role == 'admin':
        session_db = db_session.create_session()
        user = session_db.query(User).filter_by(id=id).first()
        if request.method == 'GET':
            context = {
                'name': user.name,
                'surname': user.surname,
                'patronymic': user.patronymic,
                'login': user.login,
                'role': user.role,
            }

            session_db.close()
            return render_template('edit_user.html', **context)

        if request.method == 'POST':
            name = request.form.get('name')
            surname = request.form.get('surname')
            patronymic = request.form.get('patronymic')
            login = request.form.get('login')
            role = request.form.get('role')

            if not role:
                role = user.role

            if login != user.login:
                other_user = session_db.query(User).filter(User.login == login, User.id != id).first()
                if other_user:
                    return redirect(f'/{id}/edit_user')

            if not all([name, surname, patronymic, login, role]) or not user:
                return redirect(f'/{id}/edit_user')

            user.name = name
            user.surname = surname
            user.patronymic = patronymic
            user.login = login
            user.role = role

            try:
                session_db.commit()
            except Exception:
                session_db.rollback()
            finally:
                session_db.close()

            return redirect('/read_users')

        session_db.close()
        return render_template('edit_user.html')


delete_user = Blueprint('delete_user', __name__, template_folder='templates')
@delete_user.route('/<id>/delete_user')
@login_required
def delete_user_page(id):
    if current_user.role == 'admin':
        session_db = db_session.create_session()
        user = session_db.query(User).filter_by(id=id).first()
        info = session_db.query(Info).filter_by(user_id=id).filter(user.role == 'student').first()
        session_db.delete(user)
        if user.role == 'student':
            session_db.delete(info)
        session_db.commit()
        session_db.close()

        return redirect('/read_users')