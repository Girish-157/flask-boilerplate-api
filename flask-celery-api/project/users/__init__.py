from flask import Blueprint

users_blueprint = Blueprint("users", __name__, url_prefix="/users")

from . import events, models, routes, tasks  # noqa