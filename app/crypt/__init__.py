from flask import Blueprint

crypt = Blueprint('crypt', __name__)

from . import crypt_routes