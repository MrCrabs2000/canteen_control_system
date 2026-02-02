from flask import Blueprint, render_template, request, redirect
from flask_security import roles_accepted
from datebase.classes import Menu, Dish, Product, AssociationDishProduct, Review, db
from configs.app_configs import login_required


add_dish = Blueprint('add_dish', __name__, template_folder='templates')
@add_dish.route('/cook/dish/add', methods=['GET', 'POST'])
@login_required
@roles_accepted('cook')
def add_dish_page():
    if request.method == 'GET':
        products = db.session.query(Product).all()
        db.session.close()
        return render_template('add_dish.html', products=products)

    elif request.method == 'POST':
        name = request.form.get('name')
        category = request.form.get('category')
        ingredients = request.form.getlist('ingredients')
        amounts = request.form.getlist('product_amount')

        if not all([name, category, ingredients, amounts]) or len(ingredients) != len(amounts):
            return redirect('/cook/dish/add')

        for ingredient, amount in zip(ingredients, amounts):
            if not ingredient or not amount or int(amount) <= 0:
                return redirect('/cook/dish/add')

        other_dish = db.session.query(Dish).filter_by(name=name).first()
        if other_dish:
            return redirect('/cook/dish/add')

        try:
            new_dish = Dish(name=name, category=category)
            db.session.add(new_dish)
            db.session.flush()

            for ingredient, amount in zip(ingredients, amounts):
                dish_products = AssociationDishProduct(dish_id=new_dish.id, product_id=int(ingredient),
                                                       product_amount=int(amount))
                db.session.add(dish_products)

            db.session.commit()

            return redirect('/cook/menu')
        finally:
            db.session.close()



edit_dish = Blueprint('edit_dish', __name__, template_folder='templates')
@edit_dish.route('/cook/dish/<id>/edit', methods=['GET', 'POST'])
@login_required
@roles_accepted('cook')
def edit_dish_page(id):
    dish = db.session.query(Dish).filter_by(id=id).first()
    if request.method == 'GET':
        context = {
            'name': dish.name,
            'category': dish.category,
        }
        db.session.close()
        return render_template('edit_dish.html', **context)

    if request.method == 'POST':
        name = request.form.get('name')
        category = request.form.get('category')

        if not all([name, category]):
            return redirect(f'/cook/dish/{id}/edit')

        dish.name = name
        dish.category = category

        try:
            db.session.commit()
        except Exception:
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
        except Exception:
            db.session.rollback()
        finally:
            db.session.close()

        return redirect('/cook/dishes')

    return render_template('cook_dish.html', dish=dish)