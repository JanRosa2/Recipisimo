from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
import os
from dotenv import load_dotenv

# We will set up a SQLAlchemy integration object
db = SQLAlchemy()
DB_NAME = "users.db"
# In secret.env are secret variables, so we will load that file
load_dotenv()
# And get the variables from
SECRET_KEY=os.getenv('SECRET_KEY')

def create_app():
    # We will create our app Flask object
    app = Flask(__name__)
    # Need this for sessions to keep them encrypted
    app.config['SECRET_KEY'] = SECRET_KEY
    # Setup what is the database type/name
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DB_NAME}"
    # This will initialize the connection between database and application (app)
    db.init_app(app)

    from .views import views
    from .auth import auth

    # url_prefix is saying us how the route will be
    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/auth/")

    from .models import User
    
    with app.app_context():
        db.create_all()

    from flask_session import Session

    # Configure session to use filesystem (instead of signed cookies)
    app.config["SESSION_PERMANENT"] = False
    app.config["SESSION_TYPE"] = "filesystem"
    Session(app)

    # Setting up LogingManager
    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

