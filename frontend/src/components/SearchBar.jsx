import { useState } from "react";

function SearchBar({ onSearch }) {
  const [query, setQuery] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    onSearch(query);
  };

  return (
    <form
      onSubmit={handleSubmit}
      className="flex w-full max-w-xl mb-8 shadow-lg rounded-lg overflow-hidden"
    >
      <input
        type="text"
        placeholder="Search businesses..."
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        className="flex-grow px-4 py-2 outline-none text-gray-700"
      />
      <button
        type="submit"
        className="bg-blue-600 text-white px-6 py-2 hover:bg-blue-700 transition"
      >
        Search
      </button>
    </form>
  );
}

export default SearchBar;
