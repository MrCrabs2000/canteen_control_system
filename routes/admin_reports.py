from flask import Blueprint, render_template, request, redirect, send_file
from flask_security import roles_accepted
from datebase.classes import Product, db
from configs.app_configs import login_required
import os
from exel import export_products


reports = Blueprint('reports', __name__, template_folder='templates')
@reports.route('/admin/reports', methods=['GET'])
@login_required
@roles_accepted('admin')
def reports_list():
    return render_template('reports.html')



reports_product = Blueprint('reports_product', __name__, template_folder='templates')
@reports_product.route('/admin/report/products', methods=['GET'])
@login_required
@roles_accepted('admin')
def reports_product_page():
    try:
        filepath = export_products()

        return send_file(
            str(filepath),
            as_attachment=True,
            download_name=filepath.name
        )

    except Exception as e:
        print(f"Ошибка: {e}")
        return f"Ошибка: {e}", 500