from flask_migrate import Migrate

migrate = Migrate(render_as_batch=True)


def init_migrate(app, db):
    migrate.init_app(app, db)
