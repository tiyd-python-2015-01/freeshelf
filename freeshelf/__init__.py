from flask import Flask

from .extensions import (
    db,
    migrate,
    debug_toolbar,
    bcrypt,
    login_manager,
    config,
)

SQLALCHEMY_DATABASE_URI = "postgres://localhost/freeshelf"
DEBUG = True
SECRET_KEY = 'development-key'
DEBUG_TB_INTERCEPT_REDIRECTS = False

app = Flask("freeshelf")
app.config.from_object(__name__)

config.init_app(app)
db.init_app(app)
debug_toolbar.init_app(app)
migrate.init_app(app, db)
bcrypt.init_app(app)
login_manager.init_app(app)
login_manager.login_view = "login"

from . import views, models