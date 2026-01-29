from flask import Blueprint, render_template
from flask_security import current_user
from configs.app_configs import login_required


main_page = Blueprint('main_page', __name__, template_folder='templates')
@main_page.route('/main')
@login_required
def mainpage():
    context = {
        'name': current_user.name,
        'surname': current_user.surname,
    }
    return render_template('main_page.html', **context)
