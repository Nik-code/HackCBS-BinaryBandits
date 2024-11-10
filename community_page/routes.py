from flask import Blueprint, request, jsonify, current_app
from flask_socketio import SocketIO, join_room, emit
from flask_cors import cross_origin
from models import get_users_by_condition_and_location
from app import socketio

chat_bp = Blueprint('chat', __name__)

def init_socketio(app):
    socketio.init_app(app, cors_allowed_origins="*")  # Apply CORS to socketio

# REST API Endpoint
@chat_bp.route('/connect', methods=['POST'])
@cross_origin()  # Apply CORS to this route
def connect_chat():
    try:
        data = request.get_json()
        if data is None:
            current_app.logger.error("No JSON data received")
            return jsonify({'error': 'No JSON data received'}), 400
        user_id = data.get('user_id')
        # Your existing code
    except Exception as e:
        current_app.logger.error(f"Exception occurred: {e}")
        return jsonify({'error': 'Server error'}), 500


# SocketIO Events
@socketio.on('join')
def handle_join(data):
    room = data['room']  # Room can be a unique chat ID
    join_room(room)
    current_app.logger.info(f"User joined room {room}")
    emit('status', {'msg': f'User has entered the room {room}.'}, room=room)

@socketio.on('message')
def handle_message(data):
    room = data['room']
    message = data['message']
    current_app.logger.info(f"Message in room {room}: {message}")
    emit('message', {'msg': message}, room=room)
