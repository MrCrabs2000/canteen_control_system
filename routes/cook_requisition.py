from flask import Blueprint, render_template, request, redirect
from flask_security import roles_accepted, current_user
from datebase.classes import Product, Requisition, db, Notification, Role
from configs.app_configs import login_required
from datetime import date


cook_requisition = Blueprint('cook_requisition', __name__, template_folder='templates')
@cook_requisition.route('/cook/requisition/add', methods=['GET', 'POST'])
@login_required
@roles_accepted('cook')
def cook_requisition_page():
    if request.method == 'GET':
        products = db.session.query(Product).all()
        products_formated = [(product.name, product.name) for product in products]
        db.session.close()

        context = {
            'name': current_user.name,
            'surname': current_user.surname,
            'products': products,
            'products_formated': products_formated,
        }

        return render_template('requisition/adding.html', **context)

    elif request.method == 'POST':
        name = request.form.get('product_name')
        amount = request.form.get('amount')

        admin_role = db.session.query(Role).filter_by(name='admin').first()
        admins = admin_role.users

        if not all([name, amount]):
            db.session.close()
            return redirect('/cook/requisition/add')

        try:
            product1 = db.session.query(Product).filter(Product.name == name).first()
            new_requisition = Requisition(product=product1, amount=amount, date=date.today())
            db.session.add(new_requisition)
            db.session.flush()
            for admin in admins:
                new_notification = Notification(name='Заявка', text='Вам пришла заявка на покупку продуктов', date=date.today(),
                                        recevier_id=admin.id, requisition_id=new_requisition.id, status=1)
                db.session.add(new_notification)
            db.session.commit()
            return redirect('/cook/requisitions')

        finally:
            db.session.close()