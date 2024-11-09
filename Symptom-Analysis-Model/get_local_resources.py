from typing import List, Dict, Union
import googlemaps
from config import GOOGLE_CLOUD_KEY
from functools import lru_cache

# Constants
SEARCH_RADIUS = 5000  # meters

# Initialize the Google Maps client
gmaps = googlemaps.Client(key=GOOGLE_CLOUD_KEY)

# Expanded resource map
RESOURCE_MAP = {
    "general": ["general practitioner", "family doctor"],
    "stomach": ["gastroenterologist", "digestive health specialist"],
    "heart": ["cardiologist", "heart specialist"],
    "skin": ["dermatologist", "skin doctor"],
    "bones": ["orthopedist", "bone specialist"],
    "mental health": ["psychiatrist", "psychologist", "therapist"],
    "children": ["pediatrician", "child health specialist"],
    "women's health": ["gynecologist", "obstetrician"],
    "eye": ["ophthalmologist", "optometrist", "eye doctor"],
    "ear_nose_throat": ["otolaryngologist", "ENT specialist"],
    "nervous system": ["neurologist", "brain specialist"],
    "cancer": ["oncologist", "cancer specialist"],
    "hormones": ["endocrinologist", "hormone specialist"],
    "kidney": ["nephrologist", "kidney specialist"],
    "lungs": ["pulmonologist", "lung specialist"],
    "joints": ["rheumatologist", "arthritis specialist"],
    "blood": ["hematologist", "blood specialist"],
    "allergy": ["allergist", "immunologist"],
    "surgery": ["surgeon"],
    "pharmacy": ["pharmacy", "drugstore"],
    "emergency": ["emergency room", "urgent care"],
    "hospital": ["hospital", "medical center"],
    "clinic": ["clinic", "health center"],
}


@lru_cache(maxsize=100)
def get_lat_long_from_city(city_name: str) -> str:
    """
    Convert a city name into latitude and longitude using the Google Maps Geocoding API.

    Args:
        city_name (str): The name of the city to geocode.

    Returns:
        str: A string in the format "latitude,longitude".

    Raises:
        ValueError: If the geocoding fails or no results are found.
    """
    try:
        geocode_result = gmaps.geocode(city_name)
        if not geocode_result:
            raise ValueError(f"No results found for city: {city_name}")

        location = geocode_result[0]['geometry']['location']
        return f"{location['lat']},{location['lng']}"
    except Exception as e:
        raise ValueError(f"Geocoding failed for city {city_name}: {str(e)}")


def is_valid_lat_long(location: str) -> bool:
    """
    Check if the given location string is a valid latitude,longitude format.

    Args:
        location (str): The location string to check.

    Returns:
        bool: True if the location is in valid lat,long format, False otherwise.
    """
    parts = location.split(',')
    if len(parts) != 2:
        return False

    try:
        lat, lon = map(float, parts)
        return -90 <= lat <= 90 and -180 <= lon <= 180
    except ValueError:
        return False


@lru_cache(maxsize=1000)
def get_local_resources(location: str, resource_type: str, context: str = "") -> List[Dict[str, Union[str, float]]]:
    """
    Retrieve nearby resources based on the user's location, specified resource type, and context.

    Args:
        location (str): The user's location, either in 'latitude,longitude' format or a city name.
        resource_type (str): The type of resource to find (e.g., clinic, pharmacy, hospital).
        context (str): Additional context to refine the search (e.g., "stomach ache" for relevant specialists).

    Returns:
        List[Dict[str, Union[str, float]]]: A list of places matching the specified resource type and context.

    Raises:
        ValueError: If the location is invalid or places retrieval fails.
    """
    if not is_valid_lat_long(location):
        location = get_lat_long_from_city(location)

    try:
        # Determine the most relevant specialist based on the context
        relevant_specialist = determine_relevant_specialist(context)

        # Get the appropriate search terms
        search_terms = RESOURCE_MAP.get(relevant_specialist, RESOURCE_MAP.get(resource_type.lower(), [resource_type]))

        # If context is provided, add it to the search query
        if context:
            search_terms = [f"{context} {term}" for term in search_terms]

        all_results = []
        for term in search_terms:
            places_result = gmaps.places_nearby(location=location, radius=SEARCH_RADIUS, keyword=term)
            all_results.extend(places_result.get('results', []))

        # Remove duplicates based on place_id
        unique_results = {place['place_id']: place for place in all_results}.values()

        # Sort results by prominence (if available) or rating
        sorted_results = sorted(unique_results, key=lambda x: (x.get('rating', 0), x.get('user_ratings_total', 0)), reverse=True)

        return [get_detailed_place_info(place['place_id']) for place in sorted_results[:10]]  # Return top 10 results with detailed info
    except Exception as e:
        raise ValueError(f"Failed to retrieve places: {str(e)}")


def determine_relevant_specialist(context: str) -> str:
    """
    Determine the most relevant specialist based on the given context.

    Args:
        context (str): The context of the health issue.

    Returns:
        str: The key of the most relevant specialist in the RESOURCE_MAP.
    """
    context = context.lower()
    for key, terms in RESOURCE_MAP.items():
        if any(term in context for term in terms):
            return key
    return "general"  # Default to general practitioner if no specific match is found


def get_detailed_place_info(place_id: str) -> Dict[str, Union[str, float, List[str]]]:
    """
    Get detailed information about a place using its place_id.

    Args:
        place_id (str): The Google Places API place_id.

    Returns:
        Dict[str, Union[str, float, List[str]]]: A dictionary containing detailed place information.
    """
    place_details = gmaps.place(place_id=place_id, fields=['name', 'formatted_address', 'formatted_phone_number',
                                                           'rating', 'opening_hours', 'website', 'reviews'])

    result = place_details['result']

    return {
        'name': result.get('name', 'N/A'),
        'address': result.get('formatted_address', 'N/A'),
        'phone': result.get('formatted_phone_number', 'N/A'),
        'rating': result.get('rating', 'N/A'),
        'website': result.get('website', 'N/A'),
        'opening_hours': result.get('opening_hours', {}).get('weekday_text', []),
        'reviews': [{'text': review['text'], 'rating': review['rating']} for review in result.get('reviews', [])[:3]]
    }


def format_place_result(place: Dict[str, Union[str, float, List[str]]]) -> str:
    """
    Format a single place result into a human-readable string.

    Args:
        place (Dict[str, Union[str, float, List[str]]]): The place data.

    Returns:
        str: A formatted string with relevant place information.
    """
    formatted_result = f"Name: {place['name']}\n"
    formatted_result += f"Address: {place['address']}\n"
    formatted_result += f"Phone: {place['phone']}\n"
    formatted_result += f"Rating: {place['rating']}\n"
    formatted_result += f"Website: {place['website']}\n"

    if place['opening_hours']:
        formatted_result += "Opening Hours:\n"
        for hours in place['opening_hours']:
            formatted_result += f"  {hours}\n"

    if place['reviews']:
        formatted_result += "Top Reviews:\n"
        for review in place['reviews']:
            formatted_result += f"  - Rating: {review['rating']}/5, Comment: {review['text'][:100]}...\n"

    return formatted_result