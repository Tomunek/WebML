from typing import Dict
from webml.extensions import db
from webml.model.transaction import Transaction


def is_float(string: str) -> bool:
    try:
        float(string)
        return True
    except ValueError:
        return False


def validate_non_negative_float(string: str | None) -> bool:
    if string is None:
        return False
    if len(string) == 0:
        return False
    if not is_float(string):
        return False
    if float(string) < 0:
        return False
    return True


def constrain_checkbox_value(string: str | None) -> int:
    if string is None:
        return 0
    if string == 'on':
        return 1
    return 0


def validate_and_add_record(record_data: Dict[str, str]) -> bool:
    # Get values from all fields
    distance_from_home = record_data.get('distance_from_home', None)
    distance_from_last_transaction = record_data.get('distance_from_last_transaction', None)
    ratio_to_median_purchase_price = record_data.get('ratio_to_median_purchase_price', None)
    repeat_retailer = record_data.get('repeat_retailer', None)
    fraud = record_data.get('fraud', None)

    # If all fields are ok
    if validate_non_negative_float(distance_from_home) and \
            validate_non_negative_float(distance_from_last_transaction) and \
            validate_non_negative_float(ratio_to_median_purchase_price):
        repeat_retailer_constrained = constrain_checkbox_value(repeat_retailer)
        fraud_constrained = constrain_checkbox_value(fraud)
        # Add record to db
        db.session.begin()
        db.session.add(Transaction(distance_from_home=distance_from_home,
                                   distance_from_last_transaction=distance_from_last_transaction,
                                   ratio_to_median_purchase_price=ratio_to_median_purchase_price,
                                   repeat_retailer=repeat_retailer_constrained,
                                   fraud=fraud_constrained))
        db.session.commit()
        return True
    return False
