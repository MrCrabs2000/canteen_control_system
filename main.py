from flask import Flask, render_template
from routes.main_page import main_page, mainpage
from routes.register import register_page
from routes.exit import exit_page
from routes.login import login_page
from routes.profile import profile_page
from routes.profile_edit import profile_edit_page
from routes.menu import menu_page
from routes.admin_menu import admin_menu, admin_menu_page
from routes.add_menu import add_menu
from routes.add_dish import add_dish
from routes.add_user import add_user
from routes.cook_menu import cook_menu, cook_menu_page
from datebase.db_session import init_database, create_session
from werkzeug.security import generate_password_hash
from flask_login import LoginManager, current_user
from datebase.classes import User
from random import shuffle, choice
from os import makedirs


makedirs('db', exist_ok=True)
app = Flask(__name__)
app.secret_key = '25112008'
login_manager = LoginManager()
login_manager.init_app(app)

init_database()

symbols = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
          'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'P', 'Q', 'R',
          'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']

def generate_password_for_user():
    shuffle(symbols)
    password = ''.join((choice(symbols)) for _ in range(8))
    return password


session_db = create_session()
admin = session_db.query(User).filter_by(login='Admin').first()
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
            role='admin',
        )

        session_db.add(main_admin)
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


app.register_blueprint(main_page)
app.register_blueprint(register_page)
app.register_blueprint(exit_page)
app.register_blueprint(login_page)
app.register_blueprint(profile_page)
app.register_blueprint(profile_edit_page)
app.register_blueprint(menu_page)
app.register_blueprint(admin_menu)
app.register_blueprint(add_menu)
app.register_blueprint(add_dish)
app.register_blueprint(add_user)
app.register_blueprint(cook_menu)



@app.route('/', methods=['GET', 'POST'])
def inition():
    if current_user.is_authenticated:
        if current_user.role == 'student':
            return mainpage()
        elif current_user.role == 'cook':
            return cook_menu_page()
        elif current_user.role == 'admin':
            return admin_menu_page()
    return render_template('start.html')


if "__main__" == __name__:
    app.run(debug=True)