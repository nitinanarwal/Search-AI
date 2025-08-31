import numpy as np
from sentence_transformers import SentenceTransformer
import faiss

# Global (simple for demo)
_model = None
_index = None
_ids = None

def _get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")  # 384-dim
    return _model

def _normalize(vecs: np.ndarray) -> np.ndarray:
    # cosine similarity via inner product on normalized vectors
    norms = np.linalg.norm(vecs, axis=1, keepdims=True) + 1e-12
    return vecs / norms

def build_index(items, text_fields=("name", "mission_text", "description")):
    """
    items: list of dicts (nonprofits)
    returns: None (populates globals)
    """
    global _index, _ids
    model = _get_model()
    corpora = []
    _ids = []
    for it in items:
        # simple concat of fields to embed
        text = " ".join([str(it.get(f, "")) for f in text_fields])
        corpora.append(text)
        _ids.append(it["id"])

    embeddings = model.encode(corpora, batch_size=32, show_progress_bar=False)
    embeddings = _normalize(np.array(embeddings).astype("float32"))

    dim = embeddings.shape[1]
    _index = faiss.IndexFlatIP(dim)  # inner product on normalized = cosine
    _index.add(embeddings)

def search(query_text: str, top_k: int = 50):
    global _index, _ids
    if _index is None:
        raise RuntimeError("Index not built. Call build_index() first.")
    model = _get_model()
    q_emb = model.encode([query_text])
    q_emb = _normalize(np.array(q_emb).astype("float32"))

    D, I = _index.search(q_emb, top_k)  # D: scores, I: indices
    hits = []
    for score, idx in zip(D[0], I[0]):
        if idx == -1:
            continue
        hits.append({"id": _ids[idx], "semantic_score": float(score)})
    return hits
