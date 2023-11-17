from flask import render_template

from webml.main import bp


@bp.route('/')
def index():
    # TODO: get and display all data points
    return render_template('index.html')


@bp.get('/add')
def add_get():
    return render_template('add.html')


@bp.post('/add')
def add_post():
    # TODO: add data point
    return "Adding data point not implemented yet!"


@bp.post('/delete/<int:record_id>')
def delete_post(record_id):
    # TODO: delete data point
    return f"Deleting record {record_id} is not implemented yet!"


@bp.get('/predict')
def predict_get():
    return render_template('predict.html')


@bp.post('/predict')
def predict_post():
    # TODO: predict
    return render_template('predict_result.html')
