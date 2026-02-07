from flask import Blueprint, render_template, request, redirect
from flask_security import roles_accepted, current_user
from datetime import datetime, date
from configs.app_configs import db, login_required
from datebase.classes import Menu, Dish
from utils.templates_rendering.management.menu import get_dishes_in_categories


add_menu = Blueprint('add_menu', __name__, template_folder='templates')
@add_menu.route('/cook/menu/add', methods=['GET', 'POST'])
@login_required
@roles_accepted('cook')
def add_menu_page():
    if request.method == 'GET':
        dishes = db.session.query(Dish).all()
        db.session.close()

        context = {
            'dishes': dishes,
            'name': current_user.name,
            'surname': current_user.surname,
            'categories': get_dishes_in_categories(dishes),
            'get_category_name': Dish.get_category_name,
        }

        return render_template('menus/adding.html', **context)

    elif request.method == 'POST':
        type = request.form.get('type')
        price = request.form.get('price')
        str_date = request.form.get('date')

        if not all([type, price, str_date]):
            return redirect('/cook/menu/add')

        try:
            date1 = datetime.strptime(str_date, '%Y-%m-%d').date()
        except ValueError:
            return redirect('/cook/menu/add')

        dish_name = []
        for dishes in ['breakfasts', 'salads', 'soups', 'main_dishes', 'drinks', 'bread']:
            dish = request.form.get(dishes)
            if dish:
                dish_name.append(dish)

        if not dish_name or date1 < date.today() or Menu.query.filter_by(type=type, date=date1).first():
            return redirect('/cook/menu/add')

        try:
            dish1 = db.session.query(Dish).filter(Dish.name.in_(dish_name)).all()
            new_menu = Menu(type=type, dishes=dish1, price=price, date=date1)
            db.session.add(new_menu)
            db.session.commit()
            return redirect('/cook/menu')

        finally:
            db.session.close()