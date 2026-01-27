from pathlib import Path
from flask_migrate import Migrate, migrate, upgrade, init
from datebase.classes import db


def update_database(app):
    Migrate(app, db)

    with app.app_context():
        if not Path('migrations').exists():
            init()

        migrate(message="Auto update")
        upgrade()


if __name__ == "__main__":
    from configs.app_configs import app

    update_database(app)