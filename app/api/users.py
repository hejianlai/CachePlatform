from flask import jsonify, current_app, request
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
from .decorators import permission_required
from . import api, db

user_role = db.Table('sys_user_role',
                     db.Column('user_id', db.Integer, db.ForeignKey('sys_user.id')),
                     db.Column('role_id', db.Integer, db.ForeignKey('sys_role.id'))
                     )


class User(db.Model):
    __tablename__ = 'sys_user'

    id = db.Column(db.Integer, primary_key=True)
    loginName = db.Column("login_name", db.String)
    password = db.Column("password", db.String)
    name = db.Column("name", db.String)
    isDefault = db.Column("is_default", db.Integer)
    createdTime = db.Column("created_time", db.String)
    project = db.Column("project", db.String)
    roles = db.relationship('Role',
                            secondary=user_role,
                            backref=db.backref('sys_role', lazy='dynamic'),
                            lazy='dynamic')

    def to_json(self):
        roles = self.roles.all()
        role_name = ""
        if roles is not None:
            for i in range(0, len(roles)):
                if i > 0:
                    role_name += ","
                    role_name += roles[i].name
        return {
            'loginName': self.loginName,
            'name': self.name,
            'roleName': role_name,
            'is_default': self.isDefault,
            'createdTime': self.createdTime,
            'project': self.project
        }

    def has_permissions(self, permissions):
        roles = self.roles.all()
        if roles is not None:
            user_permissions = []
            for role in roles:
                for permission in role.permissions:
                    user_permissions.append(permission)
            for permission in permissions:
                if user_permissions.count(permission) < 0:
                    return False
        else:
            return False
        # return self.roles is not None and (self.roles.permissions & permissions) == permissions
        return True


@api.route("/token", methods=['POST'])
def get_auth_token():
    login_name = request.json.get('loginName')
    password = request.json.get('password')
    user = User.query.filter_by(loginName=login_name).first()
    if not user:
        return jsonify({"error": "invalid login_name"}), 401
    elif user.password == password:
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=current_app.config['EXPIRATION'])
        token = s.dumps({'id': user.id}).decode('ascii')
        return jsonify({"token": token})
    else:
        return jsonify({"error": "invalid password"}), 401


@api.route("/refresh_token")
def refresh_auth_token():
    token = request.args.get("token")
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(token)
    except SignatureExpired:  # valid token, but expired
        user = User.query.get(data['id'])
        s2 = Serializer(current_app.config['SECRET_KEY'], expires_in=current_app.config['EXPIRATION'])
        refresh_token = s2.dumps({'id': user.id})
        return jsonify({"refresh_token": refresh_token})
    except BadSignature:  # invalid token
        return jsonify({"error": "invalid token"}), 401
    return jsonify({"token": token})


@api.route("/users/select_all")
@permission_required(["SYSTEM", "ADMIN", "ROLE"])
def select_all():
    login_name = request.args.get("loginName")
    project = request.args.get("project")
    page = int(request.args.get("page"))
    size = int(request.args.get("size"))
    users = User.query
    if login_name.strip():
        users = users.filter(User.loginName.ilike("%"+login_name+"%"))
    if project.strip():
        users = users.filter_by(project=project)
    users = users.paginate(page, size)
    result = {}
    result["content"] = [user.to_json() for user in users.items]
    result["totalElements"] = users.total
    return jsonify(result)


@api.route("/hello", methods=['GET'])
def hello():
    return "hello"
