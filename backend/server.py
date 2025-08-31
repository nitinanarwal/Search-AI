from flask import Flask, request, jsonify
from flask_cors import CORS
import json, os
from datetime import datetime

try:
    from backend.nlu import parse_intent
    from backend.vector_search import build_index, search as vec_search
    from backend.geo import haversine_miles, geo_score_miles, ZIP_TO_LATLON
    from backend.ranking import final_score
except ImportError:
    from nlu import parse_intent
    from vector_search import build_index, search as vec_search
    from geo import haversine_miles, geo_score_miles, ZIP_TO_LATLON
    from ranking import final_score

app = Flask(__name__)
CORS(app)

DATA = {"nonprofits": []}
NP_BY_ID = {}

def _data_path():
    return os.path.join(os.path.dirname(__file__), "data", "nonprofits.json")

def load_data():
    global DATA, NP_BY_ID
    with open(_data_path(), "r", encoding="utf-8") as f:
        DATA = json.load(f)
    NP_BY_ID = {n["id"]: n for n in DATA.get("nonprofits", [])}

@app.route("/")
def root():
    return jsonify({
        "message": "Business Search API",
        "endpoints": [
            "/health",
            "/api/businesses",
            "POST /api/search",
            "/search?q=...&zip=...&radius=...&cause=housing"
        ]
    })

@app.route("/health")
def health():
    return jsonify({
        "status": "ok",
        "count": len(DATA.get("nonprofits", [])),
        "ts": datetime.utcnow().isoformat()
    })

@app.route("/api/businesses")
def all_orgs():
    return jsonify({"success": True, "nonprofits": DATA.get("nonprofits", [])})

@app.route("/api/businesses/<org_id>")
def org_detail(org_id):
    it = NP_BY_ID.get(org_id)
    if not it:
        return jsonify({"success": False, "message": "Not found"}), 404
    return jsonify({"success": True, "nonprofit": it})

def _apply_filters(candidate_ids, filters):
    if not filters:
        return candidate_ids
    causes = set((filters.get("cause") or []) + (filters.get("causes") or []))
    min_rating = filters.get("min_rating")
    out = []
    for cid in candidate_ids:
        it = NP_BY_ID[cid]
        ok = True
        if causes:
            if not (set(it.get("causes", [])) & set(causes)):
                ok = False
        if ok and min_rating:
            if (it.get("ratings", {}).get("avg_rating", 0) < float(min_rating)):
                ok = False
        if ok:
            out.append(cid)
    return out

