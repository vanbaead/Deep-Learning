# Resume Optimization System

An AI-powered resume optimization tool that analyzes resumes against job descriptions using semantic similarity (Sentence-BERT) and provides actionable optimization suggestions. This system helps job seekers improve their resume's alignment with job postings and increase their chances of passing through Applicant Tracking Systems (ATS).

## 🎯 Problem Statement

Job seekers often struggle to tailor their resumes to specific job postings. Generic resumes lack alignment with job descriptions, resulting in lower chances of passing through Applicant Tracking Systems (ATS) and recruiter screenings. Manual tailoring is time-consuming, error-prone, and requires deep knowledge of keywords and phrasing that match employer expectations.

This system automatically analyzes a user's resume and provides optimized suggestions aligned with a given job description.

## ✨ Features

- **Resume Analysis**: Upload PDF resumes or paste text directly
- **Semantic Similarity Scoring**: Uses Sentence-BERT to measure semantic alignment between resume and job description
- **ATS Compatibility Score**: Comprehensive scoring system combining keyword matching, semantic similarity, and section completeness
- **Missing Keywords Detection**: Identifies important skills and keywords missing from your resume
- **Actionable Suggestions**: Provides prioritized optimization recommendations
- **Modern Web Interface**: Clean, responsive UI built with React and Tailwind CSS

## 🏗️ Architecture

### Tech Stack

**Backend:**
- FastAPI - Modern Python web framework
- Sentence-BERT (`all-MiniLM-L6-v2`) - Semantic similarity model
- PyPDF2 - PDF text extraction
- scikit-learn - Cosine similarity calculations

**Frontend:**
- React 19 - UI framework
- Vite - Build tool and dev server
- Tailwind CSS - Utility-first CSS framework
- Axios - HTTP client

### Project Structure

```
Deep Learning/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI application
│   │   ├── models/
│   │   │   ├── similarity.py    # Sentence-BERT similarity scoring
│   │   │   └── optimizer.py     # Resume optimization logic
│   │   ├── utils/
│   │   │   ├── text_processing.py  # NLP preprocessing
│   │   │   └── pdf_parser.py       # PDF extraction
│   │   └── schemas.py           # Pydantic models
│   ├── requirements.txt
│   └── venv/                    # Virtual environment
├── frontend/
│   ├── src/
│   │   ├── components/          # React components
│   │   ├── services/
│   │   │   └── api.js          # API client
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
├── data/
│   ├── sample_resumes/         # Sample resume files
│   └── sample_jobs/            # Sample job descriptions
└── README.md                   # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.12+ 
- Node.js 18+ and npm
- Virtual environment (Python venv)

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create and activate virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the server:**
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```

   The API will be available at `http://localhost:8000`

   **Note:** The Sentence-BERT model will be automatically downloaded on first use (~90MB).

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start the development server:**
   ```bash
   npm run dev
   ```

   The frontend will be available at `http://localhost:5173`

### Using the Application

1. **Start both servers:**
   - Backend: `http://localhost:8000`
   - Frontend: `http://localhost:5173`

2. **Open the frontend URL** in your browser

3. **Upload or paste your resume:**
   - Option 1: Upload a PDF file
   - Option 2: Paste resume text directly

4. **Enter the job description** in the text area

5. **Click "Analyze Resume"** to get optimization suggestions

## 📡 API Documentation

### Endpoints

#### Health Check
```
GET /health
```
Returns API health status.

#### Analyze Resume (JSON)
```
POST /analyze/json
Content-Type: application/json

{
  "resume_text": "Your resume text...",
  "job_description": "Job description text..."
}
```

#### Analyze Resume (File Upload)
```
POST /analyze
Content-Type: multipart/form-data

- job_description: (string, required) Job description text
- resume_text: (string, optional) Resume text
- resume_file: (file, optional) PDF file
```

### Response Format

```json
{
  "similarity_score": 75.5,
  "ats_compatibility_score": 68.2,
  "missing_keywords": ["Python", "AWS", "Docker"],
  "suggestions": [
    {
      "category": "missing_skill",
      "title": "Add Python Experience",
      "description": "The job description mentions Python...",
      "priority": "high"
    }
  ]
}
```

