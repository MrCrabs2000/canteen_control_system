from flask import Blueprint, redirect
from flask_login import login_required, logout_user, current_user

exit_page = Blueprint('exit_page', __name__, template_folder='templates')
@login_required
@exit_page.route('/exit')
def exitpage():
    logout_user()
    return redirect('/')