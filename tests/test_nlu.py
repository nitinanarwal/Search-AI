from backend.nlu import parse_intent


def test_parse_intent_zip_and_cause():
    intent = parse_intent("affordable housing near 94103 within 5 miles one-time")
    assert "housing" in intent["causes"]
    assert intent["location"]["zip"] == "94103"
    assert intent["location"]["radius_miles"] in (5, 200)  # clamped or exact
    assert intent["donation_type"] == "one-time"


def test_parse_intent_multiple_causes():
    intent = parse_intent("youth education tutoring in 30303")
    assert set(intent["causes"]) & {"youth", "education"}


