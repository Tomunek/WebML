from dataclasses import dataclass

from sqlalchemy.orm import Mapped

from webml.extensions import db


@dataclass
class Transaction(db.Model):
    __tablename__ = 'transactions'
    id: Mapped[int] = db.mapped_column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    distance_from_home: Mapped[float] = db.mapped_column(db.Float, nullable=False)
    distance_from_last_transaction: Mapped[float] = db.mapped_column(db.Float, nullable=False)
    ratio_to_median_purchase_price: Mapped[float] = db.mapped_column(db.Float, nullable=False)
    fraud: Mapped[int] = db.mapped_column(db.Integer, nullable=False)

    def __str__(self) -> str:
        return (f"Record {self.id}: {self.distance_from_home}, {self.distance_from_last_transaction}, "
                f"{self.ratio_to_median_purchase_price}, {self.fraud}")
