import dataclasses
import json

from flask import request

from webml.api import bp
from webml.data_manager.manager import get_all_records, validate_and_add_record, validate_and_delete_record, \
    validate_and_predict_record
from webml.exceptions.exceptions import *


@bp.route('/data', methods=['GET'])
def api_data_get():
    transactions = get_all_records()
    return f"{json.dumps([dataclasses.asdict(transaction) for transaction in transactions])}"


@bp.route('/data', methods=['POST'])
def api_data_post():
    json_object = request.json
    if json_object is None:
        return json.dumps(["Invalid data"]), 400
    try:
        inserted_id = validate_and_add_record(json_object)
        return json.dumps({'id': inserted_id}), 200
    except InvalidValueError:
        return json.dumps({'error': 'Invalid data'}), 400


@bp.route('/data/<int:record_id>', methods=['DELETE'])
def api_data_delete(record_id):
    try:
        validate_and_delete_record(record_id)
        return json.dumps({'id': record_id}), 200
    except NoRecordWithThisIDError:
        return json.dumps({'error': f'Record with id {record_id} not found'}), 404


@bp.route('/predictions', methods=['GET'])
def api_predictions_get():
    try:
        result = validate_and_predict_record(request.args.to_dict())
        return json.dumps({'fraud': result}), 200
    except InvalidValueError:
        return json.dumps({'error': 'Invalid data'}), 400
    except NoRecordsInDBError:
        return json.dumps({'error': 'Empty database'}), 400
