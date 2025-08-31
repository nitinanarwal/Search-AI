from backend.geo import haversine_miles, geo_score_miles, ZIP_TO_LATLON


def test_haversine_and_geo_score():
    sf = ZIP_TO_LATLON["94103"]  # (lat, lon)
    sf2 = ZIP_TO_LATLON["94102"]
    d = haversine_miles(sf[0], sf[1], sf2[0], sf2[1])
    assert d >= 0
    s = geo_score_miles(d, 10)
    assert 0.0 <= s <= 1.0


