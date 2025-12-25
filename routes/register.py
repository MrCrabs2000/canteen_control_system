from flask import Blueprint, render_template, request, redirect, url_for
from werkzeug.security import generate_password_hash
from datebase.classes import User, Info
from datebase import db_session
from flask_login import login_user


register_page = Blueprint('register_page', __name__, template_folder='templates')
@register_page.route('/register', methods=['GET', 'POST'])
def registerpage():
    if request.method == 'POST':
        surname = request.form.get('surname')
        name = request.form.get('name')
        patronymic = request.form.get('patronymic')
        student_class = request.form.get('student_class')
        login = request.form.get('login')
        password = request.form.get('password')
        second_password = request.form.get('second_password')

        session = db_session.create_session()

        user = session.query(User).filter_by(login=login).first()

        if not all([surname, name, patronymic, login, password, second_password, student_class]) or password != second_password or len(password) < 6 or user:
            return redirect('/')
        
        new_user = User(name=name, surname=surname, patronymic=patronymic, login=login, password=generate_password_hash(password))

        session.add(new_user)

        new_student = Info(user_id=new_student.id, stud_class=student_class)

        session.add(new_student)

        try:
            session.commit()
            login_user(new_user)
        except Exception:
            session.rollback()
        finally:
            session.close()
        return redirect('/')
    else:
        return render_template('register.html')