### Interactive API Docs

Once the backend is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 🧪 Testing

### Test Backend API

Using curl:
```bash
curl -X POST "http://localhost:8000/analyze/json" \
  -H "Content-Type: application/json" \
  -d '{
    "resume_text": "John Doe\nSoftware Engineer\n5 years of experience developing web applications using Python and JavaScript.",
    "job_description": "We are seeking a Senior Software Engineer with experience in Python, JavaScript, and cloud platforms."
  }'
```

### Test Frontend

1. Ensure backend is running on port 8000
2. Start frontend with `npm run dev`
3. Navigate to `http://localhost:5173`
4. Test the full workflow with sample data

## 🔧 How It Works

### 1. Text Processing
- Resume and job description text are cleaned and preprocessed
- PDF files are extracted to plain text

### 2. Semantic Similarity
- Sentence-BERT generates embeddings for both texts
- Cosine similarity is calculated to measure semantic alignment
- Score is scaled to 0-100

### 3. Keyword Extraction
- Technical skills and keywords are extracted from job description
- Curated skill database ensures accurate matching
- Stop words and common phrases are filtered out

### 4. Optimization Suggestions
- Missing skills are identified by comparing job requirements with resume
- Suggestions are prioritized (high/medium/low)
- Categorized by type: missing skills, phrasing improvements, keyword additions

### 5. ATS Compatibility Score
Weighted combination of:
- **30%** Keyword match percentage
- **40%** Semantic similarity score
- **30%** Section completeness (experience, education, skills)

## 📊 Scoring System

- **Similarity Score (0-100)**: Measures semantic alignment between resume and job description
- **ATS Compatibility Score (0-100)**: Overall compatibility considering multiple factors
- **Missing Keywords**: List of important skills/tools not mentioned in resume
- **Suggestions**: Prioritized recommendations for improvement

## 🎨 Features in Detail

### Resume Upload
- Drag-and-drop PDF upload
- Text paste option
- File validation
- Resume preview

### Job Description Input
- Large text area for job descriptions
- Character counter
- Input validation

### Results Display
- Visual score cards with circular progress indicators
- Color-coded scores (green/yellow/red)
- Missing keywords as tags
- Detailed suggestion cards with priorities

## 🔮 Future Improvements

- [ ] Resume section extraction (Experience, Education, Skills)
- [ ] Industry-specific keyword databases
- [ ] Resume rewriting suggestions with AI
- [ ] Batch processing for multiple job descriptions
- [ ] Export optimized resume suggestions
- [ ] Historical analysis tracking
- [ ] User accounts and saved resumes
- [ ] More advanced NLP for phrasing suggestions

## 🐛 Troubleshooting

### Backend Issues

**Port already in use:**
```bash
# Change port in backend/app/main.py or use:
uvicorn app.main:app --reload --port 8001
```

**Import errors:**
- Ensure virtual environment is activated
- Verify all dependencies are installed: `pip install -r requirements.txt`

**Model download issues:**
- Check internet connection (model downloads on first use)
- Model is cached in `~/.cache/huggingface/`

### Frontend Issues

**API connection errors:**
- Verify backend is running on `http://localhost:8000`
- Check CORS settings in backend (should allow `http://localhost:5173`)
- Check browser console for detailed error messages

**Build errors:**
- Clear node_modules and reinstall: `rm -rf node_modules && npm install`
- Check Node.js version (requires 18+)

## 📝 Development

### Backend Development

```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload
```

### Frontend Development

```bash
cd frontend
npm run dev
```

### Project Structure Details

- **Backend Models**: ML logic for similarity and optimization
- **Backend Utils**: Text processing and PDF parsing utilities
- **Frontend Components**: Reusable React components
- **Frontend Services**: API client functions

## 📄 License

This project is for educational purposes.

## 👥 Authors

Resume Optimization System - ML Project
Adam Vanbaelinghem

## 🙏 Acknowledgments

- Sentence-BERT models by UKP Lab
- FastAPI for the excellent Python framework
- React and Vite communities

---

**Note:** This is a demo/prototype system. For production use, consider additional features like authentication, data persistence, and enhanced error handling.