from flask import Blueprint, render_template, send_file
from flask_security import roles_accepted
from configs.app_configs import login_required
from exel import export_products, export_dishes, export_menus


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



reports_dish = Blueprint('reports_dish', __name__, template_folder='templates')
@reports_dish.route('/admin/report/dishes', methods=['GET'])
@login_required
@roles_accepted('admin')
def reports_dish_page():
    try:
        filepath = export_dishes()

        return send_file(
            str(filepath),
            as_attachment=True,
            download_name=filepath.name
        )

    except Exception as e:
        print(f"Ошибка: {e}")
        return f"Ошибка: {e}", 500



reports_menu = Blueprint('reports_menu', __name__, template_folder='templates')
@reports_menu.route('/admin/report/menus', methods=['GET'])
@login_required
@roles_accepted('admin')
def reports_menu_page():
    try:
        filepath = export_menus()

        return send_file(
            str(filepath),
            as_attachment=True,
            download_name=filepath.name
        )

    except Exception as e:
        print(f"Ошибка: {e}")
        return f"Ошибка: {e}", 500