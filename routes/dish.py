from flask import Blueprint, render_template
from flask_security import login_required, current_user, roles_accepted
from configs.app_configs import db
from datebase.classes import Dish


dish_view = Blueprint('dish_view', __name__)

@dish_view.route('/dishes/<dish_id>')
@login_required
@roles_accepted('user')
def dishview(dish_id):
    dish = db.session.query(Dish).filter_by(id=dish_id).first()
    db.session.close()
    return render_template('dish_view.html', dish=dish)