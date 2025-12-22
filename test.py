from flask import Blueprint, render_template
from flask_login import login_required


simple_page = Blueprint('simple_page', __name__, template_folder='templates')
@login_required.user_loader
@simple_page.route('/')
def index():
    return render_template('test.html')