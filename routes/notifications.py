from flask import Blueprint, render_template
from flask_security import current_user, roles_accepted
from datebase.classes import db, Notification
from configs.app_configs import login_required


notifications_admin = Blueprint('notifications_admin', __name__, template_folder='templates')
@notifications_admin.route('/admin/notifications')
@login_required
@roles_accepted('admin')
def admin_notifications_page():
    try:
        notifications = db.session.query(Notification).filter_by(receiver_id=current_user.id)
        context = {
            'menus': menu,
            'name': current_user.name,
            'surname': current_user.surname
        }
        return render_template('menus/list.html', **context)

    finally:
        db.session.close()