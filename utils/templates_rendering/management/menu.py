from flask import render_template


def render_add_menu_template(dishes, name: str, surname: str):
    context = {
        'name': name,
        'surname': surname,
        'categories': {}
    }

    for dish in dishes:
        if dish.category not in context['categories']:
            context['categories'][dish.category] = [(dish.name, dish.name)]
        else:
            context['categories'][dish.category].append((dish.name, dish.name))

    return render_template('management/menus/add.html', **context)