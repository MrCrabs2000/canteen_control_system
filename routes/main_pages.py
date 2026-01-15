from flask import Blueprint, render_template
from flask_login import login_required, current_user


main_page = Blueprint('main_page', __name__, template_folder='templates')
@main_page.route('/main')
@login_required
def mainpage():
    context = {
        'name': current_user.name,
        'surname': current_user.surname,
    }
    if current_user.role == 'student':
        return render_template('main_page.html', **context)
    elif current_user.role == 'cook':
        return render_template('main_page.html', **context)
    elif current_user.role == 'admin':
        return render_template('main_page.html', **context)