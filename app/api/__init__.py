from flask import Blueprint
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
api = Blueprint('api', __name__)

from . import users, roles, permissions
