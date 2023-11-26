from typing import Dict, List
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler

from webml.extensions import db
from webml.model.transaction import Transaction


class ImportantThinkyThingy:
    scaler = StandardScaler()
    model = KNeighborsClassifier(n_neighbors=5)
    initialised = False
    ok = False


IMPORTANT_THINKY_THINGY = ImportantThinkyThingy()


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
    # Get all data from db and separate features and results
    transactions = get_all_records()
    if len(transactions) == 0:
        IMPORTANT_THINKY_THINGY.ok = False
        return
    training_data = pd.DataFrame.from_records([r.to_dict() for r in transactions])
    training_data_features = training_data.drop('id', axis=1).drop('fraud', axis=1)
    training_data_results = training_data['fraud']

    # Standardize all continuous features
    training_data_features = IMPORTANT_THINKY_THINGY.scaler.fit_transform(training_data_features)

    # Train model on standardized data
    IMPORTANT_THINKY_THINGY.model.fit(training_data_features, training_data_results)
    IMPORTANT_THINKY_THINGY.initialised = True
    IMPORTANT_THINKY_THINGY.ok = True


def get_all_records() -> List[Transaction]:
    return Transaction.query.all()


def validate_and_add_record(record_data: Dict[str, str]) -> int | None:
    # TODO: make this function better (in reality, it accepts Dict[str, Any]) and
    #  should validate and cast each value in a better way
    # Get values from all fields
    distance_from_home = str(record_data.get('distance_from_home', None))
    distance_from_last_transaction = str(record_data.get('distance_from_last_transaction', None))
    ratio_to_median_purchase_price = str(record_data.get('ratio_to_median_purchase_price', None))
    fraud = str(record_data.get('fraud', None))

    # If all fields are ok
    if validate_non_negative_float(distance_from_home) and \
            validate_non_negative_float(distance_from_last_transaction) and \
            validate_non_negative_float(ratio_to_median_purchase_price):
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
                                  fraud=fraud_constrained)
        db.session.begin()
        db.session.add(transaction)
        db.session.flush()
        db.session.commit()
        db.session.refresh(transaction)
        retrain_model()
        return transaction.id
    return None


def validate_and_delete_record(record_id: int) -> int | None:
    # Check if selected record exists
    transaction_to_delete = Transaction.query.get(record_id)
    if transaction_to_delete is None:
        return None
    Transaction.query.filter(Transaction.id == record_id).delete()
    db.session.commit()
    retrain_model()
    return record_id


def validate_and_predict_record(record_data: Dict[str, str]) -> int | None:
    if not IMPORTANT_THINKY_THINGY.initialised:
        retrain_model()
    if not IMPORTANT_THINKY_THINGY.ok:
        return None
    distance_from_home = str(record_data.get('distance_from_home', None))
    distance_from_last_transaction = str(record_data.get('distance_from_last_transaction', None))
    ratio_to_median_purchase_price = str(record_data.get('ratio_to_median_purchase_price', None))

    if validate_non_negative_float(distance_from_home) and \
            validate_non_negative_float(distance_from_last_transaction) and \
            validate_non_negative_float(ratio_to_median_purchase_price):
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
        print(transaction)
        record_to_analyze = pd.DataFrame.from_records([transaction.to_dict()])
        record_to_analyze = record_to_analyze.drop('id', axis=1).drop('fraud', axis=1)

        # Standardize all continuous features
        record_to_analyze = IMPORTANT_THINKY_THINGY.scaler.transform(record_to_analyze)
        print(record_to_analyze)
        result = IMPORTANT_THINKY_THINGY.model.predict(record_to_analyze)
        print(result)
        return result[0]
    return None
