import os

DATA_DIR="DATA_DIR"
THUMBNAIL_DIR="THUMBNAIL_DIR"
USER_PREFIX="USER_"
SECRET_KEY="SECRET_KEY"  
LOG_FILE="LOG_FILE"    
LOG_LEVEL="LOG_LEVEL"
SELF_PORT="SELF_PORT"

def getAllUsers():
    users={}
    for key,val in os.environ.items():
        if key.startswith(USER_PREFIX):
            username=key.removeprefix(USER_PREFIX).lower()
            password=val
            users[username]=password
    return users

def getSecretKey():
    return os.getenv(SECRET_KEY,"k6nn@p12=76ry(*w0lundi9juf^7f8r*5xf)sbe*p5qbnz1&0i")