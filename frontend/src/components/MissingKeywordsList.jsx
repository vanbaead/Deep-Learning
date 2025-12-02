const MissingKeywordsList = ({ keywords }) => {
  if (!keywords || keywords.length === 0) {
    return null;
  }

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h3 className="text-lg font-semibold text-gray-800 mb-4">
        Missing Keywords ({keywords.length})
      </h3>
      <div className="flex flex-wrap gap-2">
        {keywords.map((keyword, index) => (
          <span
            key={index}
            className="px-4 py-2 bg-red-100 text-red-800 rounded-full text-sm font-medium border border-red-300"
          >
            {keyword}
          </span>
        ))}
      </div>
    </div>
  );
};

export default MissingKeywordsList;

