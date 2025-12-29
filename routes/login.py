from flask import Blueprint, request, redirect, render_template
from flask_login import login_required, login_user
from datebase import db_session
from datebase.classes import User
from werkzeug.security import check_password_hash



login_page = Blueprint('login_page', __name__, template_folder='templates')
@login_required
@login_page.route('/login', methods=['GET', 'POST'])
def loginpage():
    if request.method == 'POST':
        login = request.form.get('login')
        password = request.form.get('password')

        session = db_session.create_session()

        if not all([login, password]):
            return redirect('/')
        
        user = session.query(User).filter_by(login=login).first()

        if not user or not check_password_hash(user.password, password):
            return redirect('/')

        login_user(user)

        session.close()

        return redirect('/')
    else:
        return render_template('auth/login.html', is_not_authenticated=True)