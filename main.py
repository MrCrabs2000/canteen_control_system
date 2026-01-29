from configs.app_configs import app
from flask import render_template
from routes.main_pages import mainpage
from routes.routes import register_all_blueprints
from routes.admin_menu import admin_menu_page
from routes.cook_menu import cook_menu_page
from flask_security import current_user
from utils.migrate import update_database, drop_alembic_version_table
from pathlib import Path


register_all_blueprints(app)
try:
    db_path = Path(__file__).parent / 'db' / 'canteen_control_system.db'
    if not db_path.exists():
        drop_alembic_version_table(app)

    update_database(app)

except Exception as e:
    print(f'У нас ошибка в функции поймана:{e}')



@app.route('/', methods=['GET', 'POST'])
def inition():
    if current_user.is_authenticated:
        if current_user.roles[0].name == 'user':
            return mainpage()
        elif current_user.roles[0].name == 'cook':
            return cook_menu_page()
        elif current_user.roles[0].name == 'admin':
            return admin_menu_page()
    return render_template('start.html')


if "__main__" == __name__:
    app.run(debug=True)