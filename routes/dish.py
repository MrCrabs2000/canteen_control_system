from lib2to3.fixes.fix_input import context

from flask import Blueprint, render_template
from flask_security import roles_accepted, current_user
from configs.app_configs import db, login_required
from datebase.classes import Dish


dish_view = Blueprint('dish_view', __name__)

@dish_view.route('/dishes/<dish_id>')
@login_required
@roles_accepted('user', 'admin')
def dishview(dish_id):
    if current_user.roles[0].name == 'user':
        dish = db.session.query(Dish).filter_by(id=dish_id).first()
        context = {
            'name': current_user.name,
            'surname': current_user.surname,
            'dish': dish
        }
        try:
            return render_template('dishes/dish.html', **context)
        except Exception as e:
            print(f'Ошибка в dish.py: {e}')
        finally:
            db.session.close()
    else:
        dish = db.session.query(Dish).filter_by(id=dish_id).first()
        context = {
            'name': current_user.name,
            'surname': current_user.surname,
            'dish': dish
        }
        try:
            return render_template('dishes/dish.html', **context)
        except Exception as e:
            print(f'Ошибка в dish.py: {e}')
        finally:
            db.session.close()
