from flask import Blueprint, render_template


register_page = Blueprint('register_page', __name__, template_folder='templates')
@register_page.route('/register')
def registerpage():
    return render_template('register.html')