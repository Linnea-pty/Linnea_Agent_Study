from functools import lru_cache
from chat.models import CODING_KEYWORDS, REASONING_KEYWORDS, Tier

@lru_cache(maxsize=256)
def decide_tier(task: str) -> Tier:
    text = task.strip().lower()
    if any(w in text for w in CODING_KEYWORDS):
        return Tier.BALANCED
    if any(w in text for w in REASONING_KEYWORDS):
        return Tier.BALANCED
    return Tier.FAST