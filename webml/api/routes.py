from webml.api import bp


@bp.get('/data')
def api_data_get():
    # TODO: get all data points
    return "TODO: return all data points"


@bp.post('/data')
def api_data_post():
    # TODO: add data point
    return "TODO: add new data point"


@bp.delete('/data/<int:record_id>')
def api_data_delete(record_id):
    # TODO: delete data point
    return f"TODO: delete data point {record_id}"


@bp.get('/predictions')
def api_predictions_get():
    # TODO: predict
    return f"TODO: predictions"
