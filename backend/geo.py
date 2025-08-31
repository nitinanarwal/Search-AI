import math

ZIP_TO_LATLON = {
    "94103": (37.7763, -122.4167),
    "94105": (37.7892, -122.3960),
    "94102": (37.7784, -122.4175),
    "94901": (37.9735, -122.5311),
    "85004": (33.4510, -112.0730),
    "30303": (33.7537, -84.3884),
    "95113": (37.3348, -121.8906)
}

def haversine_miles(lat1, lon1, lat2, lon2):
    # radius of Earth in miles
    R = 3958.8
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlmb = math.radians(lon2 - lon1)
    a = (math.sin(dphi/2)**2 +
         math.cos(p1) * math.cos(p2) * math.sin(dlmb/2)**2)
    return 2 * R * math.asin(math.sqrt(a))

def geo_score_miles(distance_miles, max_radius_miles):
    if max_radius_miles is None or max_radius_miles <= 0:
        return 0.0
    # score decays linearly to 0 at max radius
    s = max(0.0, 1.0 - (distance_miles / max_radius_miles))
    return s
