from flask import Flask
from flask_security import Security, SQLAlchemyUserDatastore
from datebase.classes import db, User, Role
import uuid
import os
from werkzeug.security import generate_password_hash
from utils.generation_password import generate_password_for_user


app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, '..', 'templates')
app.template_folder = TEMPLATE_DIR

app.static_folder = os.path.join(BASE_DIR, '..', 'static')

DB_DIR = os.path.join(BASE_DIR, '..', 'db')
DB_PATH = os.path.join(DB_DIR, 'canteen_control_system.db')

if not os.path.exists(DB_DIR):
    os.makedirs(DB_DIR, exist_ok=True)


app.config['SECRET_KEY'] = '25112008'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_PATH}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SECURITY_PASSWORD_SALT'] = 'wasd'
app.config['SECURITY_TRACKABLE'] = True
app.config['SECURITY_USERNAME_REQUIRED'] = True
app.config['SECURITY_LOGIN_URL'] = '/logining'
app.config['SECURITY_REGISTER_URL'] = '/registration'
app.config['SECURITY_REGISTERABLE'] = True
app.config['SECURITY_SEND_REGISTER_EMAIL'] = False
app.config['SECURITY_FLASH_MESSAGES'] = False
app.config['SECURITY_UNAUTHORIZED_VIEW'] = None
app.config['SECURITY_LOGIN_USER_TEMPLATE'] = 'auth/login.html'
app.config['SECURITY_PROFILE_URL'] = '/user_profile'

db.init_app(app)



@app.before_request
def start_db():
    with app.app_context():
        db.create_all()
        if not Role.query.first():
            admin_role = Role(name='admin')
            user_role = Role(name='user')
            cook_role = Role(name='cook')
            db.session.add(admin_role)
            db.session.add(user_role)
            db.session.add(cook_role)
            db.session.commit()
        
    admin_role = Role.query.filter_by(name='admin').first()

    try:
        admin = User.query.filter_by(login='Admin').first()

        if not admin:
            password = generate_password_for_user()
            print(f"Admin password: {password}")

            passwordHash = generate_password_hash(password)

            main_admin = User(
                name='Admin',
                surname='Admin',
                patronymic='Admin',
                login='Admin',
                password=passwordHash,
                active=True,
                fs_uniquifier=str(uuid.uuid4()),
                login_count=0
            )

            db.session.add(main_admin)

            if admin_role:
                main_admin.roles.append(admin_role)
            else:
                admin_role = Role(name='admin')
                db.session.add(admin_role)
                main_admin.roles.append(admin_role)
                
        elif admin_role and admin_role not in admin.roles:
            main_admin.roles.append(admin_role)

        db.session.commit()
    except Exception:
        db.session.rollback()
    db.session.close()

    app.before_first_request = True





user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)