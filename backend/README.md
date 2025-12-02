# Resume Optimization Backend API

FastAPI backend service for analyzing resumes and providing optimization suggestions based on job descriptions.

## Features

- Resume analysis via text input or PDF upload
- Semantic similarity scoring using Sentence-BERT
- ATS compatibility scoring
- Missing keyword detection
- Optimization suggestions

## Setup

1. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Download NLTK data (if using NLTK):**
   ```bash
   python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
   ```

4. **Run the server:**
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```

   Or using Python directly:
   ```bash
   python -m app.main
   ```

## API Endpoints

### Health Check
- **GET** `/health` - Check if API is running

### Analyze Resume
- **POST** `/analyze` - Analyze resume (supports form-data with file upload)
  - Parameters:
    - `job_description` (required): Job description text
    - `resume_text` (optional): Resume text
    - `resume_file` (optional): PDF file upload
  
- **POST** `/analyze/json` - Analyze resume (JSON format)
  - Body: `AnalysisRequest` JSON
    ```json
    {
      "resume_text": "Your resume text here...",
      "job_description": "Job description here..."
    }
    ```

## Response Format

```json
{
  "similarity_score": 75.5,
  "ats_compatibility_score": 68.2,
  "missing_keywords": ["Python", "AWS"],
  "suggestions": [
    {
      "category": "missing_skill",
      "title": "Add Python Experience",
      "description": "The job requires Python...",
      "priority": "high"
    }
  ]
}
```

## Development

The Sentence-BERT model will be automatically downloaded on first use (approximately 90MB).

## Testing

Test the API using curl:

```bash
curl -X POST "http://localhost:8000/analyze/json" \
  -H "Content-Type: application/json" \
  -d '{
    "resume_text": "Your resume text...",
    "job_description": "Job description..."
  }'
```

