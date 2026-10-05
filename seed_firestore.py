"""
Seed script to populate Firestore with sample travel destination data.
Hardcodes project ID to prevent Agent Platform resolution issues.
"""

from google.cloud import firestore

# IMPORTANT: Hardcoded Project ID string (do not derive from GOOGLE_CLOUD_PROJECT or google.auth.default())
FIRESTORE_PROJECT_ID = "qwiklabs-gcp-03-4d70f29521bc"

DESTINATIONS = [
    {
        "id": "eiffel-tower",
        "name": "Eiffel Tower",
        "city": "Paris",
        "country": "France",
        "category": "Landmark",
        "description": "Iconic 19th-century iron lattice tower on the Champ de Mars with panoramic city views.",
        "price_level": "$$",
        "rating": 4.7,
        "tags": ["monument", "views", "architecture", "iconic"],
    },
    {
        "id": "louvre-museum",
        "name": "Louvre Museum",
        "city": "Paris",
        "country": "France",
        "category": "Museum",
        "description": "World's largest art museum and historic monument housing the Mona Lisa and Venus de Milo.",
        "price_level": "$$",
        "rating": 4.8,
        "tags": ["art", "history", "culture", "museum"],
    },
    {
        "id": "sensoji-temple",
        "name": "Sensō-ji Temple",
        "city": "Tokyo",
        "country": "Japan",
        "category": "Temple",
        "description": "Ancient Buddhist temple located in Asakusa, Tokyo's oldest and most significant temple.",
        "price_level": "$",
        "rating": 4.7,
        "tags": ["temple", "culture", "history", "landmark"],
    },
    {
        "id": "tokyo-skytree",
        "name": "Tokyo Skytree",
        "city": "Tokyo",
        "country": "Japan",
        "category": "Landmark",
        "description": "Broadcasting and observation tower in Sumida, Tokyo, featuring panoramic views across the city.",
        "price_level": "$$",
        "rating": 4.6,
        "tags": ["tower", "views", "modern", "sightseeing"],
    },
    {
        "id": "shibuya-crossing",
        "name": "Shibuya Crossing",
        "city": "Tokyo",
        "country": "Japan",
        "category": "Landmark",
        "description": "Famous scramble crossing outside Shibuya Station, known as the busiest pedestrian intersection in the world.",
        "price_level": "$",
        "rating": 4.8,
        "tags": ["iconic", "city-life", "free", "nightlife"],
    },
    {
        "id": "fushimi-inari",
        "name": "Fushimi Inari-taisha",
        "city": "Kyoto",
        "country": "Japan",
        "category": "Temple",
        "description": "Famous Shinto shrine in southern Kyoto famous for its thousands of vibrant vermilion torii gates.",
        "price_level": "$",
        "rating": 4.8,
        "tags": ["shrine", "torii", "kyoto", "culture", "iconic"],
    },
    {
        "id": "mount-fuji",
        "name": "Mount Fuji",
        "city": "Shizuoka",
        "country": "Japan",
        "category": "Landmark",
        "description": "Japan's highest and most famous active volcano peak, revered as a sacred symbol of beauty.",
        "price_level": "$$",
        "rating": 4.9,
        "tags": ["mountain", "nature", "iconic", "views", "landmark"],
    },
    {
        "id": "colosseum",
        "name": "Colosseum",
        "city": "Rome",
        "country": "Italy",
        "category": "Landmark",
        "description": "Ancient Roman amphitheatre in the centre of the city of Rome, built under the Flavian dynasty.",
        "price_level": "$$",
        "rating": 4.7,
        "tags": ["history", "ancient", "monument", "architecture"],
    },
    {
        "id": "trevi-fountain",
        "name": "Trevi Fountain",
        "city": "Rome",
        "country": "Italy",
        "category": "Landmark",
        "description": "Famous 18th-century Baroque fountain in the Trevi district of Rome.",
        "price_level": "$",
        "rating": 4.8,
        "tags": ["fountain", "baroque", "free", "sightseeing"],
    },
    {
        "id": "sagrada-familia",
        "name": "Basílica de la Sagrada Família",
        "city": "Barcelona",
        "country": "Spain",
        "category": "Landmark",
        "description": "Unfinished masterpiece Roman Catholic church designed by Antoni Gaudí.",
        "price_level": "$$",
        "rating": 4.8,
        "tags": ["gaudi", "architecture", "church", "culture"],
    },
]


def seed_database():
    print(f"Connecting to Firestore in project '{FIRESTORE_PROJECT_ID}'...")
    db = firestore.Client(project=FIRESTORE_PROJECT_ID)
    collection_ref = db.collection("destinations")

    count = 0
    for dest in DESTINATIONS:
        doc_id = dest["id"]
        data = {k: v for k, v in dest.items() if k != "id"}
        collection_ref.document(doc_id).set(data)
        print(f"  ✓ Seeded destination: {dest['name']} ({doc_id})")
        count += 1

    print(f"\nSuccessfully seeded {count} items into the 'destinations' collection!")


if __name__ == "__main__":
    seed_database()
