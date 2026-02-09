from itertools import product

from flask import Blueprint, render_template, request, redirect
from flask_security import roles_accepted, current_user
from datebase.classes import Product, Requisition, db, Notification
from configs.app_configs import login_required
from datetime import date

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

        requisitions_list = []
        for requisition in requisitions:
            if requisition.coordination == 0:
                requisitions_list.append(requisition)

        context = {
            'products': products,
            'requisitions': requisitions_list[::-1],
            'name': current_user.name,
            'surname': current_user.surname,
            'role': current_user.roles[0].name
        }
        db.session.close()
        return render_template('requisition/admin.html', **context)

    elif request.method == 'POST':
        action = request.form.get('action')
        requisition_id = request.form.get('requisition_id')


        if not all([action, requisition_id]):
            db.session.close()
            return redirect('/admin/requisitions')

        requisition = db.session.query(Requisition).filter_by(id=requisition_id).first()
        if not requisition:
            return redirect('/admin/requisitions')

        if action == 'approved':
            coordination = 1
            product = db.session.query(Product).filter_by(id=requisition.product_id).first()
            if product:
                product.amount += requisition.amount
                product.buy_amount += requisition.amount
        elif action == 'rejected':
            coordination = 2
        else:
            db.session.close()
            return redirect('/admin/requisitions')



        requisition = db.session.query(Requisition).filter_by(id=requisition_id).first()

        if requisition:
            requisition.coordination = coordination

            new_notification = Notification(name='Заявка', text='У вас изменения в статусе заявки',
                                                date=date.today(),
                                                receiver_id=requisition.receiver_id, requisition_id=requisition_id, status=1, type='requisition')
            db.session.add(new_notification)

            try:
                db.session.commit()
            except Exception as e:
                print(f"Ошибка при обновлении статуса заявки: {e}")
                db.session.rollback()
                return redirect('/admin/requisitions')
            finally:
                db.session.close()

            return redirect('/admin/requisitions')
        else:
            db.session.close()
            return redirect('/admin/requisitions')


admin_requisition_history = Blueprint('admin_requisition_history', __name__, template_folder='templates')


@admin_requisition_history.route('/admin/requisitions/history')
@login_required
@roles_accepted('admin')
def admin_requisition_page():
    requisitions = db.session.query(Requisition).order_by(Requisition.date.desc()).all()

    products = {}
    for requisition in requisitions:
        product = db.session.query(Product).filter_by(id=requisition.product_id).first()
        products[requisition.product_id] = product

    requisitions_list = []
    for requisition in requisitions:
        if requisition.coordination != 0:
            requisitions_list.append(requisition)

    context = {
        'products': products,
        'requisitions': requisitions_list[::-1],
        'name': current_user.name,
        'surname': current_user.surname,
        'role': current_user.roles[0].name
    }
    db.session.close()
    return render_template('requisition/admin.html', **context)