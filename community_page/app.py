from flask import Flask
from flask_cors import CORS
from config import Config
from models import init_db
from routes import chat_bp, init_socketio, socketio
from flask_socketio import SocketIO
from flask_cors import CORS

socketio = SocketIO(cors_allowed_origins="*")

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize CORS for the entire app
    CORS(app, resources={r"/chat/*": {"origins": "*"}})

    init_db(app)
    init_socketio(app)

    # Register the blueprint with CORS applied
    app.register_blueprint(chat_bp, url_prefix='/chat')

    return app


if __name__ == '__main__':
    app = create_app()
    CORS(app)
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True, cors_allowed_origins="*")
