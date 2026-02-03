from flask_security import current_user, roles_accepted
from datetime import date
from datebase.classes import db, User, Info, Role
from flask import Blueprint, render_template, request, redirect
from werkzeug.security import generate_password_hash
from flask_security import roles_accepted
import uuid
from configs.app_configs import login_required


read_users = Blueprint('read_users', __name__, template_folder='templates')


@read_users.route('/admin/users')
@login_required
@roles_accepted('admin')
def read_users_page():
    user = db.session.query(User).filter(User.id != current_user.id).all()

    try:
        context = {
            'users': user,
            'name': current_user.name,
            'surname': current_user.surname
        }
        return render_template('users/list.html', **context)

    finally:
        db.session.close()


user_manage = Blueprint('user_manage', __name__, template_folder='templates')


@user_manage.route('/manage/users/<user_id>')
@login_required
@roles_accepted('admin')
def manageuser(user_id):
    user = db.session.query(User).filter_by(id=user_id).first()
    user_info = db.session.query(Info).filter_by(user_id=user_id).first()

    all_roles = db.session.query(Role).all()

    context = {
        'name': current_user.name,
        'surname': current_user.surname,
        'user': user,
        'roles': user.roles,
        'all_roles': all_roles,
        'user_info': user_info
    }

    db.session.close()
    return render_template('users/user.html', **context)


user_del = Blueprint('user_del', __name__, template_folder='templates')


@user_del.route('/manage/users/<user_id>/del')
@login_required
@roles_accepted('admin')
def deluser(user_id):
    user = db.session.query(User).filter_by(id=user_id).first()

    try:
        db.session.delete(user)
        db.session.commit()
    except Exception as e:
        print(f'Ошибка при удалении пользователя: {e}')
        db.session.rollback()
    finally:
        db.session.close()
        return redirect('/admin/users')



user_add = Blueprint('user_add', __name__, template_folder='templates')


@user_add.route('/manage/users/add', methods=['GET', 'POST'])
@login_required
@roles_accepted('admin')
def useradd():
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

        if not all([name, surname, patronymic, login, role, password,
                    second_password]) or password != second_password or len(password) < 6 or user:
            return redirect('/admin/user/add')
        if role == 'cook':
            role = [db.session.query(Role).filter_by(name='cook').first()]
        elif role == 'admin':
            role = [db.session.query(Role).filter_by(name='admin').first()]
        elif role == 'user':
            role = [db.session.query(Role).filter_by(name='user').first()]

        new_user = User(name=name, surname=surname, patronymic=patronymic, login=login, roles=role,
                        password=generate_password_hash(password), active=True, fs_uniquifier=fs_uniquifier)

        db.session.add(new_user)

        try:
            db.session.commit()
        except Exception:
            db.session.rollback()
        finally:
            db.session.close()

        return redirect('/menu')

    else:
        context = {
            'name': current_user.name,
            'surname': current_user.surname
        }
        return render_template('users/adding.html', **context)


user_edit = Blueprint('user_edit', __name__, template_folder='templates')


@user_edit.route('/manage/users/<user_id>/edit', methods=['GET', 'POST'])
@login_required
@roles_accepted('admin')
def edit_user(user_id):
    if request.method == 'GET':
        user = db.session.query(User).filter_by(id=user_id).first()
        user_info = db.session.query(Info).filter_by(user_id=user_id).first()

        context = {
            'name': current_user.name,
            'surname': current_user.surname,
            'user': user,
            'user_info': user_info,
            'roles': user.roles
        }

        db.session.close()
        return render_template('users/edit.html', **context)

    elif request.method == 'POST':
        user = db.session.query(User).filter_by(id=user_id).first()

        name = request.form.get('name')
        surname = request.form.get('surname')
        patronymic = request.form.get('patronymic')
        login = request.form.get('login')
        role = request.form.get('role')

        if name:
            user.name = name
        if surname:
            user.surname = surname
        if patronymic:
            user.patronymic = patronymic
        if login:
            user.login = login

        if role:
            user_role = False
            if role == 'user':
                user_role = db.session.query(Role).filter_by(name='user').first()
            elif role == 'cook':
                user_role = db.session.query(Role).filter_by(name='cook').first()
            elif role == 'admin':
                user_role = db.session.query(Role).filter_by(name='admin').first()

            if user_role:
                user.roles.clear()
                user.roles.append(user_role)

        password = request.form.get('password')
        second_password = request.form.get('second_password')

        if password and second_password and password == second_password and len(password) >= 6:
            user.password = generate_password_hash(password)

        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f'Ошибка изменения пользователя: {e}')
            return redirect(f'/manage/users/{user_id}/edit')
        finally:
            db.session.close()

        return redirect(f'/manage/users/{user_id}')