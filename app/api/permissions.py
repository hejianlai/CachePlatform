from ..api import db


class Permission(db.Model):
    __tablename__ = "sys_permission"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    code = db.Column(db.String)
    description = db.Column(db.String)
    pid = db.Column(db.Integer)
    created_time = db.Column(db.String)
