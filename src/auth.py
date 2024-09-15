import datetime,jwt,logging,env
from flask import request
from req_resp import *
from functools import wraps
from utils import get_logger

logger = get_logger()

def ValidateJWT(token:str):  
    if not token:
        return ResponseInvalidArguments('access-token missing')
    try:
        data = jwt.decode(token, env.getSecretKey(), algorithms=['HS256'])
        current_user = {'username':data["username"]}
        logger.debug(f"JWT validation for user {current_user} successfull.")
        return current_user
    except Exception as e:
        logger.error(e)
        return None

def generate_token(username):
    payload = {
        'username': username,
        'exp': datetime.datetime.now() + datetime.timedelta(days=14)
    }
    return jwt.encode(payload, env.getSecretKey(), algorithm='HS256')

def authorize(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('x-access-token',None)
        token = token or request.args.get('token',None)
        if not token:
            return ResponseInvalidArguments('access-token missing')
              
        user=ValidateJWT(token)
        if not user:
            return ResponseUnauthorized
        return f(user, *args, **kwargs)
    
    return decorated
