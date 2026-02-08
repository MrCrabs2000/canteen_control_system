from flask import Blueprint, request, redirect, url_for
from flask_security import current_user
from datetime import datetime, date
from configs.app_configs import db, login_required
from datebase.classes import Menu, Info, History, Notification
from utils.templates_rendering.menu import render_menu_template

menu_redirect = Blueprint('menu_redirect', __name__)


@menu_redirect.route('/menu')
@login_required
def menupage():
    return redirect(f'/menu/{date.today()}')


menu_page = Blueprint('menu_page', __name__)


@menu_page.route('/menu/<date_str>', methods=['GET', 'POST'])
@login_required
def menupage(date_str):
    ttype = request.args.get('type', 'breakfast')
    date_today = datetime.strptime(str(date.today()), '%Y-%m-%d').date()
    date_ = datetime.strptime(date_str, '%Y-%m-%d').date()

    try:
        datte = datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        return redirect(url_for('menu_page.menupage', date_str=str(date.today())))

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

    elif request.method == 'POST' and date_ >= date_today:
        menu_id = request.form.get('menu_id')

        if not menu_id:
            return redirect(url_for('menu_page.menupage', date_str=date_str))

        menu2 = db.session.query(Menu).filter_by(id=int(menu_id)).first()

        if not menu2:
            return redirect(url_for('menu_page.menupage', date_str=date_str))

        for dish in menu2.dishes:
            if dish.amount < 1:
                print('Какое-то блюдо кончилось')
                return redirect(url_for('menu_page.menupage', date_str=date_str))

        try:
            if user_info.abonement and user_info.abonement >= datte:
                cost = 0
            elif user_info.balance >= menu2.price:
                cost = menu2.price
                user_info.balance -= menu2.price
            else:
                return redirect(url_for('menu_page.menupage', date_str=date_str))

            history = History(
                menu_id=int(menu_id),
                user_id=current_user.id,
                eat_date=date_today,
                type=ttype,
                cost=cost,
                status=False
            )
            new_notification = Notification(
                name='Покупка', text=f'Вы купили меню на {datte}',
                date=date.today(),
                receiver_id=current_user.id,
                status=1,
                type='buying')
            db.session.add(new_notification)

            for dish in menu2.dishes:
                dish.amount -= 1
                dish.give_amount += 1

            menu2.get_amount += 1

            db.session.add(history)
            db.session.commit()

            return redirect(url_for('menu_page.menupage', date_str=date_str))

        except Exception as e:
            print(f'Ошибка в меню: {e}')
            db.session.rollback()
            return redirect(url_for('menu_page.menupage', date_str=date_str))

        finally:
            db.session.close()
    else:
        return redirect(url_for('menu_page.menupage', date_str=date_str))