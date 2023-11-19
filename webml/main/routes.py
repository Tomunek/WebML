from flask import render_template, redirect, url_for

from webml.extensions import db
from webml.main import bp
from webml.model.transaction import Transaction


@bp.route('/', methods=['GET'])
def index():
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
    transaction_to_delete = Transaction.query.get(record_id)
    if transaction_to_delete is None:
        return f"Transaction with id {record_id} does not exist, so it can not be deleted!", 404
    else:
        Transaction.query.filter(Transaction.id == record_id).delete()
        db.session.commit()
        return redirect(url_for('main.index'), code=302)


@bp.route('/predict', methods=['GET'])
def predict_get():
    return render_template('predict.html')


@bp.route('/predict', methods=['POST'])
def predict_post():
    # TODO: predict
    return render_template('predict_result.html')
