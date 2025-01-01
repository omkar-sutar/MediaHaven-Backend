import os
from dotenv import load_dotenv
load_dotenv()
from flask import Flask
from src import env
import logging
from src.loginhandler import LoginHandler, PingHandler
from src.filehandler import MediaHandler
from src.thumbnails.tasks import generate_thumbnails_bulk, TMP_DIR
from src.scheduler import register_task
from flask_cors import CORS


def create_app():
    app = Flask(__name__)
    CORS(app,origins="*")
    app.config[env.SECRET_KEY] = env.getSecretKey()
    
    configure_app()
    register_routes(app)
    register_background_tasks()

    return app

def configure_app():
    init_logging()
    create_user_directories()

def create_user_directories():
    DATA_DIR = os.getenv(env.DATA_DIR)
    for username in env.getAllUsers():
        logging.debug(f"Registered user: {username}")
        user_dir = os.path.join(DATA_DIR, username)
        if not os.path.exists(user_dir):
            os.makedirs(user_dir)
        thumbnails_dir = os.path.join(user_dir, os.getenv(env.THUMBNAIL_DIR))
        if not os.path.exists(thumbnails_dir):
            os.makedirs(thumbnails_dir)
        tmp_dir=os.path.join(user_dir, TMP_DIR)
        if not os.path.exists(tmp_dir):
            os.makedirs(tmp_dir)

def register_background_tasks():
    # register_task(generate_thumbnails_bulk,"generate_thumbnails_bulk",30, "E:\\PY\\PY\\mediahavenbd\\data\\omkar")
    return

def register_routes(app):
    app.add_url_rule("/login", "login", LoginHandler, methods=["POST"])
    app.add_url_rule("/ping", "ping", PingHandler, methods=["GET"])
    app.add_url_rule("/api/media", "ListMedia", MediaHandler.List, methods=["GET"])
    app.add_url_rule("/api/media/thumbnails", "GetMediaThumbnails", MediaHandler.GetThumbnails, methods=["POST"])
    app.add_url_rule("/api/media/<filename>", "GetMedia", MediaHandler.Get, methods=["GET"])
    app.add_url_rule("/api/media/upload", "Upload", MediaHandler.Upload, methods=["POST"])

def init_logging():
    logfile = os.getenv(env.LOG_FILE, None)
    print(f"Redirecting logs to {logfile if logfile else 'stdout'}")
    logging.basicConfig(filename=logfile, format="%(asctime)s {%(filename)s:%(lineno)d} [%(levelname)s] %(message)s",level=logging.DEBUG)

app = create_app()
if __name__ == "__main__":
    # This creates the application object
    app.run(debug=False, host="0.0.0.0", port=int(os.getenv(env.SELF_PORT, 5001)), threaded=True)