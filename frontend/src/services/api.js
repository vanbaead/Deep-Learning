import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

/**
 * Analyze resume with text input (JSON endpoint)
 * @param {string} resumeText - Resume text content
 * @param {string} jobDescription - Job description text
 * @returns {Promise} Analysis results
 */
export const analyzeResume = async (resumeText, jobDescription) => {
  try {
    const response = await api.post('/analyze/json', {
      resume_text: resumeText,
      job_description: jobDescription,
    });
    return response.data;
  } catch (error) {
    if (error.response) {
      throw new Error(error.response.data.detail || 'API request failed');
    } else if (error.request) {
      throw new Error('Network error: Could not reach the server');
    } else {
      throw new Error(error.message || 'An unexpected error occurred');
    }
  }
};

/**
 * Analyze resume with PDF file upload
 * @param {File} resumeFile - PDF file object
 * @param {string} jobDescription - Job description text
 * @returns {Promise} Analysis results
 */
export const analyzeResumeWithFile = async (resumeFile, jobDescription) => {
  try {
    const formData = new FormData();
    formData.append('resume_file', resumeFile);
    formData.append('job_description', jobDescription);

    const response = await api.post('/analyze', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  } catch (error) {
    if (error.response) {
      throw new Error(error.response.data.detail || 'API request failed');
    } else if (error.request) {
      throw new Error('Network error: Could not reach the server');
    } else {
      throw new Error(error.message || 'An unexpected error occurred');
    }
  }
};

/**
 * Check if backend API is running
 * @returns {Promise} Health status
 */
export const checkHealth = async () => {
  try {
    const response = await api.get('/health');
    return response.data;
  } catch (error) {
    throw new Error('Backend API is not available');
  }
};

export default api;

