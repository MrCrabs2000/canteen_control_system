from flask import Blueprint, render_template, request, redirect
from flask_login import login_required, current_user
from datetime import datetime
from datebase import db_session
from datebase.classes import Menu, Dish


add_menu = Blueprint('add_menu', __name__, template_folder='templates')
@add_menu.route('/add_menu', methods=['GET', 'POST'])
@login_required
def add_menu_page():
    if current_user.role == 'admin':
        if request.method == 'GET':
            session_db = db_session.create_session()
            dishes = session_db.query(Dish).all()
            session_db.close()
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

            session_db = db_session.create_session()

            if not all([type, price, dish_name, date1]):
                session_db.close()
                return redirect('/add_menu')

            try:
                dish1 = session_db.query(Dish).filter(Dish.name.in_(dish_name)).all()
                new_menu = Menu(type=type, dishes=dish1, price=price, date=date1)
                session_db.add(new_menu)
                session_db.commit()
                return redirect('/admin_menu')

            finally:
                session_db.close()