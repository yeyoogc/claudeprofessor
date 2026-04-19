"""
Picks a unique palette + layout combination per post topic.
Deterministic (same topic → same design), zero API calls.
5 layouts × 6 palettes = 30 combinations.
"""

import hashlib

PALETTES = ["", "palette-night", "palette-slate", "palette-sand", "palette-ink", "palette-dusk"]
LAYOUTS  = ["layout-a", "layout-b", "layout-c", "layout-d", "layout-e"]


def pick(topic: str) -> dict:
    h = int(hashlib.md5(topic.encode()).hexdigest()[:8], 16)
    palette = PALETTES[h % len(PALETTES)]
    layout  = LAYOUTS[(h // len(PALETTES)) % len(LAYOUTS)]
    return {"palette": palette, "layout": layout}
