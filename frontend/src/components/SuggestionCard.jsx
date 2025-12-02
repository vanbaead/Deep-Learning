const SuggestionCard = ({ suggestion }) => {
  const getPriorityColor = (priority) => {
    const colors = {
      high: 'bg-red-100 text-red-800 border-red-300',
      medium: 'bg-yellow-100 text-yellow-800 border-yellow-300',
      low: 'bg-blue-100 text-blue-800 border-blue-300',
    };
    return colors[priority] || colors.medium;
  };

  const getCategoryIcon = (category) => {
    const icons = {
      missing_skill: '🔧',
      phrasing: '✏️',
      keyword: '🔑',
    };
    return icons[category] || '💡';
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-5 border border-gray-200 hover:shadow-lg transition-shadow">
      <div className="flex items-start justify-between mb-3">
        <div className="flex items-center space-x-2">
          <span className="text-2xl">{getCategoryIcon(suggestion.category)}</span>
          <h4 className="text-lg font-semibold text-gray-800">
            {suggestion.title}
          </h4>
        </div>
        <span
          className={`px-3 py-1 text-xs font-semibold rounded-full border ${getPriorityColor(
            suggestion.priority
          )}`}
        >
          {suggestion.priority.toUpperCase()}
        </span>
      </div>
      <p className="text-gray-600 text-sm leading-relaxed">
        {suggestion.description}
      </p>
    </div>
  );
};

export default SuggestionCard;

