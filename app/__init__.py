from flask import Flask
from . import routes
from .create_db import db, User, bcrypt


def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    # Import and register blueprints (if needed)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
    db.init_app(app)
    bcrypt.init_app(app)

  # Redirect to login page if not logged in


    from . import routes
    app.register_blueprint(routes.bp)

    


 
    return app