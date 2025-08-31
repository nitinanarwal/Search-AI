// frontend/src/App.jsx
import React, { useState } from "react";
import "./index.css"; // ensure Tailwind CSS is loaded

const API_BASE = import.meta.env.VITE_API_URL || "http://localhost:5000";

export default function App() {
  const [q, setQ] = useState("");
  const [zip, setZip] = useState("");
  const [radius, setRadius] = useState(10);
  const [selectedCauses, setSelectedCauses] = useState([]);
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const KNOWN_CAUSES = ["housing","families","anti-homelessness","mental health","veterans","education","youth","legal"];

  function toggleCause(c) {
    setSelectedCauses(prev => prev.includes(c) ? prev.filter(x => x !== c) : [...prev, c]);
  }

  async function doSearch(page = 1) {
    setLoading(true);
    setError(null);
    try {
      const payload = {
        query: q,
        location: (zip || radius) ? { zip, radius_miles: Number(radius) } : null,
        filters: selectedCauses.length ? { cause: selectedCauses } : null,
        sort: "relevance",
        page,
        limit: 12
      };

      const resp = await fetch(`${API_BASE}/api/search`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });

      if (!resp.ok) {
        const txt = await resp.text();
        throw new Error(`${resp.status} ${resp.statusText}: ${txt}`);
      }

      const data = await resp.json();
      setResults(data.results || []);
    } catch (err) {
      console.error(err);
      setError("Search failed. Check backend and console.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-5xl mx-auto">
        <h1 className="text-3xl font-bold mb-4">What causes would you like to support?</h1>

        {/* Search bar */}
        <div className="flex flex-col md:flex-row gap-2 mb-4">
          <input
            value={q}
            onChange={(e) => setQ(e.target.value)}
            placeholder="e.g., affordable housing near 94103 for families"
            className="flex-1 border rounded-xl p-3"
          />
          <select id="sort" className="border rounded-xl p-3 hidden md:block">
            <option value="relevance">Relevance</option>
            <option value="distance">Distance</option>
            <option value="impact">Impact Score</option>
            <option value="popularity">Popularity</option>
            <option value="newest">Newest</option>
            <option value="rating">Rating</option>
          </select>
          <button
            onClick={() => doSearch(1)}
            className="px-4 py-3 rounded-xl bg-black text-white"
          >
            Search
          </button>
        </div>

        {/* Filters */}
        <div className="grid md:grid-cols-4 gap-3 mb-6">
          <div className="col-span-2 flex items-center gap-2">
            <label className="text-sm text-gray-700">ZIP</label>
            <input value={zip} onChange={e => setZip(e.target.value)} className="border rounded-xl p-2 w-28" placeholder="94103" />
            <label className="text-sm text-gray-700">Radius (mi)</label>
            <input value={radius} onChange={e => setRadius(e.target.value)} type="number" className="border rounded-xl p-2 w-24" />
          </div>

          <div className="col-span-2">
            <div className="text-sm text-gray-700 mb-1">Causes</div>
            <div className="flex flex-wrap gap-2">
              {KNOWN_CAUSES.map(c => {
                const active = selectedCauses.includes(c);
                return (
                  <button
                    key={c}
                    onClick={() => toggleCause(c)}
                    className={`px-3 py-1 rounded-full text-sm font-medium ${active ? "bg-black text-white" : "bg-white text-gray-700 border"}`}
                  >
                    {c}
                  </button>
                );
              })}
            </div>
          </div>
        </div>

        {/* Results / Info */}
        <div>
          {loading && <div className="text-sm text-gray-500 mb-3">Loading...</div>}
          {error && <div className="text-sm text-red-500 mb-3">{error}</div>}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {results.length === 0 && !loading && (
              <div className="col-span-full text-gray-500">No results — try widening radius or different keywords.</div>
            )}

            {results.map(r => (
              <div key={r.id || r.ein || r.name} className="bg-white rounded-2xl shadow-lg p-6 border">
                <div className="flex items-start justify-between mb-3">
                  <h2 className="text-lg font-semibold text-gray-900">{r.name}</h2>
                  <div className="flex items-center gap-1">
                    <span className="text-yellow-500">★</span>
                    <span className="text-sm font-medium">{r.ratings?.avg_rating ?? "-"}</span>
                  </div>
                </div>

                <p className="text-gray-600 text-sm mb-3 line-clamp-3">{r.mission_text || r.description}</p>

                <div className="flex items-center gap-2 text-sm text-gray-500 mb-3">
                  <span>📍 {r.location?.city ?? r.location}</span>
                  {r._explain ? <span>• {r._explain}</span> : null}
                </div>

                <div className="flex flex-wrap gap-2 mb-4">
                  {(r.causes || []).map(c => <span key={c} className="px-3 py-1 text-xs rounded-full bg-blue-100 text-blue-700">{c}</span>)}
                </div>

                <div className="flex gap-2 mb-3">
                  {r.trust?.verification_status ? <span className="px-2 py-1 text-xs rounded-full bg-green-100 text-green-700">✓ Verified</span> : null}
                  {r._scores?.final ? <span className="px-2 py-1 text-xs rounded-full bg-purple-100 text-purple-700">Impact: {r._scores.final.toFixed(2)}</span> : null}
                </div>

                <div className="flex gap-2">
                  <button className="flex-1 px-4 py-2 rounded-xl bg-blue-600 text-white text-sm">Donate</button>
                  <button className="px-4 py-2 rounded-xl border border-gray-300 text-sm">Bookmark</button>
                </div>
              </div>
            ))}

          </div>
        </div>
      </div>
    </div>
  );
}
