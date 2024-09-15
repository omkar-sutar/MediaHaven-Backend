import base64
import logging
from functools import wraps
import time


def EncodeFileToBase64(filepath : str)->str:
    with open(filepath, "rb") as file:
        file_content = file.read()
        base64_encoded = base64.b64encode(file_content)
        return base64_encoded.decode('utf-8')
    
def get_logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    return logger

def profile(f):
    wraps(f)
    def decorated(*args,**kwargs):
        start=time.time()
        ret = f(*args,**kwargs)
        end=time.time()
        name=f.__name__
        get_logger().debug(f"Method {name} took {end-start} seconds to execute.")
        return ret
    return decorated