from flask import redirect
from pathlib import Path
from configs.app_configs import app
from routes.routes import register_all_blueprints
from flask_security import current_user
from utils.migrate import update_database, drop_alembic_version_table


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
        if current_user.roles[0].name != 'admin':
            return redirect('/menu')
        elif current_user.roles[0].name == 'admin':
            return redirect('/admin/menu')

    return redirect('/login')


if "__main__" == __name__:
    app.run(host='0.0.0.0', port=5000, debug=True)