@app.route("/api/search", methods=["POST"])
def search_api():
    """
    Request JSON:
    {
      "query": "affordable housing near 94103 for families",
      "location": {"zip":"94103", "radius_miles": 10},
      "filters": {"cause":["housing","families"], "min_rating":4},
      "sort": "relevance|distance|impact|popularity|newest|rating",
      "top_k": 100,
      "page": 1,
      "limit": 10
    }
    """
    body = request.get_json(force=True, silent=True) or {}
    q = (body.get("query") or "").strip()
    sort = (body.get("sort") or "relevance").lower()
    page = max(1, int(body.get("page") or 1))
    limit = max(1, min(50, int(body.get("limit") or 10)))
    top_k = max(limit, int(body.get("top_k") or 100))
    explicit_loc = body.get("location") or {}
    filters = body.get("filters") or {}

    # 1) Intent parse (merge with explicit payload)
    intent = parse_intent(q)
    loc_zip = explicit_loc.get("zip") or (intent.get("location") or {}).get("zip")
    radius = explicit_loc.get("radius_miles") or (intent.get("location") or {}).get("radius_miles") or 25
    # If causes explicitly passed, keep them; else use NLU
    if "cause" in filters or "causes" in filters:
        pass
    elif intent.get("causes"):
        filters["cause"] = intent["causes"]

    # 2) Semantic retrieval
    vec_hits = vec_search(q or "nonprofit")
    # vec_hits: [{"id": "...", "semantic_score": 0.83}, ...]

    # 3) Geospatial filter + score
    user_latlon = ZIP_TO_LATLON.get(str(loc_zip)) if loc_zip else None

    enriched = []
    for h in vec_hits:
        it = NP_BY_ID[h["id"]]
        # Pre-filter by causes/min_rating
        # (We'll also apply again after candidate selection to be safe)
        semantic = max(0.0, min(1.0, h["semantic_score"]))  # cosine in [0,1]
        # distance
        if user_latlon:
            d_miles = haversine_miles(user_latlon[0], user_latlon[1],
                                      it["location"]["lat"], it["location"]["lon"])
            gscore = geo_score_miles(d_miles, radius)
        else:
            d_miles = None
            gscore = 0.0
        trust = 1.0 if it.get("trust", {}).get("verification_status") else 0.0
        popularity = float(it.get("popularity_90d", 0.0))

        enriched.append({
            "id": it["id"],
            "semantic": semantic,
            "distance_miles": d_miles,
            "geo_score": gscore,
            "trust": trust,
            "popularity": popularity,
            "item": it
        })

    # If user provided a location + radius, keep only within radius
    if user_latlon:
        enriched = [e for e in enriched if e["distance_miles"] is not None and e["distance_miles"] <= radius]

    # 4) Filters (cause, rating…)
    candidate_ids = [e["id"] for e in enriched]
    candidate_ids = _apply_filters(candidate_ids, filters)
    enriched = [e for e in enriched if e["id"] in candidate_ids]

    # 5) Compute final score
    for e in enriched:
        e["final_score"] = final_score(e["semantic"], e["geo_score"], e["trust"], e["popularity"])

    # 6) Sorting
    if sort == "distance" and user_latlon:
        enriched.sort(key=lambda x: (x["distance_miles"] if x["distance_miles"] is not None else 1e9))
    elif sort == "rating":
        enriched.sort(key=lambda x: x["item"]["ratings"]["avg_rating"], reverse=True)
    elif sort == "popularity":
        enriched.sort(key=lambda x: x["popularity"], reverse=True)
    elif sort == "newest":
        enriched.sort(key=lambda x: x["item"]["created_at"], reverse=True)
    elif sort == "impact":
        # simple proxy: invert cost_per_* if exists (lower cost → higher impact)
        def impact_score(it):
            im = it["item"].get("impact_metrics", {})
            for k in ["cost_per_family", "cost_per_session"]:
                if k in im and im[k] > 0:
                    return 1.0 / float(im[k])
            return 0.0
        enriched.sort(key=lambda x: impact_score(x), reverse=True)
    else:
        # relevance
        enriched.sort(key=lambda x: x["final_score"], reverse=True)

    total = len(enriched)
    start, end = (page - 1) * limit, (page - 1) * limit + limit
    page_items = enriched[start:end]

    # 7) Build explain lines
    results = []
    for e in page_items:
        it = e["item"]
        why = []
        if filters.get("cause"):
            why.append(f"matches: {', '.join(filters['cause'])}")
        elif intent.get("causes"):
            why.append(f"matches: {', '.join(intent['causes'])}")
        if e["distance_miles"] is not None:
            why.append(f"{e['distance_miles']:.1f} mi away")
        if e["trust"] >= 1.0:
            why.append("verified")
        results.append({
            **it,
            "_scores": {
                "semantic": round(e["semantic"], 3),
                "geo": round(e["geo_score"], 3),
                "final": round(e["final_score"], 3)
            },
            "_explain": " • ".join(why) if why else "relevant to your search"
        })

    return jsonify({
        "success": True,
        "query": q,
        "intent": intent,
        "sort": sort,
        "page": page,
        "limit": limit,
        "total_found": total,
        "results": results
    })

