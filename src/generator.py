from typing import Dict, List
from groq import Groq
from src.config import REASONING_MODEL

class LeadBriefGenerator:
    def __init__(self, client: Groq):
        self.client = client

    def generate(self, inquiry: Dict, req: Dict, matches: List[Dict], blocked: bool = False) -> str:
        if blocked: return self._blocked_brief(inquiry)
        
        # Safely format to prevent NoneType formatting errors
        match_str = "\n\n".join([
            f"- {m['address']} (${m['price']:,.0f}) | {m['property_type']} | {m['bedrooms']}BR | Score: {m['match_score']*100:.0f}% | Features: {m['features']}"
            for m in matches
        ]) if matches else "NO MATCHES FOUND"

        # Safely extract values, using fallbacks if extraction returned None
        budget_max = req.get('budget_max') or 0
        beds_min = req.get('bedrooms_min') or '?'
        beds_max = req.get('bedrooms_max') or '+'
        prop_type = req.get('property_type') or 'Any'
        locs = ', '.join(req.get('preferred_locations', [])) or 'Any'
        must_haves = ', '.join(req.get('must_have_features', [])) or 'None specified'
        is_investor = req.get('is_investor') or False

        prompt = f"""Realtor Lead Brief. Generate clean Markdown.

Buyer: {inquiry.get('buyer_name')} | ID: {inquiry['lead_id']} | Source: {inquiry.get('channel')}
Contact: {inquiry.get('buyer_email')} | {inquiry.get('buyer_phone') or 'No Phone'}
Message: "{inquiry.get('message')}"

Extracted Needs: Type:{prop_type} | Beds:{beds_min}-{beds_max} | Budget:${budget_max:,.0f} | Locs:{locs} | Must:{must_haves} | Investor:{is_investor}

Matching Properties:
{match_str}

Create this exact structure:
# Lead Brief: [Name]
## 📋 Executive Summary (2 sentences)
## 👤 Buyer Profile (Situation, Timeline, Budget, Source in a clean list)
## ✅ Must-Have Requirements (bullet points)
## 🌟 Nice-to-Have Features (bullet points)
## 🏠 Recommended Properties (For each: Address, Price, Specs, Why it fits, Concerns)
## ⚠️ Things to Clarify (Questions for first call)
## 🎯 Suggested Next Steps (1, 2, 3)
## 📝 Notes for Realtor (Red flags, strategy, missing info)"""

        try:
            resp = self.client.chat.completions.create(
                model=REASONING_MODEL, 
                messages=[{"role":"user","content":prompt}], 
                temperature=0.3, 
                max_tokens=2500
            )
            return resp.choices[0].message.content
        except Exception as e:
            return f"Error generating brief: {e}"

    def _blocked_brief(self, inquiry: Dict) -> str:
        return f"""# 🚨 SECURITY ALERT: {inquiry.get('lead_id')}\n\n**Status:** BLOCKED\n**Reason:** Prompt injection detected attempting to extract database PII.\n\n**Action:** Do not process. Flag for admin review."""