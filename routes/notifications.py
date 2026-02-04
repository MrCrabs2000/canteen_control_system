from flask import Blueprint, render_template, redirect
from flask_security import current_user, roles_accepted
from datebase.classes import db, Notification
from configs.app_configs import login_required

notifications_admin = Blueprint('notifications_admin', __name__, template_folder='templates')


@notifications_admin.route('/notifications')
@login_required
@roles_accepted('admin', 'cook')
def admin_notifications_page():
    try:
        notifications = db.session.query(Notification).filter_by(recevier_id=current_user.id).order_by(
            Notification.date.desc()).all()

        for notification in notifications:
            if notification.status == False:
                notification.status = True

        db.session.commit()

        context = {
            'notifications': notifications,
            'name': current_user.name,
            'surname': current_user.surname,
            'role': current_user.roles[0].name
        }

        return render_template('notifications/notifications.html', **context)

    except Exception as e:
        db.session.rollback()
        print(f"Error updating notifications: {e}")
        return redirect('/')

    finally:
        db.session.close()