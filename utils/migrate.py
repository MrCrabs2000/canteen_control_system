from pathlib import Path
from flask_migrate import Migrate, migrate, upgrade, init
from datebase.classes import db
from sqlalchemy import text
import shutil


def drop_alembic_version_table(app):
    with app.app_context():
        inspector = db.inspect(db.engine)
        tables = inspector.get_table_names()

        if 'alembic_version' in tables:
            db.session.execute(text('DROP TABLE alembic_version'))
            db.session.commit()
            print("Таблица alembic_version успешно удалена")
        else:
            print("Таблица alembic_version не существует")

        migrations = Path('migrations')

        if migrations.exists() and migrations.is_dir():
            shutil.rmtree(migrations)
            print("Директория migrations удалена")


def update_database(app):
    Migrate(app, db)

    with app.app_context():
        if not Path('migrations').exists():
            init()

        try:
            migrate()
            upgrade()
        except Exception as e:
            drop_alembic_version_table(app)
            print(f'У нас ошибка в функции поймана:{e}')


if __name__ == "__main__":
    from configs.app_configs import app

    update_database(app)