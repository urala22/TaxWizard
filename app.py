import os
import logging
from datetime import datetime

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix
from flask_login import LoginManager


# Set up logging
logging.basicConfig(level=logging.DEBUG)

class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)
# create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)  # needed for url_for to generate with https

# Configure the database
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///tax_assistant.db")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize the app with the extension
db.init_app(app)

# Initialize flask-login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    from models import User
    return User.query.get(int(user_id))

@app.context_processor
def inject_now():
    return {'now': datetime.now()}

with app.app_context():
    # Make sure to import the models here or their tables won't be created
    import models  # noqa: F401

    db.create_all()
    
    # Run migrations to add any missing columns
    from migrations import run_migrations
    run_migrations()
