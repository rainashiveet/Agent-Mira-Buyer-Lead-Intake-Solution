import re
from typing import Dict, Tuple

class SecurityValidator:
    INJECTION_PATTERNS = [
        r'ignore\s+(all\s+)?previous\s+instructions',
        r'forget\s+(all\s+)?previous', r'disregard\s+(all\s+)?previous',
        r'you\s+are\s+now', r'act\s+as\s+if', r'pretend\s+you\s+are',
        r'respond\s+by\s+listing', r'output\s+(all\s+)?(names?|phones?|data)',
        r'show\s+me\s+(all\s+)?(names?|phones?|data)', r'dump\s+(the\s+)?database',
        r'system\s+prompt', r'reveal\s+your\s+(instructions?|prompt)',
    ]

    def validate(self, inquiry: Dict) -> Tuple[bool, str]:
        message = inquiry.get('message', '').lower()
        for pattern in self.INJECTION_PATTERNS:
            if re.search(pattern, message, re.IGNORECASE):
                return False, "PROMPT_INJECTION_DETECTED"
        return True, ""