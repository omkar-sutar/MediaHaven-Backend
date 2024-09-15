import threading
import time
import logging
import uuid
from functools import wraps
from utils import get_logger

logger = get_logger()

task_ids = []
lock = threading.Lock()

def with_lock(f):
    @wraps(f)
    def decorated(*args,**kwargs):
        with lock:
            f(*args,**kwargs)
    return decorated

@with_lock
def register_task(func: callable,task_id:str, delta: float, *args, **kwargs):
    """
    Executes 'func' every 'delta' seconds
    """
    if task_id in task_ids:
        logger.error("Duplicate task registration detected")
        return
    task_ids.append(task_id)
    logger.info(f"Registering task {func.__name__} (ID: {task_id}) with delta {delta} seconds")
    
    def run():
        while True:
            start_time = time.time()
            try:
                logger.debug(f"Executing task {func.__name__} (ID: {task_id})")
                func(*args, **kwargs)
                logger.debug(f"Done executing task {func.__name__} (ID: {task_id})")
            except Exception as e:
                logger.error(f"Error executing task {func.__name__} (ID: {task_id}): {e}")
            finally:
                execution_time = time.time() - start_time
                sleep_time = max(0, delta - execution_time)
                logger.debug(f"Task {func.__name__} (ID: {task_id}) took {execution_time:.2f}s to execute. Sleeping for {sleep_time:.2f}s")
                time.sleep(sleep_time)
    
    thread = threading.Thread(target=run, daemon=True)
    thread.start()
    logger.info(f"Started thread for task {func.__name__} (ID: {task_id})")