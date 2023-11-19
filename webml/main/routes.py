from flask import render_template, redirect, url_for, request

from webml.main import bp
from webml.model.transaction import Transaction
from webml.util.utils import validate_and_add_record, validate_and_delete_record


@bp.route('/', methods=['GET'])
def index():
    transactions = Transaction.query.all()
    return render_template('index.html', transactions=transactions)


@bp.route('/add', methods=['GET'])
def add_get():
    return render_template('add.html')


@bp.route('/add', methods=['POST'])
def add_post():
    # Try to add record to db
    if validate_and_add_record(request.form) is not None:
        # If ok, redirect to index
        return redirect(url_for('main.index'), code=302)
    else:
        # else, return error
        return "Invalid data!", 400


@bp.route('/delete/<int:record_id>', methods=['POST'])
def delete_post(record_id):
    if validate_and_delete_record(record_id) is None:
        return f"Transaction with id {record_id} does not exist, so it can not be deleted!", 404
    else:
        return redirect(url_for('main.index'), code=302)


@bp.route('/predict', methods=['GET'])
def predict_get():
    return render_template('predict.html')


@bp.route('/predict', methods=['POST'])
def predict_post():
    # TODO: predict
    return render_template('predict_result.html')
