from flask import Blueprint, render_template, request, redirect
from werkzeug.security import generate_password_hash
from flask_security import login_required, current_user
from configs.app_configs import db
from datebase.classes import User, Role
import uuid


add_user = Blueprint('add_user', __name__, template_folder='templates')
@add_user.route('/add_user', methods=['GET', 'POST'])
@login_required
def add_user_page():
    if current_user.roles[0].name == 'admin':
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
                return redirect('/add_user')
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

            return redirect('/admin_menu')
        else:
            return render_template('add_user.html')
