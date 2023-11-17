from flask import Blueprint

bp = Blueprint('api', __name__)

# Do not move this import (module will not initialise correctly)
# noinspection PyPep8
from webml.api import routes
