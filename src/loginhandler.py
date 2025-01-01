from flask import request,jsonify
import os
from src.auth import *
from src.utils import get_logger
import threading
from src.thumbnails.tasks import generate_thumbnails_bulk

logger = get_logger()

def LoginHandler():
    data = request.get_json()
    logger.debug(data)
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return ResponseInvalidArguments("username/password not found")
    users=env.getAllUsers()
    if users.get(username,None) == password:
        token = generate_token(username)

        # Generate thumbnails
        dirname=username
        dirpath=os.path.join(os.getenv(env.DATA_DIR),dirname)
        threading.Thread(target=generate_thumbnails_bulk,daemon=True,args=(dirpath,)).start()
        return jsonify({'token': token})
    
    return jsonify({'message': 'Invalid credentials'}), 401
    


@authorize
def PingHandler(user):
    return {"message":f"Hello user {user['username']}"},200