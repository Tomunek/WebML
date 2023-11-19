from webml.api import bp


@bp.route('/data', methods=['GET'])
def api_data_get():
    # TODO: get all data points
    return "TODO: return all data points"


@bp.route('/data', methods=['POST'])
def api_data_post():
    # TODO: add data point
    return "TODO: add new data point"


@bp.route('/data/<int:record_id>', methods=['DELETE'])
def api_data_delete(record_id):
    # TODO: delete data point
    return f"TODO: delete data point {record_id}"


@bp.route('/predictions', methods=['GET'])
def api_predictions_get():
    # TODO: predict
    return f"TODO: predictions"
