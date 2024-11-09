import requests
from geopy.distance import geodesic

# Expanded location coordinates for various regions in India
region_coordinates = {
    'Delhi': (28.6139, 77.2090),
    'Mumbai': (19.0760, 72.8777),
    'Bengaluru': (12.9716, 77.5946),
    'Kolkata': (22.5726, 88.3639),
    'Chennai': (13.0827, 80.2707),
    'Hyderabad': (17.3850, 78.4867),
    'Ahmedabad': (23.0225, 72.5714),
    'Pune': (18.5204, 73.8567),
    'Jaipur': (26.9124, 75.7873),
    'Lucknow': (26.8467, 80.9462),
    'Patna': (25.5941, 85.1376),
    'Bhopal': (23.2599, 77.4126),
    'Indore': (22.7196, 75.8577),
    # Add additional locations as needed for better coverage
}

def fetch_outbreak_data():
    url = "https://ghoapi.azureedge.net/api/WHOSIS_000001"  # WHO OData example endpoint
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data['value']
    else:
        print("Failed to fetch data")
        return []

def filter_india_outbreaks(data):
    # Filter only outbreaks in India
    return [item for item in data if item.get('SpatialDim') == 'IND']

def check_nearby_outbreaks(user_location, outbreaks, radius_km=200):
    # Check for nearby outbreaks within a specified radius
    nearby_outbreaks = []
    for outbreak in outbreaks:
        location_name = outbreak.get('ParentLocation')  # Use the region within India if available
        if location_name and location_name in region_coordinates:
            outbreak_coords = region_coordinates[location_name]
            distance = geodesic(user_location, outbreak_coords).km
            if distance <= radius_km:
                nearby_outbreaks.append(outbreak)
    return nearby_outbreaks

# Example usage to simulate user locations across India
if __name__ == "__main__":
    user_locations = [
        (28.6139, 77.2090),  # New Delhi
        (19.0760, 72.8777),  # Mumbai
        (22.5726, 88.3639),  # Kolkata
        (13.0827, 80.2707),  # Chennai
        (26.8467, 80.9462),  # Lucknow
    ]

    for user_location in user_locations:
        print(f"Checking outbreaks for user at location: {user_location}")
        data = fetch_outbreak_data()
        india_outbreaks = filter_india_outbreaks(data)
        nearby_outbreaks = check_nearby_outbreaks(user_location, india_outbreaks, radius_km=200)

        if nearby_outbreaks:
            print(f"Alert: There are {len(nearby_outbreaks)} outbreak(s) within 200 km of your location.")
            for outbreak in nearby_outbreaks:
                print(f" - Disease: {outbreak.get('IndicatorCode')}, Region: {outbreak.get('ParentLocation')}")
        else:
            print(f"No outbreaks within 200 km of your location.")
        print("\n")
