from typing import Dict, List
from webml.extensions import db
from webml.model.transaction import Transaction


def is_float(string: str) -> bool:
    try:
        float(string)
        return True
    except ValueError:
        return False


def validate_non_negative_float(string: str) -> bool:
    if len(string) == 0:
        return False
    if not is_float(string):
        return False
    if float(string) < 0:
        return False
    return True


def constrain_checkbox_value(string: str) -> int:
    if string == 'on':
        return 1
    return 0


def get_all_records() -> List[Transaction]:
    return Transaction.query.all()


def validate_and_add_record(record_data: Dict[str, str]) -> int | None:
    # TODO: make this function better (in reality, it accepts Dict[str, Any]) and
    #  should validate and cast each value in a better way
    # Get values from all fields
    distance_from_home = str(record_data.get('distance_from_home', None))
    distance_from_last_transaction = str(record_data.get('distance_from_last_transaction', None))
    ratio_to_median_purchase_price = str(record_data.get('ratio_to_median_purchase_price', None))
    repeat_retailer = str(record_data.get('repeat_retailer', None))
    fraud = str(record_data.get('fraud', None))

    # If all fields are ok
    if validate_non_negative_float(distance_from_home) and \
            validate_non_negative_float(distance_from_last_transaction) and \
            validate_non_negative_float(ratio_to_median_purchase_price):
        repeat_retailer_constrained = constrain_checkbox_value(repeat_retailer)
        fraud_constrained = constrain_checkbox_value(fraud)
        distance_from_home_f = float(distance_from_home)
        distance_from_last_transaction_f = float(distance_from_last_transaction)
        ratio_to_median_purchase_price_f = float(ratio_to_median_purchase_price)

        assert isinstance(distance_from_home_f, float)
        assert isinstance(distance_from_last_transaction_f, float)
        assert isinstance(ratio_to_median_purchase_price_f, float)
        # Add record to db
        transaction = Transaction(distance_from_home=distance_from_home_f,
                                  distance_from_last_transaction=distance_from_last_transaction_f,
                                  ratio_to_median_purchase_price=ratio_to_median_purchase_price_f,
                                  repeat_retailer=repeat_retailer_constrained,
                                  fraud=fraud_constrained)
        db.session.begin()
        db.session.add(transaction)
        db.session.flush()
        db.session.commit()
        db.session.refresh(transaction)
        return transaction.id
    return None


def validate_and_delete_record(record_id: int) -> int | None:
    # Check if selected record exists
    transaction_to_delete = Transaction.query.get(record_id)
    if transaction_to_delete is None:
        return None
    Transaction.query.filter(Transaction.id == record_id).delete()
    db.session.commit()
    return record_id


def validate_and_predict_record(record_data: Dict[str, str]) -> int | None:
    distance_from_home = str(record_data.get('distance_from_home', None))
    distance_from_last_transaction = str(record_data.get('distance_from_last_transaction', None))
    ratio_to_median_purchase_price = str(record_data.get('ratio_to_median_purchase_price', None))
    repeat_retailer = str(record_data.get('repeat_retailer', None))

    if validate_non_negative_float(distance_from_home) and \
            validate_non_negative_float(distance_from_last_transaction) and \
            validate_non_negative_float(ratio_to_median_purchase_price):
        repeat_retailer_constrained = constrain_checkbox_value(repeat_retailer)
        distance_from_home_f = float(distance_from_home)
        distance_from_last_transaction_f = float(distance_from_last_transaction)
        ratio_to_median_purchase_price_f = float(ratio_to_median_purchase_price)
        repeat_retailer_constrained = constrain_checkbox_value(repeat_retailer)

    return None
