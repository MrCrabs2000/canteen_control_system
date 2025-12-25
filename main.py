from flask import Flask, render_template
from routes.main_page import main_page, mainpage
from routes.register import register_page
from routes.exit import exit_page
from routes.login import login_page
from datebase.db_session import init_database, create_session
from flask_login import LoginManager, current_user
from datebase.classes import User
from os import makedirs


makedirs('db', exist_ok=True)
app = Flask(__name__)
app.secret_key = '25112008'
login_manager = LoginManager()
login_manager.init_app(app)

init_database()


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



@app.route('/', methods=['GET', 'POST'])
def inition():
    if current_user.is_authenticated:
        return mainpage()
    return render_template('start.html')


if "__main__" == __name__:
    app.run(debug=True)