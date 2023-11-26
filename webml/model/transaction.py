from dataclasses import dataclass

from webml.extensions import db


@dataclass
class Transaction(db.Model):
    __tablename__ = 'transactions'
    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    distance_from_home: float = db.Column(db.Float, nullable=False)
    distance_from_last_transaction: float = db.Column(db.Float, nullable=False)
    ratio_to_median_purchase_price: float = db.Column(db.Float, nullable=False)
    fraud: int = db.Column(db.Integer, nullable=False)

    def __str__(self) -> str:
        return (f"Record {self.id}: {self.distance_from_home}, {self.distance_from_last_transaction}, "
                f"{self.ratio_to_median_purchase_price}, {self.fraud}")

    def to_dict(self):
        return {
            "id": self.id,
            "distance_from_home": self.distance_from_home,
            "distance_from_last_transaction": self.distance_from_last_transaction,
            "ratio_to_median_purchase_price": self.ratio_to_median_purchase_price,
            "fraud": self.fraud
        }
