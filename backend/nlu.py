import re

CAUSE_CANON = {
    "housing": ["housing", "affordable housing", "homeless", "shelter", "rent"],
    "families": ["families", "family", "children", "kids"],
    "mental health": ["mental health", "ptsd", "therapy", "counseling"],
    "veterans": ["veteran", "veterans"],
    "education": ["education", "school", "tutoring", "stem"],
    "youth": ["youth", "teen", "teenagers"],
    "legal": ["legal", "law", "eviction"]
}


def parse_intent(query: str):
    q = (query or "").lower().strip()

    # zip (US 5 digits)
    zip_match = re.search(r"\b(\d{5})\b", q)
    zip_code = zip_match.group(1) if zip_match else None

    # radius (e.g., "within 10 miles", "10mi", "radius 15")
    rad_match = re.search(r"(?:within|radius)?\s*(\d{1,3})\s*(?:mi|miles|km)?", q)
    radius_miles = int(rad_match.group(1)) if rad_match else None
    if radius_miles and radius_miles > 200:  # clamp silly values
        radius_miles = 200

    # donation type
    donation_type = "one-time" if "one-time" in q or "one time" in q else ("recurring" if "recurring" in q or "monthly" in q else None)

    # causes
    causes = set()
    for canon, variants in CAUSE_CANON.items():
        if any(v in q for v in variants):
            causes.add(canon)

    return {
        "causes": sorted(list(causes)) if causes else None,
        "location": {"zip": zip_code, "radius_miles": radius_miles} if zip_code or radius_miles else None,
        "donation_type": donation_type
    }


