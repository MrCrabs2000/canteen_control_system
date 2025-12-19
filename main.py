from flask import Flask
from flask_login import LoginManager

app = Flask(__name__)
login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    return


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)