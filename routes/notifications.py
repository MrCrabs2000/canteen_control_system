from flask import Blueprint, render_template, redirect, request
from flask_security import current_user, roles_accepted
from datebase.classes import db, Notification
from configs.app_configs import login_required

notifications = Blueprint('notifications_admin', __name__, template_folder='templates')


@notifications.route('/notifications', methods=["GET", "POST"])
@login_required
@roles_accepted('admin', 'cook', 'user')
def notifications_page():
    try:
        notifications_not_checked = db.session.query(Notification).filter_by(
            receiver_id=current_user.id
        ).order_by(
            Notification.status == 1,
            Notification.date.desc()
        ).all()
        notifications = []
        cnt = 0

        for notification in notifications_not_checked:
            if notification.status == 1:
                notifications.append(notification)
            elif cnt < 10:
                cnt += 1
                notifications.append(notification)

        db.session.commit()
        if request.method == 'POST':
            notification_id = request.form.get('notification_id')
            notification_viewed = db.session.query(Notification).filter_by(id=notification_id).first()
            try:
                notification_viewed.status = 2
                db.session.commit()
            except Exception as e:
                print(f'У нас ошибка в изменении статуса уведома: {e}')
            finally:
                if current_user.roles[0].name == 'admin' and notification_viewed.type == 'requisition':
                    db.session.close()
                    return redirect('/admin/requisitions')
                elif current_user.roles[0].name == 'cook' and notification_viewed.type == 'requisition':
                    db.session.close()
                    return redirect('/cook/requisitions')
                elif current_user.roles[0].name == 'cook' and notification_viewed.type == 'add_menu':
                    db.session.close()
                    return redirect('/cook/menus')
                elif current_user.roles[0].name == 'cook' and notification_viewed.type == 'add_dish':
                    db.session.close()
                    return redirect('/cook/dishes')
                elif current_user.roles[0].name == 'cook' and notification_viewed.type == 'add_product':
                    db.session.close()
                    return redirect('/cook/products')
                elif current_user.roles[0].name in ['cook', 'admin', 'user'] and notification_viewed.type == 'profile':
                    db.session.close()
                    return redirect('/profile')
        context = {
            'notifications': notifications[::-1],
            'name': current_user.name,
            'surname': current_user.surname,
            'role': current_user.roles[0].name
        }

        return render_template('notifications/notifications.html', **context)

    except Exception as e:
        db.session.rollback()
        print(f"Ошибка в обновлении статуса уведома: {e}")
        return redirect('/')

    finally:
        db.session.close()