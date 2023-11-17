from flask import Flask

from config import Config
from webml.extensions import db


# Flask application factory
def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize sqlite database
    db.init_app(app)

    # Register blueprint for UI
    from webml.main import bp as main_bp
    app.register_blueprint(main_bp)

    # Register blueprint for API
    from webml.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    return app
