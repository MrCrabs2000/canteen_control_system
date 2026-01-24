from flask import Blueprint, render_template, request, redirect
from flask_login import login_required, current_user
from datebase import db_session
from datebase.classes import Product, Requisition


cook_requisition = Blueprint('cook_requisition', __name__, template_folder='templates')
@cook_requisition.route('/cook_requisition', methods=['GET', 'POST'])
@login_required
def cook_requisition_page():
    if current_user.role == 'cook':
        if request.method == 'GET':
            session_db = db_session.create_session()
            product = session_db.query(Product).all()
            session_db.close()
            return render_template('cook_requisition.html', products=product)

        elif request.method == 'POST':
            name = request.form.get('product_name')
            amount = request.form.get('amount')

            session_db = db_session.create_session()

            if not all([name, amount]):
                session_db.close()
                return redirect('/cook_requisition')

            try:
                product1 = session_db.query(Product).filter(Product.name == name).first()
                new_requisition = Requisition(product=product1, amount=amount)
                session_db.add(new_requisition)
                session_db.commit()
                return redirect('/cook_menu')

            finally:
                session_db.close()