from ..api import db

role_permission = db.Table('sys_role_permission',
                           db.Column('role_id', db.Integer, db.ForeignKey('sys_role.id')),
                           db.Column('permission_id', db.Integer, db.ForeignKey('sys_permission.id'))
                           )


class Role(db.Model):
    __tablename__ = "sys_role"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    is_default = db.Column(db.Integer)
    created_time = db.Column(db.String)
    permissions = db.relationship('Permission',
                                  secondary=role_permission,
                                  backref=db.backref('sys_permission', lazy='dynamic'),
                                  lazy='dynamic')
