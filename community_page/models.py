from flask_pymongo import PyMongo
from geopy.distance import geodesic

mongo = PyMongo()

def init_db(app):
    mongo.init_app(app)

def get_users_by_condition_and_location(condition, user_location):
    users = list(mongo.db.users.find({'medical_condition': condition}))
    # Calculate distances
    for user in users:
        user_latlong = user.get('location')  # {'lat': ..., 'lng': ...}
        if user_latlong:
            user_coords = (user_latlong['lat'], user_latlong['lng'])
            user['distance'] = geodesic(user_coords, (user_location['lat'], user_location['lng'])).km
        else:
            user['distance'] = float('inf')  # Assign a large distance if location is missing
    # Sort users by distance
    users.sort(key=lambda x: x['distance'])
    return users
