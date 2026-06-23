import os

# --- API Configuration ---
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

# UPDATED: Active Groq Models (Mixtral was decommissioned)
EXTRACTION_MODEL = "llama-3.1-8b-instant"        # Fast, excellent for JSON extraction
REASONING_MODEL = "llama-3.3-70b-versatile"       # Best reasoning for brief generation

# --- Matching Configuration ---
MAX_PROPERTIES_PER_BRIEF = 5
MIN_MATCH_SCORE = 0.25
BUDGET_TOLERANCE = 0.15  # 15% over budget is acceptable

# --- Feature Mappings (for robust matching) ---
AMENITY_MAPPINGS = {
    "gym": ["gym", "fitness center", "exercise room"],
    "pool": ["pool", "swimming pool"],
    "parking": ["garage", "parking", "parking space"],
    "waterfront": ["waterfront", "bay view", "ocean view", "boat dock", "water view"],
    "pet_friendly": ["pet friendly", "pets allowed"],
    "elevator": ["elevator", "elevator access"],
    "balcony": ["balcony", "terrace", "patio"],
    "home_office": ["home office", "office"],
    "updated_kitchen": ["updated kitchen", "modern kitchen", "new kitchen"],
    "security": ["gated", "gated community", "security gate"],
}

# --- Location Aliases ---
LOCATION_ALIASES = {
    "brickell": "Brickell", "downtown miami": "Downtown Miami", "downtown": "Downtown Miami",
    "coral gables": "Coral Gables", "pinecrest": "Pinecrest", "aventura": "Aventura",
    "north miami": "North Miami", "coconut grove": "Coconut Grove", 
    "key biscayne": "Key Biscayne", "bal harbour": "Bal Harbour", "wynwood": "Wynwood",
    "miami beach": "Miami Beach", "south beach": "South Beach", "edgewater": "Edgewater",
}