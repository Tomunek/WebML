from flask import render_template, redirect, url_for, request

from webml.main import bp
from webml.data_manager.manager import get_all_records, validate_and_add_record, validate_and_delete_record, \
    validate_and_predict_record
from webml.exceptions.exceptions import *


@bp.route('/', methods=['GET'])
def index():
    transactions = get_all_records()
    return render_template('index.html', transactions=transactions)


@bp.route('/add', methods=['GET'])
def add_get():
    return render_template('add.html')


@bp.route('/add', methods=['POST'])
def add_post():
    # Try to add record to db
    try:
        validate_and_add_record(request.form)
    except InvalidValueError:
        return render_template('error.html', code=400,
                               text="Invalid data!"), 400
    return redirect(url_for('main.index'), code=302)


@bp.route('/delete/<int:record_id>', methods=['POST'])
def delete_post(record_id):
    try:
        validate_and_delete_record(record_id)
    except NoRecordWithThisIDError:
        return render_template('error.html', code=404,
                               text=f"Transaction with id {record_id} does not exist, so it can not be deleted!"), 404
    return redirect(url_for('main.index'), code=302)


@bp.route('/predict', methods=['GET'])
def predict_get():
    return render_template('predict.html')


@bp.route('/predict', methods=['POST'])
def predict_post():
    try:
        result = validate_and_predict_record(request.form)
        return render_template('predict_result.html', result=result)
    except InvalidValueError:
        return render_template('error.html', code=400,
                               text="Invalid data!"), 400
    except NoRecordsInDBError:
        return render_template('error.html', code=400,
                               text="Not enough points in database to predict a result!"), 400
