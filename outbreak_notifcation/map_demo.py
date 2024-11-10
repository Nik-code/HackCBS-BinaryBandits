import folium
from geopy.distance import geodesic
from folium.features import DivIcon

# Expanded location coordinates for various regions in India
region_coordinates = {
    'Delhi': (28.6139, 77.2090),
    'Mumbai': (19.0760, 72.8777),
    'Bengaluru': (12.9716, 77.5946),
    'Kolkata': (22.5726, 88.3639),
    'Chennai': (13.0827, 80.2707),
    'Hyderabad': (17.3850, 78.4867),
}

# Mock outbreak data with different diseases and case numbers
mock_outbreaks = [
    {'ParentLocation': 'Delhi', 'IndicatorCode': 'Dengue Fever', 'cases': 1500},
    {'ParentLocation': 'Mumbai', 'IndicatorCode': 'Cholera', 'cases': 2300},
    {'ParentLocation': 'Bengaluru', 'IndicatorCode': 'Malaria', 'cases': 3000},
    {'ParentLocation': 'Kolkata', 'IndicatorCode': 'COVID-19', 'cases': 12000},
    {'ParentLocation': 'Chennai', 'IndicatorCode': 'Typhoid', 'cases': 900},
    {'ParentLocation': 'Hyderabad', 'IndicatorCode': 'Ebola', 'cases': 405},
]

# Disease properties: color and radius in meters
disease_properties = {
    'Dengue Fever': {'color': 'red', 'radius': 75000},
    'Cholera': {'color': 'blue', 'radius': 90000},
    'Malaria': {'color': 'green', 'radius': 58000},
    'COVID-19': {'color': 'purple', 'radius': 65000},
    'Typhoid': {'color': 'orange', 'radius': 42000},
    'Ebola': {'color': 'brown', 'radius': 52000},
}


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

    # Add outbreak circles with different colors, sizes, and case count labels
    for outbreak in outbreaks:
        disease = outbreak.get('IndicatorCode')
        location_name = outbreak.get('ParentLocation')
        cases = outbreak.get('cases')

        if location_name in region_coordinates and disease in disease_properties:
            outbreak_coords = region_coordinates[location_name]
            properties = disease_properties[disease]

            # Add a circle to represent the outbreak
            folium.Circle(
                location=outbreak_coords,
                radius=properties['radius'],  # Radius in meters for each disease
                color=properties['color'],
                fill=True,
                fill_color=properties['color'],
                fill_opacity=0.4,
                popup=f"Disease: {disease}<br>Region: {location_name}<br>Cases: ~{cases}"
            ).add_to(outbreak_map)

            # Add a label to show the approximate number of cases
            folium.Marker(
                location=outbreak_coords,
                icon=DivIcon(
                    icon_size=(120, 25),
                    icon_anchor=(0, 0),
                    html=f'<div style="font-size: 14px; color: black; background-color: white; padding: 2px; border-radius: 3px; text-align: center;">~{cases} cases</div>'
                )
            ).add_to(outbreak_map)

    # Add a custom legend to the map
    legend_html = '''
     <div style="position: fixed; 
     bottom: 50px; left: 50px; width: 200px; height: 180px; 
     border:2px solid grey; z-index:9999; font-size:14px;
     background-color:white; padding: 10px;">
     <strong>Disease Legend</strong><br>
     <i style="background:red; width: 10px; height: 10px; float: left; margin-right: 5px; border-radius: 50%;"></i>Dengue Fever<br>
     <i style="background:blue; width: 10px; height: 10px; float: left; margin-right: 5px; border-radius: 50%;"></i>Cholera<br>
     <i style="background:green; width: 10px; height: 10px; float: left; margin-right: 5px; border-radius: 50%;"></i>Malaria<br>
     <i style="background:purple; width: 10px; height: 10px; float: left; margin-right: 5px; border-radius: 50%;"></i>COVID-19<br>
     <i style="background:orange; width: 10px; height: 10px; float: left; margin-right: 5px; border-radius: 50%;"></i>Typhoid<br>
     <i style="background:brown; width: 10px; height: 10px; float: left; margin-right: 5px; border-radius: 50%;"></i>Ebola<br>
     </div>
     '''

    # Add legend to the map
    outbreak_map.get_root().html.add_child(folium.Element(legend_html))

    return outbreak_map


# Main function to create the map with mock data and save it as an HTML file
if __name__ == "__main__":
    user_location = (28.6139, 77.2090)  # Example user location (New Delhi)

    # Create the map with mock outbreak data and user location
    outbreak_map = create_outbreak_map(mock_outbreaks, user_location=user_location, radius_km=200)

    # Save map as HTML
    outbreak_map.save("outbreak_map_demo.html")
    print("Outbreak map demo with legend and case labels has been saved as 'outbreak_map_demo.html'")
