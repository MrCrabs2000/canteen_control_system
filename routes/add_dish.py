from flask import Blueprint, render_template, request, redirect
from flask_security import roles_accepted, current_user
from datebase.classes import Menu, Dish, Product, AssociationDishProduct, Review, db, Role, User, Notification
from configs.app_configs import login_required
from datetime import date


add_dish = Blueprint('add_dish', __name__, template_folder='templates')
@add_dish.route('/cook/dish/add', methods=['GET', 'POST'])
@login_required
@roles_accepted('cook')
def add_dish_page():
    if request.method == 'GET':
        products = db.session.query(Product).all()
        products_form = [(product.name, product.name) for product in products]
        db.session.close()

        context = {
            'name': current_user.name,
            'surname': current_user.surname,
            'products': products,
            'products_form': products_form
        }

        return render_template('dishes/adding.html', **context)

    elif request.method == 'POST':
        name = request.form.get('name')
        category = request.form.get('category')
        ingredients_given = request.form.getlist('ingredients')
        amounts_given = request.form.getlist('product_amount')

        ingredients, amounts = [], []

        for i in range(len(ingredients_given)):
            if ingredients_given[i] not in ingredients:
                ingredients.append(ingredients_given[i])
                amounts.append(amounts_given[i])

        if not all([name, category, ingredients, amounts]) or len(ingredients) != len(amounts):
            return redirect('/cook/dish/add')
        
        for ingredient, amount in zip(ingredients, amounts):
            if not ingredient or not amount or int(amount) <= 0:
                return redirect('/cook/dish/add')

        other_dish = db.session.query(Dish).filter_by(name=name).first()
        if other_dish:
            return redirect('/cook/dish/add')

        cook_role = Role.query.filter_by(name='cook').first()
        cooks = None
        if cook_role:
            cooks = db.session.query(User).filter(User.roles.contains(cook_role)).all()
        if cooks:
            for cook in cooks:
                if cook.id != current_user.id:
                    try:
                        new_notification = Notification(name='Добавление',
                                                        text=f'Повар {current_user.name} добавил блюдо',
                                                        date=date.today(),
                                                        receiver_id=cook.id, status=1,
                                                        type='add_dish')
                        db.session.add(new_notification)
                    except Exception as e:
                        print(f'У нас ошибочка уведома при создании Блюда: {e}')
                        db.session.rollback()

        try:
            new_dish = Dish(name=name, category=category)
            db.session.add(new_dish)
            db.session.flush()

            for ingredient, amount in zip(ingredients, amounts):
                id_product = db.session.query(Product).filter_by(name=ingredient).first()
                dish_products = AssociationDishProduct(dish_id=new_dish.id, product_id=int(id_product.id),
                                                       product_amount=int(amount))
                db.session.add(dish_products)
            db.session.commit()

            return redirect('/cook/dishes')
        finally:
            db.session.close()



edit_dish = Blueprint('edit_dish', __name__, template_folder='templates')
@edit_dish.route('/cook/dish/<id>/edit', methods=['GET', 'POST'])
@login_required
@roles_accepted('cook')
def edit_dish_page(id):
    dish = db.session.query(Dish).filter_by(id=id).first()
    if request.method == 'GET':
        menus = db.session.query(Menu).join(Menu.dishes).filter(Dish.id == id).all()
        reviews = db.session.query(Review).filter_by(dish_id=id).all()
        products = db.session.query(Product).all()
        products_form = [(product.name, product.name) for product in products]

        products_selected = []

        for idd in dish.product_ids:
            productt = db.session.query(Product).filter_by(id=idd).first()
            products_selected.append(productt)
        context = {
            'dish': dish,
            'dish_name': dish.name,
            'category': dish.category,
            'amount': dish.amount,
            'menus': menus,
            'reviews': reviews,
            'name': current_user.name,
            'surname': current_user.surname,
            'products': products,
            'products_selected': products_selected,
            'amount_products': len(products_selected),
            'products_amounts': dish.product_amounts,
            'products_form': products_form
        }
        db.session.close()
        return render_template('dishes/manage_dish.html', **context)

    if request.method == 'POST':
        name = request.form.get('name')
        category = request.form.get('category')
        ingredients_given = request.form.getlist('ingredients')
        amounts_given = request.form.getlist('product_amount')

        if not all([name, category, ingredients_given, amounts_given]) or len(ingredients_given) != len(amounts_given):
            return redirect(f'/cook/dish/{id}/edit')

        dish.name = name
        dish.category = category

        for i in range(len(ingredients_given)):
            if ingredients_given:
                product = db.session.query(Product).filter_by(name=ingredients_given[i]).first()
                if product.id not in dish.product_ids:
                    dish_products = AssociationDishProduct(dish_id=dish.id, product_id=int(product.id),
                                                           product_amount=int(amounts_given[i]))
                    db.session.add(dish_products)


        try:
            db.session.commit()
        except Exception as e:
            print(f'Ошибка при добавлении блюда: {e}')
            db.session.rollback()
        finally:
            db.session.close()

        return redirect('/cook/dishes')



delete_dish = Blueprint('delete_dish', __name__, template_folder='templates')
@delete_dish.route('/cook/dish/<id>/del')
@login_required
@roles_accepted('cook')
def delete_dish_page(id):
    dish = db.session.query(Dish).filter_by(id=id).first()
    if dish:
        menus = db.session.query(Menu).join(Menu.dishes).filter(Dish.id == id).all()
        reviews = db.session.query(Review).filter_by(dish_id=id).all()
        associatives = db.session.query(AssociationDishProduct).filter_by(dish_id=id).all()
        if dish.amount == 0 and not any([menus, reviews]):
            for associative in associatives:
                db.session.delete(associative)
            db.session.delete(dish)
            db.session.commit()
    db.session.close()

    return redirect('/cook/dishes')



cook_dish = Blueprint('cook_dish', __name__, template_folder='templates')
@cook_dish.route('/cook/dish/<id>/cook', methods=['GET', 'POST'])
@login_required
@roles_accepted('cook')
def cook_dish_page(id):
    dish = db.session.query(Dish).filter_by(id=id).options(
        db.joinedload(Dish.products).joinedload(AssociationDishProduct.product)).first()
    if request.method == 'POST':
        amount = int(request.form.get('amount'))

        if not amount:
            return redirect(f'/cook/dish/{id}/cook')

        cook = True
        for association in dish.products:
            product_dish_amount = int(association.product_amount)
            product_amount = int(association.product.amount)
            if amount * product_dish_amount > product_amount:
                cook = False
            if not cook:
                break

        if cook:
            dish.amount += amount
            dish.cook_amount += amount
            for association in dish.products:
                product_dish_amount = int(association.product_amount)
                product_amount = int(association.product.amount)
                product_amount -= amount * product_dish_amount
                association.product.amount = product_amount
                association.product.spend_amount += amount * product_dish_amount
        else:
            return redirect(f'/cook/dish/{id}/cook')

        try:
            db.session.commit()
        except Exception as e:
            print(f'Ошибка в add_dish.py: {e}')
            db.session.rollback()
        finally:
            db.session.close()

        return redirect('/cook/dishes')

    return render_template('cook_dish.html', dish=dish)