from flask import Blueprint, render_template, request, redirect
from flask_login import login_required, current_user
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
            dishes = request.form.get('dishes')
            price = request.form.get('price')

            session_db = db_session.create_session()
            new_menu = Menu(type=type, price=price)
            session_db.add(new_menu)
            session_db.commit()
            session_db.close()

            return redirect('/admin_menu')