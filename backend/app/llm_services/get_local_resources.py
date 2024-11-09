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
    """
    try:
        search_terms = RESOURCE_MAP.get(determine_relevant_specialist(context) or resource_type.lower(),
                                        [resource_type])
        if context:
            search_terms = [f"{context} {term}" for term in search_terms]

        all_results = [gmaps.places_nearby(location=location, radius=SEARCH_RADIUS, keyword=term).get('results', []) for
                       term in search_terms]
        unique_results = {place['place_id']: place for sublist in all_results for place in sublist}.values()
        sorted_results = sorted(unique_results, key=lambda x: (x.get('rating', 0), x.get('user_ratings_total', 0)),
                                reverse=True)

        return [get_detailed_place_info(place['place_id']) for place in sorted_results[:10]]
    except Exception as e:
        raise ValueError(f"Failed to retrieve places: {str(e)}")


# Endpoint for finding labs based on location and test category
# Endpoint for finding labs based on location and test category
def find_lab(location: str, test_category: str) -> List[Dict[str, Union[str, float]]]:
    """
    Find nearby labs offering specific tests based on the user's location and the test category.
    """
    return search_resources(location, f"lab {test_category}")


@lru_cache(maxsize=1000)
def search_resources(location: str, search_term: str) -> List[Dict[str, Union[str, float]]]:
    """
    Search for resources nearby based on location and search term.
    """
    try:
        places_result = gmaps.places_nearby(location=location, radius=SEARCH_RADIUS, keyword=search_term).get('results', [])
        return sorted([get_detailed_place_info(place['place_id']) for place in places_result],
                      key=lambda x: (x.get('rating', 0), x.get('user_ratings_total', 0)), reverse=True)[:10]
    except Exception as e:
        raise ValueError(f"Failed to retrieve resources: {str(e)}")


def determine_relevant_specialist(context: str) -> str:
    """
    Determine the most relevant specialist based on the given context.
    """
    context = context.lower()
    return next((key for key, terms in RESOURCE_MAP.items() if any(term in context for term in terms)), "general")

def get_detailed_place_info(place_id: str) -> Dict[str, Union[str, float, List[str]]]:
    """
    Get detailed information about a place using its place_id.
    """
    place_details = gmaps.place(place_id=place_id, fields=['name', 'formatted_address', 'formatted_phone_number',
                                                           'rating', 'opening_hours', 'website', 'reviews'])['result']
    return {
        'name': place_details.get('name', 'N/A'),
        'address': place_details.get('formatted_address', 'N/A'),
        'phone': place_details.get('formatted_phone_number', 'N/A'),
        'rating': place_details.get('rating', 'N/A'),
        'website': place_details.get('website', 'N/A'),
        'opening_hours': place_details.get('opening_hours', {}).get('weekday_text', []),
        'reviews': [{'text': review['text'], 'rating': review['rating']} for review in place_details.get('reviews', [])[:3]]
    }