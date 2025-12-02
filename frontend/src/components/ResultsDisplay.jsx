import ScoreCard from './ScoreCard';
import SuggestionCard from './SuggestionCard';
import MissingKeywordsList from './MissingKeywordsList';

const ResultsDisplay = ({ results }) => {
  if (!results) return null;

  return (
    <div className="space-y-6">
      <div className="bg-gradient-to-r from-primary-600 to-primary-800 text-white rounded-lg shadow-md p-6">
        <h2 className="text-2xl font-bold mb-2">Analysis Results</h2>
        <p className="text-primary-100">
          Your resume has been analyzed against the job description
        </p>
      </div>

      {/* Score Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <ScoreCard
          title="Semantic Similarity Score"
          score={results.similarity_score}
          color="blue"
        />
        <ScoreCard
          title="ATS Compatibility Score"
          score={results.ats_compatibility_score}
          color="green"
        />
      </div>

      {/* Missing Keywords */}
      {results.missing_keywords && results.missing_keywords.length > 0 && (
        <MissingKeywordsList keywords={results.missing_keywords} />
      )}

      {/* Suggestions */}
      {results.suggestions && results.suggestions.length > 0 && (
        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-lg font-semibold text-gray-800 mb-4">
            Optimization Suggestions ({results.suggestions.length})
          </h3>
          <div className="space-y-4">
            {results.suggestions.map((suggestion, index) => (
              <SuggestionCard key={index} suggestion={suggestion} />
            ))}
          </div>
        </div>
      )}

      {/* Empty State */}
      {(!results.suggestions || results.suggestions.length === 0) &&
        (!results.missing_keywords || results.missing_keywords.length === 0) && (
          <div className="bg-green-50 border border-green-200 rounded-lg p-6 text-center">
            <p className="text-green-800 font-semibold">
              🎉 Great! Your resume looks well-aligned with the job description.
            </p>
          </div>
        )}
    </div>
  );
};

export default ResultsDisplay;

