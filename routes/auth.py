from flask import Blueprint, render_template, request, redirect
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
from datebase.classes import User, Info, Role
from configs.app_configs import db, login_required
from flask_security import login_user, logout_user


register_page = Blueprint('register_page', __name__, template_folder='templates')
@register_page.route('/register', methods=['GET', 'POST'])
def registerpage():
    if request.method == 'POST':
        surname = request.form.get('surname')
        name = request.form.get('name')
        patronymic = request.form.get('patronymic')
        student_class = request.form.get('class')
        login = request.form.get('login')
        password = request.form.get('password')
        second_password = request.form.get('second_password')

        user = db.session.query(User).filter_by(login=login).first()
        role = db.session.query(Role).filter_by(name='user').first()

        if not all([surname, name, patronymic, login, password, second_password, student_class]) or password != second_password or len(password) < 6 or user:
            return redirect('/')

        fs_uniquifier = str(uuid.uuid4())

        new_user = User(name=name, surname=surname, patronymic=patronymic, login=login, password=generate_password_hash(password), active=True, fs_uniquifier=fs_uniquifier)
        new_user.roles.append(role)

        db.session.add(new_user)

        db.session.flush()
        if student_class:
            new_student = Info(user_id=new_user.id, stud_class=student_class)
        else:
            new_student = Info(user_id=new_user.id, stud_class='')

        db.session.add(new_student)

        try:
            db.session.commit()
            login_user(new_user)
        except Exception as e:
            print(f'Ошибка в регистрации пользователя: {e}')
            db.session.rollback()
        finally:
            db.session.close()

        return redirect('/')
    else:
        return render_template('auth/register.html', is_not_authenticated=True)



login_page = Blueprint('login_page', __name__, template_folder='templates')
@login_page.route('/login', methods=['GET', 'POST'])
def loginpage():
    if request.method == 'POST':
        login = request.form.get('login')
        password = request.form.get('password')

        if not all([login, password]):
            return redirect('/')
        
        user = db.session.query(User).filter_by(login=login).first()

        if not user or not check_password_hash(user.password, password):
            return redirect('/')
        
        login_user(user)
        db.session.close()

        if user.roles[0].name != 'admin':
            return redirect('/')
        else:
            return redirect('admin/menu')
    else:
        return render_template('auth/login.html', is_not_authenticated=True)



exit_page = Blueprint('exit_page', __name__, template_folder='templates')
@exit_page.route('/logout')
@login_required
def exitpage():
    logout_user()
    return redirect('/')