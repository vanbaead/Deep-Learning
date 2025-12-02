import { useState } from 'react';

const JobDescriptionInput = ({ value, onChange }) => {
  const [charCount, setCharCount] = useState(0);

  const handleChange = (e) => {
    const text = e.target.value;
    setCharCount(text.length);
    onChange(text);
  };

  const clearInput = () => {
    onChange('');
    setCharCount(0);
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-xl font-semibold text-gray-800">
          Step 2: Enter Job Description
        </h2>
        {value && (
          <button
            onClick={clearInput}
            className="text-sm text-red-600 hover:text-red-800 font-medium"
          >
            Clear
          </button>
        )}
      </div>
      <textarea
        value={value || ''}
        onChange={handleChange}
        placeholder="Paste the job description here...&#10;&#10;Example:&#10;We are seeking a Senior Software Engineer with extensive experience in Python, JavaScript, and cloud platforms. The ideal candidate should have 5+ years of experience..."
        className="w-full h-64 p-4 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent resize-y"
      />
      <div className="mt-3 flex items-center justify-between">
        <p className="text-sm text-gray-500">
          {charCount === 0 ? 'Enter job description' : `${charCount} characters`}
        </p>
        {charCount < 50 && charCount > 0 && (
          <p className="text-sm text-yellow-600">
            Job description seems too short (minimum 50 characters)
          </p>
        )}
      </div>
    </div>
  );
};

export default JobDescriptionInput;

