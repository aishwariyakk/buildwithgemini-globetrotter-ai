"""
Firestore tools for GlobeTrotter AI.
Reads and writes destination data from/to the 'destinations' collection in Firestore.
"""

from typing import Any
from google.cloud import firestore

# IMPORTANT: Hardcoded project ID string (do not derive from GOOGLE_CLOUD_PROJECT or google.auth.default())
FIRESTORE_PROJECT_ID = "qwiklabs-gcp-03-4d70f29521bc"

_db = None


def get_firestore_client() -> firestore.Client:
    global _db
    if _db is None:
        _db = firestore.Client(project=FIRESTORE_PROJECT_ID)
    return _db


def search_destinations(
    city: str | None = None, category: str | None = None
) -> list[dict[str, Any]]:
    """Search for destinations in the travel database by city, country, or category.

    Args:
        city: Optional location/city/country query to filter destinations (e.g. 'Japan', 'Tokyo', 'Paris', 'Rome').
        category: Optional category to filter (e.g. 'Landmark', 'Museum', 'Restaurant').

    Returns:
        A list of destination dictionaries with details including name, city, country, category, description, rating, price_level, and tags.
    """
    db = get_firestore_client()
    collection_ref = db.collection("destinations")

    docs = collection_ref.stream()
    results = []
    q_str = (city or "").strip().lower()

    for doc in docs:
        item = doc.to_dict()
        item["id"] = doc.id

        if not q_str:
            city_match = True
        else:
            c_city = item.get("city", "").lower()
            c_country = item.get("country", "").lower()
            c_name = item.get("name", "").lower()
            c_tags = " ".join(item.get("tags", [])).lower()
            city_match = (q_str in c_city) or (q_str in c_country) or (q_str in c_name) or (q_str in c_tags)

        cat_match = not category or category.lower() in item.get("category", "").lower()

        if city_match and cat_match:
            results.append(item)

    return results


def add_destination(
    name: str,
    city: str,
    country: str,
    category: str,
    description: str,
    price_level: str = "$$",
    rating: float = 4.5,
    tags: list[str] | None = None,
) -> dict[str, Any]:
    """Add a new travel destination or spot to the database.

    Args:
        name: Name of the destination/spot (e.g., 'Park Güell').
        city: City where the destination is located (e.g., 'Barcelona').
        country: Country where the destination is located (e.g., 'Spain').
        category: Category of spot (e.g., 'Landmark', 'Museum', 'Park', 'Restaurant').
        description: A short engaging description of the spot.
        price_level: Price level indicator ('$', '$$', '$$$', '$$$$').
        rating: Rating out of 5.0 (e.g., 4.7).
        tags: List of descriptive tags (e.g. ['views', 'architecture']).

    Returns:
        A dictionary confirming the newly created destination item with its ID.
    """
    db = get_firestore_client()
    collection_ref = db.collection("destinations")

    doc_id = name.lower().replace(" ", "-").replace("'", "")
    data = {
        "name": name,
        "city": city.title(),
        "country": country.title(),
        "category": category.title(),
        "description": description,
        "price_level": price_level,
        "rating": float(rating),
        "tags": tags or [],
    }

    collection_ref.document(doc_id).set(data)
    data["id"] = doc_id
    return {"status": "success", "message": f"Added {name} to destinations.", "destination": data}
