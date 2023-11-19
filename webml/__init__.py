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
        db.session.add(Transaction(distance_from_home=57.87785658389723,
                                   distance_from_last_transaction=0.3111400080477545,
                                   ratio_to_median_purchase_price=1.9459399775518593,
                                   repeat_retailer=1.0,
                                   fraud=0.0))
        db.session.commit()

    # Register blueprint for UI
    from webml.main import bp as main_bp
    app.register_blueprint(main_bp)

    # Register blueprint for API
    from webml.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    return app
