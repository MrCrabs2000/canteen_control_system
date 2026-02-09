from flask import Blueprint, render_template, request, redirect
from werkzeug.security import generate_password_hash
from flask_security import roles_accepted, current_user
import uuid
from configs.app_configs import db, login_required
from datebase.classes import User, Role, Info, Notification
from datetime import date

add_user = Blueprint('add_user', __name__, template_folder='templates')


@add_user.route('/admin/user/add', methods=['GET', 'POST'])
@login_required
@roles_accepted('admin')
def add_user_page():
    context = {
        'name': current_user.name,
        'surname': current_user.surname
    }

    if request.method == 'POST':
        name = request.form.get('name')
        surname = request.form.get('surname')
        patronymic = request.form.get('patronymic')
        login = request.form.get('login')
        role = request.form.get('role')
        password = request.form.get('password')
        second_password = request.form.get('second_password')

        stud_class = request.form.get('stud_class')
        balance = request.form.get('balance')
        abonement = request.form.get('abonement')

        user_dublicate = db.session.query(User).filter_by(login=login).first()
        if user_dublicate:
            return redirect('/admin/user/add')

        fs_uniquifier = str(uuid.uuid4())

        if (not all([name, surname, patronymic, login, role, password, second_password])
                or password != second_password or len(password) < 6):
            return redirect('/admin/user/add')

        if role == 'cook':
            role_obj = db.session.query(Role).filter_by(name='cook').first()
        elif role == 'admin':
            role_obj = db.session.query(Role).filter_by(name='admin').first()
        else:
            role_obj = db.session.query(Role).filter_by(name='user').first()

        new_user = User(
            name=name,
            surname=surname,
            patronymic=patronymic,
            login=login,
            password=generate_password_hash(password),
            active=True,
            fs_uniquifier=fs_uniquifier
        )

        new_user.roles.append(role_obj)
        db.session.add(new_user)
        db.session.flush()

        if role == 'user':
            new_info = Info(
                user_id=new_user.id,
                stud_class=stud_class if stud_class else '-',
                balance=int(balance) if balance else 0,
                abonement=abonement if abonement else None
            )
            db.session.add(new_info)

        try:
            db.session.commit()
        except Exception as e:
            print(f':Ошибка при добавлении пользователя: {e}')
            db.session.rollback()
            return redirect('/admin/user/add')
        finally:
            db.session.close()

        return redirect('/admin/users')
    else:
        return render_template('users/adding.html', **context)


edit_user = Blueprint('edit_user', __name__, template_folder='templates')


@edit_user.route('/admin/user/<id>/edit', methods=['GET', 'POST'])
@login_required
@roles_accepted('admin')
def edit_user_page(id):
    user = db.session.query(User).filter_by(id=id).first()

    if not user:
        return redirect('/admin/users')

    if request.method == 'GET':
        context = {
            'user': user,
            'name': current_user.name,
            'surname': current_user.surname,
            'role': user.roles[0].name
        }

        try:
            return render_template('users/edit.html', **context)
        except Exception as e:
            print(f'Ошибка при изменении пользователя: {e}')
            return redirect('/admin/users')
        finally:
            db.session.close()

    if request.method == 'POST':
        name = request.form.get('name')
        surname = request.form.get('surname')
        patronymic = request.form.get('patronymic')
        login = request.form.get('login')
        role = request.form.get('role')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')

        stud_class = request.form.get('stud_class')
        balance = request.form.get('balance')
        abonement = request.form.get('abonement')

        if login != user.login:
            other_user = db.session.query(User).filter(User.login == login, User.id != id).first()
            if other_user:
                return redirect(f'/admin/user/{id}/edit')

        if not all([name, surname, patronymic, login, role]):
            return redirect(f'/admin/user/{id}/edit')

        if new_password and confirm_password:
            if new_password != confirm_password or len(new_password) < 6:
                return redirect(f'/admin/user/{id}/edit')

        user_dublicate = db.session.query(User).filter(
            User.id != id,
            User.password == new_password
        ).first()
        if user_dublicate and new_password:
            return redirect(f'/admin/user/{id}/edit')

        role_accepted = db.session.query(Role).filter_by(name=role).first()

        user.name = name
        user.surname = surname
        user.patronymic = patronymic
        user.login = login
        user.roles = []
        user.roles.append(role_accepted)

        if new_password and confirm_password:
            if new_password == confirm_password and len(new_password) >= 6:
                user.password = generate_password_hash(new_password)

        if role == 'user':
            info = db.session.query(Info).filter_by(user_id=id).first()
            if not info:
                info = Info(user_id=id)
                db.session.add(info)

            if stud_class:
                info.stud_class = stud_class
            else:
                info.stud_class = '-'
            if balance:
                info.balance = int(balance)
            else:
                info.balance = 0
            if abonement:
                info.abonement = abonement
            else:
                info.abonement = None

        notification = Notification(
            name='Изменение данных', text='У вас изменения в данных профиля',
            date=date.today(),
            receiver_id=user.id, status=1
        )

        try:
            db.session.add(notification)
            db.session.commit()
        except Exception as e:
            print(f'Ошибка создания уведомления об изменении: {e}')
            db.session.rollback()
            return redirect(f'/admin/user/{id}/edit')
        finally:
            db.session.close()

        return redirect('/admin/users')


delete_user = Blueprint('delete_user', __name__, template_folder='templates')


@delete_user.route('/admin/user/<id>/del')
@login_required
@roles_accepted('admin')
def delete_user_page(id):
    user = db.session.query(User).filter_by(id=id).first()

    if not user:
        return redirect('/admin/users')

    if user.roles and user.roles[0].name == 'user':
        info = db.session.query(Info).filter_by(user_id=id).first()
        if info:
            db.session.delete(info)

    if user:
        db.session.delete(user)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()

    db.session.close()
    return redirect('/admin/users')