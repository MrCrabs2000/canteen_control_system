from flask import Blueprint, render_template, request, redirect
from flask_security import login_required, current_user, roles_accepted
from datebase.classes import Product, Requisition, db


cook_requisition = Blueprint('cook_requisition', __name__, template_folder='templates')
@cook_requisition.route('/cook_requisition', methods=['GET', 'POST'])
@login_required
@roles_accepted('cook')
def cook_requisition_page():
    if request.method == 'GET':
        product = db.session.query(Product).all()
        db.session.close()
        return render_template('cook_requisition.html', products=product)

    elif request.method == 'POST':
        name = request.form.get('product_name')
        amount = request.form.get('amount')


        if not all([name, amount]):
            db.session.close()
            return redirect('/cook_requisition')

        try:
            product1 = db.session.query(Product).filter(Product.name == name).first()
            new_requisition = Requisition(product=product1, amount=amount)
            db.session.add(new_requisition)
            db.session.commit()
            return redirect('/cook_menu')

        finally:
            db.session.close()