from flask import Blueprint, render_template, request, redirect
from flask_security import roles_accepted, current_user
from datebase.classes import Product, AssociationDishProduct, Requisition, db
from configs.app_configs import login_required


add_product = Blueprint('add_product', __name__, template_folder='templates')
@add_product.route('/cook/product/add', methods=['GET', 'POST'])
@login_required
@roles_accepted('cook')
def add_product_page():
    if request.method == 'GET':

        context = {
            'name': current_user.name,
            'surname': current_user.surname
        }

        return render_template('/products/adding.html', **context)

    elif request.method == 'POST':
        name = request.form.get('name')
        measurement = request.form.get('measurement')

        if not name or not measurement:
            print(name, measurement)
            return redirect('/cook/product/add')

        other_product = db.session.query(Product).filter_by(name=name).first()
        if other_product:
            print(2)
            return redirect('/cook/product/add')

        new_product = Product(name=name, measurement=measurement)
        db.session.add(new_product)
        db.session.commit()
        db.session.close()

        return redirect('/cook/products')



edit_product = Blueprint('edit_product', __name__, template_folder='templates')
@edit_product.route('/cook/product/<id>/edit', methods=['GET', 'POST'])
@login_required
@roles_accepted('cook')
def edit_product_page(id):
    product = db.session.query(Product).filter_by(id=id).first()
    if request.method == 'GET':
        dishes = db.session.query(Dish).join(AssociationDishProduct).filter(AssociationDishProduct.product_id == id).all()
        requisitions = db.session.query(Requisition).filter_by(product_id=id).all()
        context = {
            'product': product,
            'name': product.name,
            'measurement': product.measurement,
            'amount': product.amount,
            'dishes': dishes,
            'requisitions': requisitions,
        }
        db.session.close()
        return render_template('edit_product.html', **context)

    elif request.method == 'POST':
        name = request.form.get('name')
        measurement = request.form.get('measurement')

        if not all([name, measurement]):
            return redirect(f'/cook/product/{id}/edit')

        product.name = name
        product.measurement = measurement

        try:
            db.session.commit()
        except Exception:
            db.session.rollback()
        finally:
            db.session.close()

        return redirect('/cook/products')



delete_product = Blueprint('delete_product', __name__, template_folder='templates')
@delete_product.route('/cook/product/<id>/del')
@login_required
@roles_accepted('cook')
def delete_product_page(id):
    product = db.session.query(Product).filter_by(id=id).first()
    dishes = db.session.query(AssociationDishProduct).filter_by(product_id=id).all()
    requisitions = db.session.query(Requisition).filter_by(product_id=id).all()
    if product.amount == 0 and not any([dishes, requisitions]):
        db.session.delete(product)
        db.session.commit()
    db.session.close()

    return redirect('/cook/products')