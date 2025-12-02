import { useState } from 'react';

const ResumeUpload = ({ onResumeChange, resumeText, resumeFile }) => {
  const [inputMode, setInputMode] = useState('text'); // 'text' or 'file'
  const [dragActive, setDragActive] = useState(false);

  const handleFileChange = (file) => {
    if (file && file.type === 'application/pdf') {
      onResumeChange({ file, text: null });
    } else {
      alert('Please upload a PDF file only.');
    }
  };

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFileChange(e.dataTransfer.files[0]);
    }
  };

  const handleTextChange = (text) => {
    onResumeChange({ file: null, text });
  };

  const clearResume = () => {
    onResumeChange({ file: null, text: null });
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-xl font-semibold text-gray-800">
          Step 1: Upload Your Resume
        </h2>
        <div className="flex space-x-2">
          <button
            onClick={() => setInputMode('text')}
            className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
              inputMode === 'text'
                ? 'bg-primary-600 text-white'
                : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
            }`}
          >
            Paste Text
          </button>
          <button
            onClick={() => setInputMode('file')}
            className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
              inputMode === 'file'
                ? 'bg-primary-600 text-white'
                : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
            }`}
          >
            Upload PDF
          </button>
        </div>
      </div>

      {inputMode === 'file' ? (
        <div
          className={`border-2 border-dashed rounded-lg p-8 text-center transition-colors ${
            dragActive
              ? 'border-primary-500 bg-primary-50'
              : 'border-gray-300 bg-gray-50'
          }`}
          onDragEnter={handleDrag}
          onDragLeave={handleDrag}
          onDragOver={handleDrag}
          onDrop={handleDrop}
        >
          <input
            type="file"
            accept=".pdf"
            onChange={(e) => handleFileChange(e.target.files[0])}
            className="hidden"
            id="file-upload"
          />
          <label
            htmlFor="file-upload"
            className="cursor-pointer flex flex-col items-center"
          >
            <svg
              className="w-12 h-12 text-gray-400 mb-4"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"
              />
            </svg>
            <p className="text-gray-600 mb-2">
              <span className="text-primary-600 font-semibold">Click to upload</span> or drag and drop
            </p>
            <p className="text-sm text-gray-500">PDF files only</p>
          </label>
          {resumeFile && (
            <div className="mt-4 p-3 bg-green-50 border border-green-200 rounded-lg">
              <p className="text-sm text-green-800">
                ✓ {resumeFile.name}
              </p>
            </div>
          )}
        </div>
      ) : (
        <div className="space-y-4">
          <textarea
            value={resumeText || ''}
            onChange={(e) => handleTextChange(e.target.value)}
            placeholder="Paste your resume text here...&#10;&#10;Example:&#10;John Doe&#10;Software Engineer&#10;5 years of experience developing web applications..."
            className="w-full h-64 p-4 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent resize-y"
          />
          {resumeText && (
            <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
              <p className="text-sm text-gray-600">
                {resumeText.split('\n').length} lines, {resumeText.length} characters
              </p>
              <button
                onClick={clearResume}
                className="text-sm text-red-600 hover:text-red-800 font-medium"
              >
                Clear
              </button>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default ResumeUpload;

