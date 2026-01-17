from flask import Flask, render_template
from routes.main_pages import mainpage
from routes.routes import register_all_blueprints
from routes.admin_menu import admin_menu_page
from routes.cook_menu import cook_menu_page
from utils.generation_password import generate_password_for_user
from datebase.db_session import init_database, create_session
from werkzeug.security import generate_password_hash
from flask_login import LoginManager, current_user
from datebase.classes import User, Role
from os import makedirs


makedirs('db', exist_ok=True)
app = Flask(__name__)
app.secret_key = '25112008'
login_manager = LoginManager()
login_manager.init_app(app)

init_database()

session_db = create_session()
admin = session_db.query(User).filter_by(login='Admin').first()
admin_role = session_db.query(Role).filter_by(name='admin').first()
try:
    if not admin:
        password = generate_password_for_user()
        print(password)

        passwordHash = generate_password_hash(password)

        main_admin = User(
            name='Admin',
            surname='Admin',
            patronymic='Admin',
            login='Admin',
            password=passwordHash,
            role=1
        )

        session_db.add(main_admin)

    if  not admin_role:
        admin_role = Role(
            name='admin'
        )
        session_db.add(admin_role)

    session_db.commit()
except Exception:
    session_db.rollback()
session_db.close()


@login_manager.user_loader
def load_user(id):
    db_session = create_session()
    user = db_session.get(User, id)
    db_session.close()
    return user


register_all_blueprints(app)


@app.route('/', methods=['GET', 'POST'])
def inition():
    if current_user.is_authenticated:
        if current_user.role == 3:
            return mainpage()
        elif current_user.role == 2:
            return cook_menu_page()
        elif current_user.role == 1:
            return admin_menu_page()
    return render_template('start.html')


if "__main__" == __name__:
    app.run(debug=True)