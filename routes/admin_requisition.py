from flask import Blueprint, render_template, request, redirect
from flask_security import roles_accepted
from datebase.classes import Product, Requisition, db
from configs.app_configs import login_required


admin_requisition = Blueprint('admin_requisition', __name__, template_folder='templates')
@admin_requisition.route('/admin/requisitions', methods=['GET', 'POST'])
@login_required
@roles_accepted('admin')
def admin_requisition_page():
    requisitions = db.session.query(Requisition).order_by(Requisition.date.desc()).all()
    if request.method == 'GET':
        products = {}
        for requisition in requisitions:
            product = db.session.query(Product).filter_by(id=requisition.product_id).first()
            products[requisition.product_id] = product
        db.session.close()
        return render_template('admin_requisition.html', products=products, requisitions=requisitions)

    elif request.method == 'POST':
        coordination = request.form.get('coordination')
        requisition_id = request.form.get('requisition_id')

        if not all([coordination, requisition_id]):
            db.session.close()
            return redirect('/admin/requisitions')

        requisition = db.session.query(Requisition).filter_by(id=requisition_id).first()
        product = db.session.query(Product).filter_by(id=requisition.product_id).first()
        if requisition:
            if coordination == "1":
                product.amount += requisition.amount
                product.buy_amount += requisition.amount
            requisition.coordination = coordination
            try:
                db.session.commit()
            except Exception as e:
                print(e)
                return redirect('/admin_menu')
            finally:
                db.session.close()
            return redirect('/admin/requisition')
        else:
            db.session.close()
            return redirect('/admin/requisitions')