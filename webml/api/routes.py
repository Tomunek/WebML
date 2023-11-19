import dataclasses
import json

from flask import request

from webml import Transaction
from webml.api import bp
from webml.util.utils import validate_and_add_record, validate_and_delete_record


@bp.route('/data', methods=['GET'])
def api_data_get():
    transactions = Transaction.query.all()
    return f"{json.dumps([dataclasses.asdict(transaction) for transaction in transactions])}"


@bp.route('/data', methods=['POST'])
def api_data_post():
    json_object = request.json
    if json_object is None:
        return json.dumps(["Invalid data"]), 400
    inserted_id = validate_and_add_record(json_object)
    if inserted_id is not None:
        return json.dumps({'id': inserted_id}), 200
    else:
        return json.dumps({'error': 'Invalid data'}), 400


@bp.route('/data/<int:record_id>', methods=['DELETE'])
def api_data_delete(record_id):
    if validate_and_delete_record(record_id) is None:
        return json.dumps({'error': 'Record not found'}), 404
    else:
        return json.dumps({'id': record_id}), 200


@bp.route('/predictions', methods=['GET'])
def api_predictions_get():
    # TODO: predict
    return f"TODO: predictions"