# Optional: GET /search passthrough for convenience
@app.route("/search")
def search_get():
    q = request.args.get("query", request.args.get("q", ""))
    zip_code = request.args.get("zip")
    radius = request.args.get("radius", type=int)
    cause = request.args.getlist("cause")  # ?cause=housing&cause=families
    
    # Call the search logic directly
    sort = (request.args.get("sort") or "relevance").lower()
    page = max(1, int(request.args.get("page") or 1))
    limit = max(1, min(50, int(request.args.get("limit") or 10)))
    top_k = max(limit, int(request.args.get("top_k") or 100))
    explicit_loc = {"zip": zip_code, "radius_miles": radius} if zip_code or radius else {}
    filters = {"cause": cause} if cause else {}

    # 1) Intent parse (merge with explicit payload)
    intent = parse_intent(q)
    loc_zip = explicit_loc.get("zip") or (intent.get("location") or {}).get("zip")
    radius = explicit_loc.get("radius_miles") or (intent.get("location") or {}).get("radius_miles") or 25
    # If causes explicitly passed, keep them; else use NLU
    if "cause" in filters or "causes" in filters:
        pass
    elif intent.get("causes"):
        filters["cause"] = intent["causes"]

    # 2) Semantic retrieval
    vec_hits = vec_search(q or "nonprofit")
    # vec_hits: [{"id": "...", "semantic_score": 0.83}, ...]

    # 3) Geospatial filter + score
    user_latlon = ZIP_TO_LATLON.get(str(loc_zip)) if loc_zip else None

    enriched = []
    for h in vec_hits:
        it = NP_BY_ID[h["id"]]
        # Pre-filter by causes/min_rating
        # (We'll also apply again after candidate selection to be safe)
        semantic = max(0.0, min(1.0, h["semantic_score"]))  # cosine in [0,1]
        # distance
        if user_latlon:
            d_miles = haversine_miles(user_latlon[0], user_latlon[1],
                                      it["location"]["lat"], it["location"]["lon"])
            gscore = geo_score_miles(d_miles, radius)
        else:
            d_miles = None
            gscore = 0.0
        trust = 1.0 if it.get("trust", {}).get("verification_status") else 0.0
        popularity = float(it.get("popularity_90d", 0.0))

        enriched.append({
            "id": it["id"],
            "semantic": semantic,
            "distance_miles": d_miles,
            "geo_score": gscore,
            "trust": trust,
            "popularity": popularity,
            "item": it
        })

    # If user provided a location + radius, keep only within radius
    if user_latlon:
        enriched = [e for e in enriched if e["distance_miles"] is not None and e["distance_miles"] <= radius]

    # 4) Filters (cause, rating…)
    candidate_ids = [e["id"] for e in enriched]
    candidate_ids = _apply_filters(candidate_ids, filters)
    enriched = [e for e in enriched if e["id"] in candidate_ids]

    # 5) Compute final score
    for e in enriched:
        e["final_score"] = final_score(e["semantic"], e["geo_score"], e["trust"], e["popularity"])

    # 6) Sorting
    if sort == "distance" and user_latlon:
        enriched.sort(key=lambda x: (x["distance_miles"] if x["distance_miles"] is not None else 1e9))
    elif sort == "rating":
        enriched.sort(key=lambda x: x["item"]["ratings"]["avg_rating"], reverse=True)
    elif sort == "popularity":
        enriched.sort(key=lambda x: x["popularity"], reverse=True)
    elif sort == "newest":
        enriched.sort(key=lambda x: x["item"]["created_at"], reverse=True)
    elif sort == "impact":
        # simple proxy: invert cost_per_* if exists (lower cost → higher impact)
        def impact_score(it):
            im = it["item"].get("impact_metrics", {})
            for k in ["cost_per_family", "cost_per_session"]:
                if k in im and im[k] > 0:
                    return 1.0 / float(im[k])
            return 0.0
        enriched.sort(key=lambda x: impact_score(x), reverse=True)
    else:
        # relevance
        enriched.sort(key=lambda x: x["final_score"], reverse=True)

    total = len(enriched)
    start, end = (page - 1) * limit, (page - 1) * limit + limit
    page_items = enriched[start:end]

    # 7) Build explain lines
    results = []
    for e in page_items:
        it = e["item"]
        why = []
        if filters.get("cause"):
            why.append(f"matches: {', '.join(filters['cause'])}")
        elif intent.get("causes"):
            why.append(f"matches: {', '.join(intent['causes'])}")
        if e["distance_miles"] is not None:
            why.append(f"{e['distance_miles']:.1f} mi away")
        if e["trust"] >= 1.0:
            why.append("verified")
        results.append({
            **it,
            "_scores": {
                "semantic": round(e["semantic"], 3),
                "geo": round(e["geo_score"], 3),
                "final": round(e["final_score"], 3)
            },
            "_explain": " • ".join(why) if why else "relevant to your search"
        })

    return jsonify({
        "success": True,
        "query": q,
        "intent": intent,
        "sort": sort,
        "page": page,
        "limit": limit,
        "total_found": total,
        "results": results
    })

if __name__ == "__main__":
    load_data()
    build_index(DATA.get("nonprofits", []))
    print(f"Loaded {len(DATA.get('nonprofits', []))} nonprofits; FAISS index ready.")
    app.run(host="0.0.0.0", port=5000, debug=True)
