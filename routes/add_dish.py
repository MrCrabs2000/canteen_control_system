from flask import Blueprint, render_template, request, redirect
from flask_security import roles_accepted
from datebase.classes import Dish, Product, AssociationDishProduct, db
from configs.app_configs import login_required


add_dish = Blueprint('add_dish', __name__, template_folder='templates')
@add_dish.route('/add_dish', methods=['GET', 'POST'])
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
            return redirect('/add_dish')

        for ingredient, amount in zip(ingredients, amounts):
            if not ingredient or not amount or int(amount) <= 0:
                return redirect('/add_dish')

        other_dish = db.session.query(Dish).filter_by(name=name).first()
        if other_dish:
            return redirect('/add_dish')

        try:
            new_dish = Dish(name=name, category=category)
            db.session.add(new_dish)
            db.session.flush()

            for ingredient, amount in zip(ingredients, amounts):
                dish_products = AssociationDishProduct(dish_id=new_dish.id, product_id=int(ingredient), product_amount=int(amount))
                db.session.add(dish_products)

            db.session.commit()

            return redirect('/cook_menu')
        finally:
            db.session.close()



edit_dish = Blueprint('edit_dish', __name__, template_folder='templates')
@edit_dish.route('/<id>/edit_dish', methods=['GET', 'POST'])
@login_required
@roles_accepted('cook')
def edit_dish_page(id):
    dish = db.session.query(Dish).filter_by(id=id).first()
    if request.method == 'POST':
        name = request.form.get('name')
        category = request.form.get('category')

        if not all([name, category]):
            return redirect(f'/{id}/edit_dish')

        dish.name = name
        dish.category = category

        try:
            db.session.commit()
        except Exception:
            db.session.rollback()
        finally:
            db.session.close()

        return redirect('/read_dish')

    context = {
        'name': dish.name,
        'category': dish.category,
    }
    db.session.close()
    return render_template('edit_dish.html', **context)



delete_dish = Blueprint('delete_dish', __name__, template_folder='templates')
@delete_dish.route('/<id>/delete_dish')
@login_required
@roles_accepted('cook')
def delete_dish_page(id):
    dish = db.session.query(Dish).filter_by(id=id).first()
    associatives = db.session.query(AssociationDishProduct).filter_by(dish_id=id).all()
    for associative in associatives:
        db.session.delete(associative)
    db.session.delete(dish)
    db.session.commit()
    db.session.close()

    return redirect('/read_dish')