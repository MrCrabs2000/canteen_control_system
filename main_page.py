from flask import Blueprint, render_template
from flask_login import login_required


main_page = Blueprint('main_page', __name__, template_folder='templates')
@login_required
@main_page.route('/main')
def mainpage():
    return render_template('main_page.html')