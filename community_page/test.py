from flask import Flask, jsonify, request
from flask_socketio import SocketIO, join_room, emit

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")  # Add cors_allowed_origins for testing

# Mock data
mock_users = [
    {'_id': 1, 'name': 'Alice', 'medical_condition': 'diabetes', 'location': {'lat': 40.7128, 'lng': -74.0060}},
    {'_id': 2, 'name': 'Bob', 'medical_condition': 'diabetes', 'location': {'lat': 40.730610, 'lng': -73.935242}},
    {'_id': 3, 'name': 'Charlie', 'medical_condition': 'diabetes', 'location': {'lat': 40.650002, 'lng': -73.949997}},
]

from geopy.distance import geodesic

@app.route('/chat/connect', methods=['POST'])
def connect_chat():
    data = request.get_json()
    user_id = data.get('user_id')
    condition = data.get('medical_condition')
    user_location = data.get('location')

    # Filter users with the same condition
    users = [user for user in mock_users if user['medical_condition'] == condition and user['_id'] != user_id]

    # Calculate distances
    for user in users:
        user_coords = (user['location']['lat'], user['location']['lng'])
        user['distance'] = geodesic(user_coords, (user_location['lat'], user_location['lng'])).km

    # Sort users by distance
    users.sort(key=lambda x: x['distance'])

    return jsonify({'matched_users': users}), 200

# Adding endpoints to send and receive messages via HTTP for testing
messages = []

@app.route('/chat/message', methods=['POST'])
def send_message():
    data = request.get_json()
    messages.append(data)
    app.logger.info(f"Message received: {data}")
    return jsonify({'status': 'Message sent'}), 200

@app.route('/chat/messages', methods=['GET'])
def get_messages():
    return jsonify({'messages': messages}), 200

if __name__ == '__main__':
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True)
