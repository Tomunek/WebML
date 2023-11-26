class WebMLError(Exception):
    pass


class InvalidValueError(WebMLError):
    pass


class NoRecordsInDBError(WebMLError):
    pass


class NoRecordWithThisIDError(WebMLError):
    pass
