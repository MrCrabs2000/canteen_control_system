from flask import Blueprint, render_template, request, redirect
from flask_security import login_required, roles_accepted
from datebase.classes import Product, db
from configs.app_configs import login_required


add_product = Blueprint('add_product', __name__, template_folder='templates')
@add_product.route('/add_product', methods=['GET', 'POST'])
@login_required
@roles_accepted('cook')
def add_product_page():
    if request.method == 'GET':
        return render_template('add_product.html')

    elif request.method == 'POST':
        name = request.form.get('name')
        measurement = request.form.get('measurement')

        if not name or not measurement:
            return render_template('add_product.html')

        other_dish = db.session.query(Product).filter_by(name=name).first()
        if other_dish:
            return render_template('add_product.html')

        new_product = Product(name=name, measurement=measurement)
        db.session.add(new_product)
        db.session.commit()
        db.session.close()

        return redirect('/cook_menu')



edit_product = Blueprint('edit_product', __name__, template_folder='templates')
@edit_product.route('/<id>/edit_product', methods=['GET', 'POST'])
@login_required
@roles_accepted('cook')
def edit_product_page(id):
    product = db.session.query(Product).filter_by(id=id).first()
    if request.method == 'POST':
        name = request.form.get('name')
        measurement = request.form.get('measurement')

        if not all([name, measurement]):
            return redirect(f'/{id}/edit_product')

        product.name = name
        product.measurement = measurement

        try:
            db.session.commit()
        except Exception:
            db.session.rollback()
        finally:
            db.session.close()

        return redirect('/read_product')

    context = {
        'name': product.name,
        'measurement': product.measurement,
    }
    db.session.close()
    return render_template('edit_product.html', **context)



delete_product = Blueprint('delete_product', __name__, template_folder='templates')
@delete_product.route('/<id>/delete_product')
@login_required
@roles_accepted('cook')
def delete_product_page(id):
    product = db.session.query(Product).filter_by(id=id).first()
    if product.amount == 0:
        db.session.delete(product)
        db.session.commit()
    db.session.close()

    return redirect('/read_product')