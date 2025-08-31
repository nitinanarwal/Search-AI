function BusinessCard({ business }) {
  // Defensive check for business object
  if (!business || typeof business !== 'object') {
    return (
      <div className="bg-white shadow-md rounded-xl p-6 hover:shadow-lg transition">
        <p className="text-red-500">Invalid business data</p>
      </div>
    );
  }

  return (
    <div className="bg-white shadow-md rounded-xl p-6 hover:shadow-lg transition">
      <h2 className="text-xl font-semibold text-blue-600">
        {business.name || "Unnamed Business"}
      </h2>
      <p className="text-gray-700 mt-2">
        {business.category || "No category"}
      </p>
      <p className="text-gray-500 mt-1 text-sm">
        {business.description || "No description available"}
      </p>
      <p className="text-gray-600 mt-2 font-medium">
        📍 {business.location || "Location not available"}
      </p>
    </div>
  );
}

export default BusinessCard;
