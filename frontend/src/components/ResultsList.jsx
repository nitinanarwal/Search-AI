import BusinessCard from "./BusinessCard";

function ResultsList({ results }) {
  console.log('ResultsList received:', results);
  
  if (!results || results.length === 0) {
    return <p className="text-gray-500">No results found. Try another search.</p>;
  }

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 w-full max-w-6xl">
      {results.map((item, index) => (
        <BusinessCard key={index} business={item} />
      ))}
    </div>
  );
}

export default ResultsList;
