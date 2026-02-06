from flask import render_template
from datetime import date
from utils.get_dates import get_dates


def render_menu_template(menu, name: str = '', surname: str = '', selected_date: date = date.today(), days_back: int = 0, days_forward: int = 0, **kwargs):
    dates = get_dates(days_back, days_forward)

    context = {
        'name': name,
        'surname': surname,
        'today_date': date.today(),
        'dates': dates,
        'selected_date': selected_date,
        'menu': menu
    }

    return render_template('menus/menu.html', **context, **kwargs)