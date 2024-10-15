from flask import Blueprint 

import logging

auth = Blueprint('auth',__name__)

logging.basicConfig(level=logging.DEBUG)


from . import views