from flask import Blueprint, render_template, request, redirect
from flask_security import login_required, current_user, roles_accepted
from configs.app_configs import db
from datebase.classes import Menu, Dish
from datetime import datetime


add_menu = Blueprint('add_menu', __name__, template_folder='templates')
@add_menu.route('/add_menu', methods=['GET', 'POST'])
@login_required
@roles_accepted('admin')
def add_menu_page():
    if request.method == 'GET':
        dishes = db.session.query(Dish).all()
        db.session.close()
        return render_template('add_menu.html', dishes=dishes)

    elif request.method == 'POST':
        type = request.form.get('type')
        price = request.form.get('price')
        date = request.form.get('date')

        date1 = datetime.strptime(date, '%Y-%m-%d').date()

        dish_name = []
        for dishes in ['breakfasts', 'salads', 'soups', 'main_dishes', 'drinks', 'bread']:
            dish = request.form.get(dishes)
            if dish:
                dish_name.append(dish)


        if not all([type, price, dish_name]):
            db.session.close()
            return redirect('/add_menu')

        try:
            dish1 = db.session.query(Dish).filter(Dish.name.in_(dish_name)).all()
            new_menu = Menu(type=type, dishes=dish1, price=price, date=date1)
            db.session.add(new_menu)
            db.session.commit()
            return redirect('/admin_menu')

        finally:
            db.session.close()