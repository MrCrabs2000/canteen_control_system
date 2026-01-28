from flask import Blueprint, request, redirect
from flask_security import login_required, current_user, roles_accepted
from datetime import datetime, date
from configs.app_configs import db
from datebase.classes import Menu, Info, History
from utils.templates_rendering.menu import render_menu_template


menu_redirect = Blueprint('menu_redirect', __name__)
@menu_redirect.route('/menu')
@login_required
@roles_accepted('user')
def menupage():
    return redirect(f'/menu/{date.today()}')


menu_page = Blueprint('menu_page', __name__)

@menu_page.route('/menu/<date_str>', methods=['GET', 'POST'])
@login_required
@roles_accepted('user')
def menupage(date_str):
    ttype = request.args.get('type', 'breakfast')

    datte = datetime.strptime(date_str, '%Y-%m-%d').date()
    menu = db.session.query(Menu).filter_by(date=datte, type=ttype).first()
    user_info = db.session.query(Info).filter_by(user_id=current_user.id).first()

    if request.method == 'GET':
        context = {
            'menu': menu,
            'name': current_user.name,
            'surname': current_user.surname,
            'selected_date': datte,
            'days_back': 7,
            'days_forward': 7
        }

        return render_menu_template(**context)

    elif request.method == 'POST':
        menu_id = request.form.get('menu_id')
        date_today = datetime.strptime(str(date.today()), '%Y-%m-%d').date()
        menu2 = db.session.query(Menu).filter_by(id=int(menu_id)).first()
        flag = True

        context = {
            'menu': menu,
            'name': current_user.name,
            'surname': current_user.surname,
            'selected_date': datte,
            'days_back': 7,
            'days_forward': 7
        }
        for dish in menu2.dishes:
            if dish.amount < 1:
                flag = False
                break
        if flag:
            if user_info.abonement >= datte:

                history = History(
                    user_id=current_user.id,
                    eat_date=date_today,
                    type=ttype,
                    cost=0
                    )

                for dish in menu2.dishes:
                    dish.amount -= 1

                db.session.add(history)
                db.session.commit()
                return render_menu_template(**context)

            elif user_info.balance >= menu2.price:
                user_info.balance -= menu2.price

                history = History(
                    user_id=current_user.id,
                    eat_date=date_today,
                    type=ttype,
                    cost=menu2.price
                )

                for dish in menu2.dishes:
                    dish.amount -= 1

                db.session.add(history)
                db.session.commit()
                return render_menu_template(**context)
        else:
            print('Какое-то блюдо кончилось')
            return render_menu_template(**context)

    return render_menu_template(**context)

