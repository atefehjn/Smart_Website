from flask import Flask
from . import routes

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    # Import and register blueprints (if needed)
    from . import routes
    app.register_blueprint(routes.bp)

    return app