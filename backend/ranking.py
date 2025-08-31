def final_score(semantic, geo_s, trust, popularity):
    # Simple transparent formula; tune via A/B tests
    return 0.6*semantic + 0.2*geo_s + 0.15*trust + 0.05*popularity
