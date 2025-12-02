import { useState } from 'react';
import ResumeUpload from './components/ResumeUpload';
import JobDescriptionInput from './components/JobDescriptionInput';
import ResultsDisplay from './components/ResultsDisplay';
import LoadingSpinner from './components/LoadingSpinner';
import { analyzeResume, analyzeResumeWithFile } from './services/api';

function App() {
  const [resumeData, setResumeData] = useState({ file: null, text: null });
  const [jobDescription, setJobDescription] = useState('');
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleResumeChange = ({ file, text }) => {
    setResumeData({ file, text });
    setResults(null); // Clear previous results
    setError(null);
  };

  const handleJobDescriptionChange = (text) => {
    setJobDescription(text);
    setResults(null); // Clear previous results
    setError(null);
  };

  const validateInputs = () => {
    if (!resumeData.file && !resumeData.text) {
      setError('Please upload a resume file or paste resume text.');
      return false;
    }

    if (!jobDescription || jobDescription.trim().length < 50) {
      setError('Job description must be at least 50 characters long.');
      return false;
    }

    return true;
  };

  const handleAnalyze = async () => {
    if (!validateInputs()) {
      return;
    }

    setLoading(true);
    setError(null);
    setResults(null);

    try {
      let analysisResults;

      if (resumeData.file) {
        // Use file upload endpoint
        analysisResults = await analyzeResumeWithFile(
          resumeData.file,
          jobDescription
        );
      } else {
        // Use text input endpoint
        analysisResults = await analyzeResume(
          resumeData.text,
          jobDescription
        );
      }

      setResults(analysisResults);
    } catch (err) {
      setError(err.message || 'An error occurred while analyzing your resume.');
      console.error('Analysis error:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <h1 className="text-3xl font-bold text-gray-900">
            Resume Optimizer
          </h1>
          <p className="text-gray-600 mt-2">
            Get AI-powered suggestions to optimize your resume for job applications
          </p>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="space-y-6">
          {/* Resume Upload */}
          <ResumeUpload
            onResumeChange={handleResumeChange}
            resumeText={resumeData.text}
            resumeFile={resumeData.file}
          />

          {/* Job Description Input */}
          <JobDescriptionInput
            value={jobDescription}
            onChange={handleJobDescriptionChange}
          />

          {/* Analyze Button */}
          <div className="flex justify-center">
            <button
              onClick={handleAnalyze}
              disabled={loading || (!resumeData.file && !resumeData.text) || !jobDescription}
              className={`px-8 py-3 rounded-lg font-semibold text-lg transition-all ${
                loading || (!resumeData.file && !resumeData.text) || !jobDescription
                  ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
                  : 'bg-primary-600 text-white hover:bg-primary-700 shadow-lg hover:shadow-xl transform hover:scale-105'
              }`}
            >
              {loading ? 'Analyzing...' : 'Analyze Resume'}
            </button>
          </div>

          {/* Error Display */}
          {error && (
            <div className="bg-red-50 border-l-4 border-red-500 p-4 rounded-lg">
              <div className="flex">
                <div className="flex-shrink-0">
                  <svg
                    className="h-5 w-5 text-red-400"
                    viewBox="0 0 20 20"
                    fill="currentColor"
                  >
                    <path
                      fillRule="evenodd"
                      d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
                      clipRule="evenodd"
                    />
                  </svg>
                </div>
                <div className="ml-3">
                  <p className="text-sm text-red-800">{error}</p>
                </div>
              </div>
            </div>
          )}

          {/* Loading State */}
          {loading && <LoadingSpinner />}

          {/* Results Display */}
          {results && !loading && <ResultsDisplay results={results} />}
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-white border-t border-gray-200 mt-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <p className="text-center text-gray-500 text-sm">
            Resume Optimization System - Powered by Sentence-BERT
          </p>
        </div>
      </footer>
    </div>
  );
}

export default App;
