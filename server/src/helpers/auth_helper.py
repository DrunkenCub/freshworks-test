from flask import request, g
from flask import abort
from functools import wraps

from src.models import User

def login_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        
        if auth_header is None:
            abort(401)
        try:
            res = User.decode_auth_token(auth_header)
            user = User.query.filter_by(id=res).first()
            g.user = user
        except:
            raise
            abort(401)
        return fn(*args, **kwargs)
    return wrapper