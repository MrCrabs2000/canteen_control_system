from flask import Blueprint, render_template, request, redirect
from werkzeug.security import generate_password_hash
from flask_security import roles_accepted
import uuid
from configs.app_configs import db, login_required
from datebase.classes import User, Role, Info


add_user = Blueprint('add_user', __name__, template_folder='templates')
@add_user.route('/admin/user/add', methods=['GET', 'POST'])
@login_required
@roles_accepted('admin')
def add_user_page():
    if request.method == 'POST':
        name = request.form.get('name')
        surname = request.form.get('surname')
        patronymic = request.form.get('patronymic')
        login = request.form.get('login')
        role = request.form.get('role')
        password = request.form.get('password')
        second_password = request.form.get('second_password')

        user = db.session.query(User).filter_by(login=login).first()
        fs_uniquifier = str(uuid.uuid4())
        if not all([name, surname, patronymic, login, role, password, second_password]) or password != second_password or len(password) < 6 or user:
            return redirect('/admin/user/add')
        if role == 'cook':
            role = [db.session.query(Role).filter_by(name='cook').first()]
        elif role == 'admin':
            role = [db.session.query(Role).filter_by(name='admin').first()]

        new_user = User(name=name, surname=surname, patronymic=patronymic, login=login, roles=role,
                            password=generate_password_hash(password), active=True, fs_uniquifier=fs_uniquifier)

        db.session.add(new_user)

        try:
            db.session.commit()
        except Exception:
            db.session.rollback()
        finally:
            db.session.close()

        return redirect('/admin/menu')
    else:
        return render_template('add_user.html')


edit_user = Blueprint('edit_user', __name__, template_folder='templates')
@edit_user.route('/admin/user/<id>/edit', methods=['GET', 'POST'])
@login_required
@roles_accepted('admin')
def edit_user_page(id):
    user = db.session.query(User).filter_by(id=id).first()
    if request.method == 'GET':
        context = {
            'name': user.name,
            'surname': user.surname,
            'patronymic': user.patronymic,
            'login': user.login,
            'role': user.roles[0].name if user.roles else None,
        }

        db.session.close()
        return render_template('edit_user.html', **context)

    if request.method == 'POST':
        name = request.form.get('name')
        surname = request.form.get('surname')
        patronymic = request.form.get('patronymic')
        login = request.form.get('login')
        role = request.form.get('role')

        if login != user.login:
            other_user = db.session.query(User).filter(User.login == login, User.id != id).first()
            if other_user:
                return redirect(f'/admin/user/{id}/edit')

        if not all([name, surname, patronymic, login, role]) or not user:
            return redirect(f'/admin/user/{id}/edit')

        user.name = name
        user.surname = surname
        user.patronymic = patronymic
        user.login = login

        if role:
            new_role = db.session.query(Role).filter_by(name=role).first()
            if new_role:
                user.roles = [new_role]

        try:
            db.session.commit()
        except Exception:
            db.session.rollback()
        finally:
            db.session.close()

        return redirect('/admin/users')

    db.session.close()
    return render_template('edit_user.html')


delete_user = Blueprint('delete_user', __name__, template_folder='templates')
@delete_user.route('/admin/user/<id>/del')
@login_required
@roles_accepted('admin')
def delete_user_page(id):
    user = db.session.query(User).filter_by(id=id).first()
    info = db.session.query(Info).filter_by(user_id=id).filter(user.roles[0].name == 'user').first()
    if user.roles[0].name == 'user':
        db.session.delete(info)
    db.session.delete(user)
    db.session.commit()
    db.session.close()

    return redirect('/admin/users')