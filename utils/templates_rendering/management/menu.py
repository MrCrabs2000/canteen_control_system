def get_dishes_in_categories(dishes):
    categories = {}

    for dish in dishes:
        if dish.category not in categories:
            categories[dish.category] = [(dish.name, dish.name)]
        else:
            categories[dish.category].append((dish.name, dish.name))

    return categories
