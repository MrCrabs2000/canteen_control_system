from flask import Blueprint, render_template, request, redirect
from flask_security import login_required, current_user
from datebase.classes import Dish, Product, db


add_dish = Blueprint('add_dish', __name__, template_folder='templates')
@add_dish.route('/add_dish', methods=['GET', 'POST'])
@login_required
def add_dish_page():
    if current_user.roles[0].name == 'cook':
        if request.method == 'GET':

            products = db.session.query(Product).all()
            db.session.close()
            return render_template('add_dish.html', products=products)

        elif request.method == 'POST':
            name = request.form.get('name')
            category = request.form.get('category')

            product = request.form.getlist('ingredients')

            if not all([name, category, product]):
                return render_template('add_dish.html')

            other_dish = db.session.query(Dish).filter_by(name=name).first()
            if other_dish:
                return render_template('add_dish.html')

            try:
                product1 = db.session.query(Product).filter(Product.name.in_(product)).all()
                new_dish = Dish(name=name, category=category, products=product1)
                db.session.add(new_dish)
                db.session.commit()

                return redirect('/cook_menu')
            finally:
                db.session.close()



edit_dish = Blueprint('edit_dish', __name__, template_folder='templates')
@edit_dish.route('/<id>/edit_dish', methods=['GET', 'POST'])
@login_required
def edit_dish_page(id):
    if current_user.roles[0].name == 'cook':
        dish = db.session.query(Dish).filter_by(id=id).first()
        if request.method == 'POST':
            name = request.form.get('name')
            category = request.form.get('category')

            if not all([name, category]):
                return redirect('/edit_dish')

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
def delete_dish_page(id):
    if current_user.roles[0].name == 'cook':
        dish = db.session.query(Dish).filter_by(id=id).first()
        db.session.delete(dish)
        db.session.commit()
        db.session.close()

        return redirect('/read_dish')