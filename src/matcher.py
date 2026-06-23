import pandas as pd
from typing import Dict, List, Tuple
from src.config import AMENITY_MAPPINGS, MAX_PROPERTIES_PER_BRIEF, MIN_MATCH_SCORE, BUDGET_TOLERANCE

class PropertyMatcher:
    def __init__(self, listings_df: pd.DataFrame):
        self.listings = listings_df

    def find_matches(self, req: Dict) -> List[Dict]:
        candidates = self._apply_filters(self.listings.copy(), req)
        if candidates.empty: candidates = self._apply_relaxed_filters(req)
        if candidates.empty: return []

        scored = []
        for _, row in candidates.iterrows():
            score, reasons = self._score(row, req)
            if score >= MIN_MATCH_SCORE:
                scored.append({**row.to_dict(), 'match_score': round(score, 2), 'match_reasons': reasons})
        
        return sorted(scored, key=lambda x: x['match_score'], reverse=True)[:MAX_PROPERTIES_PER_BRIEF]

    def _apply_filters(self, df: pd.DataFrame, req: Dict) -> pd.DataFrame:
        if req.get('budget_max'): df = df[df['price'] <= req['budget_max'] * (1 + BUDGET_TOLERANCE)]
        if req.get('bedrooms_min'): df = df[df['bedrooms'].isna() | (df['bedrooms'] >= req['bedrooms_min'])]
        
        # SAFETY: Ensure we only compare strings, handle if LLM accidentally returns a list
        pt = req.get('property_type')
        if pt and isinstance(pt, str):
            df = df[df['property_type'].str.strip().str.lower() == pt.strip().lower()]
            
        return df

    def _apply_relaxed_filters(self, req: Dict) -> pd.DataFrame:
        df = self.listings.copy()
        if req.get('budget_max'): df = df[df['price'] <= req['budget_max'] * 1.5]
        return df

    def _score(self, prop: pd.Series, req: Dict) -> Tuple[float, List[str]]:
        s_loc, r_loc = self._s_location(prop, req)
        s_bud, r_bud = self._s_budget(prop, req)
        s_size, r_size = self._s_size(prop, req)
        s_feat, r_feat = self._s_features(prop, req)
        return (s_loc + s_bud + s_size + s_feat) / 100, r_loc + r_bud + r_size + r_feat

    def _s_location(self, p, r):
        prefs = r.get('preferred_locations', [])
        if not prefs: return 15, ["No location pref"]
        p_loc = p.get('neighborhood_lower', '')
        if any(pref.lower() in p_loc for pref in prefs): return 30, [f"✓ In {p['neighborhood']}"]
        return 5, [f"○ In {p['neighborhood']} (not preferred)"]

    def _s_budget(self, p, r):
        price = p.get('price', 0)
        if not r.get('budget_max'): return 12, ["No budget"]
        bmax = r['budget_max']
        if price <= bmax: return (25 if price <= bmax*0.8 else 20), [f"✓ ${price:,.0f} in budget"]
        if price <= bmax*1.15: return 10, [f"△ ${price:,.0f} slightly over"]
        return 0, [f"✗ ${price:,.0f} over budget"]

    def _s_size(self, p, r):
        br = p.get('bedrooms')
        if pd.isna(br): return 5, ["BR unknown"]
        if r.get('bedrooms_min') and br < r['bedrooms_min']: return 0, [f"✗ Only {br} BR"]
        return 20, [f"✓ {br} BR"]

    def _s_features(self, p, r):
        must, nice = r.get('must_have_features', []), r.get('nice_to_have_features', [])
        if not must and not nice: return 12, ["No features req"]
        feats_str = ' '.join(p.get('features_list', []))
        score, reasons = 0, []
        m_met = sum(1 for f in must if self._has(f, feats_str))
        if must: score += 20 * (m_met / len(must))
        n_met = sum(1 for f in nice if self._has(f, feats_str))
        if nice: score += 5 * (n_met / len(nice))
        return min(score, 25), reasons

    def _has(self, feat, feats_str):
        if feat.lower() in feats_str: return True
        for aliases in AMENITY_MAPPINGS.values():
            if feat.lower() in aliases and any(a in feats_str for a in aliases): return True
        return False