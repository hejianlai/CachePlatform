from flask import request, current_app, jsonify
from functools import wraps
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
from . import users


def permission_required(permissions):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            token = request.headers.get("token")
            s = Serializer(current_app.config['SECRET_KEY'])
            try:
                data = s.loads(token)
                user = users.User.query.filter_by(id=data.get("id")).first()
            except SignatureExpired:  # valid token, but expired
                return jsonify({"error": "expired token"}), 401
            except BadSignature:  # invalid token
                return jsonify({"error": "invalid token"}), 401
            if not user.has_permissions(permissions):
                return jsonify({"error": "access forbidden"}), 403
            return f(*args, **kwargs)
        return decorated_function
    return decorator
