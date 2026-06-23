import os
from typing import List, Dict
from groq import Groq
from src.config import GROQ_API_KEY
from src.data_loader import DataLoader
from src.security import SecurityValidator
from src.extractor import RequirementExtractor
from src.matcher import PropertyMatcher
from src.generator import LeadBriefGenerator

class BuyerLeadIntakeAgent:
    def __init__(self, data_dir: str = "data"):
        self.client = Groq(api_key=GROQ_API_KEY)
        self.loader = DataLoader(data_dir)
        self.security = SecurityValidator()
        self.extractor = RequirementExtractor(self.client)
        self.generator = LeadBriefGenerator(self.client)
        
        self.listings = self.loader.load_mls_listings()
        self.matcher = PropertyMatcher(self.listings)

    def process_all(self, inquiries: List[Dict]) -> List[Dict]:
        results = []
        for inq in inquiries:
            print(f"Processing {inq['lead_id']}...")
            is_valid, reason = self.security.validate(inq)
            if not is_valid:
                brief = self.generator.generate(inq, {}, [], blocked=True)
                results.append({'lead_id': inq['lead_id'], 'brief': brief, 'blocked': True, 'matches': 0})
                continue
                
            reqs = self.extractor.extract(inq)
            matches = self.matcher.find_matches(reqs)
            brief = self.generator.generate(inq, reqs, matches)
            results.append({'lead_id': inq['lead_id'], 'brief': brief, 'blocked': False, 'matches': len(matches), 'requirements': reqs})
        return results

    def save_briefs(self, results: List[Dict], out_dir: str = "output/lead_briefs"):
        os.makedirs(out_dir, exist_ok=True)
        for r in results:
            # ADDED: encoding='utf-8' to support emojis on Windows
            with open(f"{out_dir}/{r['lead_id']}_brief.md", 'w', encoding='utf-8') as f: 
                f.write(r['brief'])
                
        # ADDED: encoding='utf-8' here too
        with open(f"{out_dir}/ALL_LEAD_BRIEFS.md", 'w', encoding='utf-8') as f:
            for r in results: 
                f.write(r['brief'] + "\n\n" + "="*80 + "\n\n")
                
        print(f"Saved {len(results)} briefs to {out_dir}/")