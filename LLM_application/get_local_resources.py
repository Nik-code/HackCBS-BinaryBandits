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


@lru_cache(maxsize=1000)
def get_local_resources(location: str, resource_type: str, context: str = "") -> List[Dict[str, Union[str, float]]]:
    """
    Retrieve nearby resources based on the user's location, specified resource type, and context.

    Args:
        location (str): The user's location, in 'latitude,longitude' format.
        resource_type (str): The type of resource to find (e.g., clinic, pharmacy, hospital).
        context (str): Additional context to refine the search (e.g., "stomach ache" for relevant specialists).

    Returns:
        List[Dict[str, Union[str, float]]]: A list of places matching the specified resource type and context.

    Raises:
        ValueError: If the location is invalid or places retrieval fails.
    """

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


# Endpoint for finding labs based on location and test category
@app.get("/find_lab")
def find_lab(location: str, test_category: str) -> List[Dict[str, Union[str, float]]]:
    """
    Find nearby labs offering specific tests based on the user's location and the test category.

    Args:
        location (str): The user's location, either in 'latitude,longitude' format or a city name.
        test_category (str): The test category or type (e.g., "blood test", "MRI", "X-ray").

    Returns:
        List[Dict[str, Union[str, float]]]: A list of labs offering the specified test.
    """
    if not is_valid_lat_long(location):
        location = get_lat_long_from_city(location)

    try:
        labs = search_labs_nearby(location, test_category)
        if not labs:
            raise HTTPException(status_code=404, detail="No labs found offering the specified test.")
        return labs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@lru_cache(maxsize=1000)
def search_labs_nearby(location: str, test_category: str) -> List[Dict[str, Union[str, float]]]:
    """
    Search for labs nearby based on location and test category.

    Args:
        location (str): The user's location, either in 'latitude,longitude' format or a city name.
        test_category (str): The test category (e.g., "blood test").

    Returns:
        List[Dict[str, Union[str, float]]]: A list of labs that match the test category.
    """
    try:
        # Search labs with specified test in the Google Maps API
        search_term = f"lab {test_category}"
        places_result = gmaps.places_nearby(location=location, radius=SEARCH_RADIUS, keyword=search_term)

        # Filter and process results
        labs = []
        for place in places_result.get('results', []):
            labs.append(get_detailed_place_info(place['place_id']))

        # Sort by rating or other factors
        return sorted(labs, key=lambda x: (x.get('rating', 0), x.get('user_ratings_total', 0)), reverse=True)[:10]
    except Exception as e:
        raise ValueError(f"Failed to retrieve labs: {str(e)}")


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