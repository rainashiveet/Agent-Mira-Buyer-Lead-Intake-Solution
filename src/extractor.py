import json
from typing import Dict
from groq import Groq
from src.config import EXTRACTION_MODEL, LOCATION_ALIASES

class RequirementExtractor:
    def __init__(self, client: Groq):
        self.client = client

    def extract(self, inquiry: Dict) -> Dict:
        # Changed the prompt to explicitly ask for a STRING, not a list
        prompt = f"""Analyze this buyer inquiry and extract requirements as JSON.
Message: "{inquiry['message']}"
Return JSON:
{{
    "property_type": null or "Condo" or "Single Family" or "Townhouse" or "Villa" or "Multi-Family",
    "bedrooms_min": null or int, "bedrooms_max": null or int,
    "budget_min": null or number, "budget_max": null or number,
    "preferred_locations": [],
    "must_have_features": [],
    "nice_to_have_features": [],
    "move_in_timeline": null or string,
    "buyer_context": "string",
    "is_investor": boolean,
    "urgency": "high" or "medium" or "low"
}}
Rules: "$700K"=700000. "2-3 BR" -> min:2, max:3. "at least 4" -> min:4, max:null. Standardize features: "gym", "pool", "garage", "waterfront", "pet friendly", "balcony", "home office", "boat dock". Return ONLY JSON."""

        try:
            response = self.client.chat.completions.create(
                model=EXTRACTION_MODEL,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1,
                response_format={"type": "json_object"}
            )
            reqs = json.loads(response.choices[0].message.content)
            
            # SAFETY CHECK: Force property_type to be a string, not a list
            pt = reqs.get('property_type')
            if isinstance(pt, list):
                reqs['property_type'] = pt[0] if pt else None
                
            reqs['preferred_locations'] = [LOCATION_ALIASES.get(loc.lower(), loc) for loc in reqs.get('preferred_locations', [])]
            
            # Fix budget inversion if it happens
            if reqs.get('budget_min') and reqs.get('budget_max') and reqs['budget_min'] > reqs['budget_max']:
                reqs['budget_min'], reqs['budget_max'] = reqs['budget_max'], reqs['budget_min']
            return reqs
        except Exception as e:
            print(f"Extraction error: {e}")
            return self._fallback(inquiry['message'])

    def _fallback(self, msg: str) -> Dict:
        return {"property_type": None, "bedrooms_min": None, "bedrooms_max": None,
                "budget_min": None, "budget_max": None, "preferred_locations": [],
                "must_have_features": [], "nice_to_have_features": [],
                "move_in_timeline": None, "buyer_context": msg[:200],
                "is_investor": False, "urgency": "medium"}