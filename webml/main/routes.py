from flask import render_template

from webml.main import bp
from webml.model.transaction import Transaction


@bp.route('/', methods=['GET'])
def index():
    # TODO: get and display all data points
    transactions = Transaction.query.all()
    return render_template('index.html', transactions=transactions)


@bp.route('/add', methods=['GET'])
def add_get():
    return render_template('add.html')


@bp.route('/add', methods=['POST'])
def add_post():
    # TODO: add data point
    return "Adding data point not implemented yet!"


@bp.route('/delete/<int:record_id>', methods=['POST'])
def delete_post(record_id):
    # TODO: delete data point
    return f"Deleting record {record_id} is not implemented yet!"


@bp.route('/predict', methods=['GET'])
def predict_get():
    return render_template('predict.html')


@bp.route('/predict', methods=['POST'])
def predict_post():
    # TODO: predict
    return render_template('predict_result.html')
