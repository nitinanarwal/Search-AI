import { useState } from "react";
import SearchBar from "./components/SearchBar";
import ResultsList from "./components/ResultsList";

function App() {
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSearch = async (query) => {
    if (!query) return;

    setLoading(true);
    setError("");
    setResults([]);

    try {
      const response = await fetch(
        `${import.meta.env.VITE_API_URL}/search?query=${encodeURIComponent(query)}`
      );

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: Failed to fetch results. Please try again.`);
      }

      const data = await response.json();
      console.log('API Response:', data);
      
      if (data.success === false) {
        throw new Error(data.message || "Search failed");
      }
      
      setResults(data.results || data);
    } catch (err) {
      console.error('Search error:', err);
      setError(err.message || "Something went wrong.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col items-center p-6">
      <h1 className="text-3xl font-bold text-blue-600 mb-6">
        Business Search App
      </h1>

      <SearchBar onSearch={handleSearch} />

      {loading && (
        <p className="text-blue-600 font-medium animate-pulse">Loading...</p>
      )}

      {error && (
        <p className="text-red-500 font-medium mt-4">{error}</p>
      )}

      {!loading && !error && <ResultsList results={results} />}
    </div>
  );
}

export default App;
