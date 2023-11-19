from webml.extensions import db


class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    distance_from_home = db.Column(db.Float)
    distance_from_last_transaction = db.Column(db.Float)
    ratio_to_median_purchase_price = db.Column(db.Float)
    repeat_retailer = db.Column(db.Integer)
    fraud = db.Column(db.Integer)
