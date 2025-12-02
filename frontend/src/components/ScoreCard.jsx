const ScoreCard = ({ title, score, color = 'blue' }) => {
  const getColorClasses = (color) => {
    const colors = {
      blue: 'bg-blue-500',
      green: 'bg-green-500',
      yellow: 'bg-yellow-500',
      orange: 'bg-orange-500',
      red: 'bg-red-500',
    };
    return colors[color] || colors.blue;
  };

  const getScoreColor = (score) => {
    if (score >= 80) return 'green';
    if (score >= 60) return 'yellow';
    if (score >= 40) return 'orange';
    return 'red';
  };

  const scoreColor = getScoreColor(score);

  return (
    <div className="bg-white rounded-lg shadow-md p-6 border-l-4 border-primary-500">
      <h3 className="text-lg font-semibold text-gray-800 mb-2">{title}</h3>
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-4">
          <div className="relative w-24 h-24">
            <svg className="transform -rotate-90 w-24 h-24">
              <circle
                cx="48"
                cy="48"
                r="40"
                stroke="#e5e7eb"
                strokeWidth="8"
                fill="none"
              />
              <circle
                cx="48"
                cy="48"
                r="40"
                stroke={
                  scoreColor === 'green'
                    ? '#10b981'
                    : scoreColor === 'yellow'
                    ? '#f59e0b'
                    : scoreColor === 'orange'
                    ? '#f97316'
                    : '#ef4444'
                }
                strokeWidth="8"
                fill="none"
                strokeDasharray={`${2 * Math.PI * 40}`}
                strokeDashoffset={`${2 * Math.PI * 40 * (1 - score / 100)}`}
                className="transition-all duration-500"
              />
            </svg>
            <div className="absolute inset-0 flex items-center justify-center">
              <span className="text-2xl font-bold text-gray-800">{Math.round(score)}</span>
            </div>
          </div>
          <div>
            <p className="text-3xl font-bold text-gray-900">{Math.round(score)}%</p>
            <p className="text-sm text-gray-500">out of 100</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ScoreCard;

