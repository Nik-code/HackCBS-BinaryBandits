import requests
import folium
from geopy.distance import geodesic
from folium.plugins import MarkerCluster

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


def create_outbreak_map(outbreaks, user_location=None, radius_km=200):
    # Initialize map, centered on India
    outbreak_map = folium.Map(location=[20.5937, 78.9629], zoom_start=5)

    # Add user location marker if provided
    if user_location:
        folium.Marker(
            location=user_location,
            popup="Your Location",
            icon=folium.Icon(color="blue", icon="info-sign")
        ).add_to(outbreak_map)

    # Create a marker cluster to group close outbreak points
    marker_cluster = MarkerCluster().add_to(outbreak_map)

    # Add outbreak markers to the map
    for outbreak in outbreaks:
        location_name = outbreak.get('ParentLocation')
        if location_name in region_coordinates:
            outbreak_coords = region_coordinates[location_name]
            # Calculate distance if user_location is provided
            if user_location:
                distance = geodesic(user_location, outbreak_coords).km
                if distance > radius_km:
                    continue  # Skip outbreaks outside the specified radius

            # Add outbreak marker
            folium.Marker(
                location=outbreak_coords,
                popup=f"Disease: {outbreak.get('IndicatorCode')}<br>Region: {location_name}",
                icon=folium.Icon(color="red", icon="alert")
            ).add_to(marker_cluster)

    return outbreak_map


# Main function to create the map and save it as an HTML file
if __name__ == "__main__":
    user_location = (28.6139, 77.2090)  # Example user location (New Delhi)

    # Fetch outbreak data
    data = fetch_outbreak_data()
    india_outbreaks = filter_india_outbreaks(data)

    # Create the map with outbreak data and user location
    outbreak_map = create_outbreak_map(india_outbreaks, user_location=user_location, radius_km=200)

    # Save map as HTML
    outbreak_map.save("outbreak_map.html")
    print("Outbreak map has been saved as 'outbreak_map.html'")
