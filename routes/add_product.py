from flask import Blueprint, render_template, request, redirect
from flask_login import login_required, current_user
from datebase import db_session
from datebase.classes import Product


add_product = Blueprint('add_product', __name__, template_folder='templates')
@add_product.route('/add_product', methods=['GET', 'POST'])
@login_required
def add_product_page():
    if current_user.role == 'cook':
        if request.method == 'GET':
            return render_template('add_product.html')

        elif request.method == 'POST':
            name = request.form.get('name')
            measurement = request.form.get('measurement')

            if not name or not measurement:
                return render_template('add_product.html')

            session_db = db_session.create_session()
            other_dish = session_db.query(Product).filter_by(name=name).first()
            if other_dish:
                return render_template('add_product.html')

            new_product = Product(name=name, measurement=measurement)
            session_db.add(new_product)
            session_db.commit()
            session_db.close()

            return redirect('/cook_menu')



edit_product = Blueprint('edit_product', __name__, template_folder='templates')
@edit_product.route('/<id>/edit_product', methods=['GET', 'POST'])
@login_required
def edit_product_page(id):
    if current_user.role == 'cook':
        session_db = db_session.create_session()
        product = session_db.query(Product).filter_by(id=id).first()
        if request.method == 'POST':
            name = request.form.get('name')
            measurement = request.form.get('measurement')

            if not all([name, measurement]):
                return redirect(f'/{id}/edit_product')

            product.name = name
            product.measurement = measurement

            try:
                session_db.commit()
            except Exception:
                session_db.rollback()
            finally:
                session_db.close()

            return redirect('/read_product')

        context = {
            'name': product.name,
            'measurement': product.measurement,
        }
        session_db.close()
        return render_template('edit_product.html', **context)



delete_product = Blueprint('delete_product', __name__, template_folder='templates')
@delete_product.route('/<id>/delete_product')
@login_required
def delete_product_page(id):
    if current_user.role == 'cook':
        session_db = db_session.create_session()
        product = session_db.query(Product).filter_by(id=id).first()
        if product.amount == 0:
            session_db.delete(product)
            session_db.commit()
        session_db.close()

        return redirect('/read_product')