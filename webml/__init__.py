from flask import Flask

from config import Config
from webml.model.transaction import Transaction
from webml.extensions import db


# Flask application factory
def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize sqlite database
    with app.app_context():
        db.init_app(app)
        db.create_all()

    # Register blueprint for UI
    from webml.main import bp as main_bp
    app.register_blueprint(main_bp)

    # Register blueprint for API
    from webml.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    return app
