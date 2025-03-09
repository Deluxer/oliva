from pathlib import Path
from pydantic import SecretStr
import os

class Constants:
    """Constants for LangChain integration"""
    # Configuration constants
    CHUNK_SIZE = 100
    CHUNK_OVERLAP = 50
    EMBEDDING_MODEL = "text-embedding-3-small"
    LLM_MODEL = "gpt-4o-mini"
    OPENAI_API_KEY = SecretStr(os.getenv("OPENAI_API_KEY"))

    # URLs for document loading
    URLS = [
        "https://blog.langchain.dev/what-is-an-agent/",
    ]
    
    PROCESSED_DATASET_PATH: Path = (
        Path("data") / "processed_100_sample.jsonl"
    )

    SPLK_TYPES = ["product", "book"]

    SPLK_CATEGORIES = [
        "Accessories",
        "Appliances",
        "Arts & Photography",
        "Arts, Crafts & Sewing",
        "Automotive",
        "Baby Care",
        "Baby Products",
        "Bath",
        "Beauty & Personal Care",
        "Bedding",
        "Beverages",
        "Biographies & Memoirs",
        "Books",
        "CDs & Vinyl",
        "Camera & Photo",
        "Cell Phones & Accessories",
        "Children's Books",
        "Christian Books & Bibles",
        "Classical",
        "Clothing, Shoes & Jewelry",
        "Computers & Accessories",
        "Costumes & Accessories",
        "Dogs",
        "Electrical",
        "Electronics",
        "Event & Party Supplies",
        "Exercise & Fitness",
        "Exterior Accessories",
        "GPS, Finders & Accessories",
        "Grocery & Gourmet Food",
        "Hair Care",
        "Health & Household",
        "Home & Kitchen",
        "Hunting & Fishing",
        "Industrial & Scientific",
        "Industrial Electrical",
        "Kitchen & Dining",
        "Lighting Assemblies & Accessories",
        "Lights & Lighting Accessories",
        "Luggage & Travel Gear",
        "Makeup",
        "Medical Supplies & Equipment",
        "Men",
        "Movies & TV",
        "Musical Instruments",
        "Office & School Supplies",
        "Office Products",
        "Patio Furniture & Accessories",
        "Patio, Lawn & Garden",
        "Pet Supplies",
        "Pop",
        "Portable Audio & Video",
        "Power & Hand Tools",
        "Raw Materials",
        "Replacement Parts",
        "Self-Help",
        "Sports & Outdoor Play",
        "Sports & Outdoors",
        "Stuffed Animals & Plush Toys",
        "Tires & Wheels",
        "Tools & Home Improvement",
        "Toy Figures & Playsets",
        "Toys & Games",
        "Vehicles",
        "Video Games",
        "Wall Art",
        "Women",
    ]

    QDRANT_DATABASE_URL = SecretStr(os.getenv("QDRANT_URL"))
    QDRANT_DATABASE_API_KEY = SecretStr(os.getenv("QDRANT_API_KEY"))


# Create a singleton instance
constants = Constants()