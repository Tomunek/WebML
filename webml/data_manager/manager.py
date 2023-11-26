from typing import Dict, List

from webml.data_manager.mlmodel import MLModel
from webml.exceptions.exceptions import *
from webml.extensions import db
from webml.model.transaction import Transaction

IMPORTANT_THINKY_THINGY = MLModel()


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


def retrain_model() -> None:
    global IMPORTANT_THINKY_THINGY
    transactions = get_all_records()
    IMPORTANT_THINKY_THINGY.train(transactions)


def get_all_records() -> List[Transaction]:
    return Transaction.query.all()


def validate_and_add_record(record_data: Dict[str, str]) -> int:
    # TODO: make this function better (in reality, it accepts Dict[str, Any]) and
    #  should validate and cast each value in a better way
    # Get values from all fields
    distance_from_home = str(record_data.get('distance_from_home', None))
    distance_from_last_transaction = str(record_data.get('distance_from_last_transaction', None))
    ratio_to_median_purchase_price = str(record_data.get('ratio_to_median_purchase_price', None))
    fraud = str(record_data.get('fraud', None))

    # If all fields are ok
    if not (validate_non_negative_float(distance_from_home) and
            validate_non_negative_float(distance_from_last_transaction) and
            validate_non_negative_float(ratio_to_median_purchase_price)):
        raise InvalidValueError()

    fraud_constrained = constrain_checkbox_value(fraud)
    distance_from_home_f = float(distance_from_home)
    distance_from_last_transaction_f = float(distance_from_last_transaction)
    ratio_to_median_purchase_price_f = float(ratio_to_median_purchase_price)

    # Add record to db
    transaction = Transaction(distance_from_home=distance_from_home_f,
                              distance_from_last_transaction=distance_from_last_transaction_f,
                              ratio_to_median_purchase_price=ratio_to_median_purchase_price_f,
                              fraud=fraud_constrained)
    db.session.begin()
    db.session.add(transaction)
    db.session.flush()
    db.session.commit()
    db.session.refresh(transaction)
    retrain_model()
    return transaction.id


def validate_and_delete_record(record_id: int) -> int:
    # Check if selected record exists
    transaction_to_delete = Transaction.query.get(record_id)
    if transaction_to_delete is None:
        raise NoRecordWithThisIDError()
    Transaction.query.filter(Transaction.id == record_id).delete()
    db.session.commit()
    retrain_model()
    return record_id


def validate_and_predict_record(record_data: Dict[str, str]) -> int:
    if not IMPORTANT_THINKY_THINGY.initialised:
        retrain_model()
    if not IMPORTANT_THINKY_THINGY.initialised:
        raise NoRecordsInDBError()

    distance_from_home = str(record_data.get('distance_from_home', None))
    distance_from_last_transaction = str(record_data.get('distance_from_last_transaction', None))
    ratio_to_median_purchase_price = str(record_data.get('ratio_to_median_purchase_price', None))

    if not (validate_non_negative_float(distance_from_home) and
            validate_non_negative_float(distance_from_last_transaction) and
            validate_non_negative_float(ratio_to_median_purchase_price)):
        raise InvalidValueError()
    distance_from_home_f = float(distance_from_home)
    distance_from_last_transaction_f = float(distance_from_last_transaction)
    ratio_to_median_purchase_price_f = float(ratio_to_median_purchase_price)
    # Transaction with unknown `fraud` value
    transaction = Transaction(id=0,
                              distance_from_home=distance_from_home_f,
                              distance_from_last_transaction=distance_from_last_transaction_f,
                              ratio_to_median_purchase_price=ratio_to_median_purchase_price_f,
                              fraud=1)
    # Here all the magic happens
    return IMPORTANT_THINKY_THINGY.classify(transaction)
