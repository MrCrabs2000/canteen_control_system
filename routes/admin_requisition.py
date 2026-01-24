from flask import Blueprint, render_template, request, redirect
from flask_login import login_required, current_user
from datebase import db_session
from datebase.classes import Product, Requisition


admin_requisition = Blueprint('admin_requisition', __name__, template_folder='templates')
@admin_requisition.route('/admin_requisition', methods=['GET', 'POST'])
@login_required
def admin_requisition_page():
    if current_user.role == 'admin':
        session_db = db_session.create_session()
        requisitions = session_db.query(Requisition).order_by(Requisition.date.desc()).all()
        if request.method == 'GET':
            products = {}
            for requisition in requisitions:
                product = session_db.query(Product).filter_by(id=requisition.product_id).first()
                products[requisition.product_id] = product
            session_db.close()
            return render_template('admin_requisition.html', products=products, requisitions=requisitions)

        elif request.method == 'POST':
            coordination = request.form.get('coordination')
            requisition_id = request.form.get('requisition_id')

            if not all([coordination, requisition_id]):
                session_db.close()
                return redirect('/admin_requisition')

            requisition = session_db.query(Requisition).filter_by(id=requisition_id).first()
            if requisition:
                requisition.coordination = coordination
                try:
                    session_db.commit()
                    return redirect('/admin_menu')

                finally:
                    session_db.close()
            else:
                session_db.close()
                return redirect('/admin_requisition')