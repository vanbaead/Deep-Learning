"""
FastAPI application for resume optimization system.
"""
from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import uvicorn

from app.schemas import AnalysisRequest, AnalysisResponse
from app.utils.pdf_parser import extract_text_from_pdf
from app.utils.text_processing import clean_text
from app.models.similarity import compute_similarity_score
from app.models.optimizer import generate_optimization_suggestions, calculate_ats_score

app = FastAPI(
    title="Resume Optimization API",
    description="API for analyzing resumes and providing optimization suggestions based on job descriptions",
    version="1.0.0"
)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # Vite default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "message": "Resume Optimization API is running"}


@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_resume(
    job_description: str = Form(..., description="Job description text"),
    resume_text: Optional[str] = Form(None, description="Resume text (if not uploading file)"),
    resume_file: Optional[UploadFile] = File(None, description="Resume PDF file (optional)")
):
    """
    Analyze a resume against a job description and provide optimization suggestions.
    
    Accepts either:
    - Plain text resume via `resume_text` parameter
    - PDF file via `resume_file` parameter
    
    Returns similarity scores, missing keywords, and optimization suggestions.
    """
    try:
        # Extract resume text from file or use provided text
        if resume_file and resume_file.filename:
            if not resume_file.filename.endswith('.pdf'):
                raise HTTPException(
                    status_code=400,
                    detail="Only PDF files are supported for file uploads"
                )
            resume_content = await extract_text_from_pdf(resume_file)
        elif resume_text:
            resume_content = resume_text
        else:
            raise HTTPException(
                status_code=400,
                detail="Either resume_text or resume_file must be provided"
            )
        
        if not resume_content or len(resume_content.strip()) < 50:
            raise HTTPException(
                status_code=400,
                detail="Resume content is too short or empty"
            )
        
        if not job_description or len(job_description.strip()) < 50:
            raise HTTPException(
                status_code=400,
                detail="Job description is too short or empty"
            )
        
        # Clean and preprocess text
        cleaned_resume = clean_text(resume_content)
        cleaned_job_desc = clean_text(job_description)
        
        # Compute similarity score
        similarity_score = compute_similarity_score(cleaned_resume, cleaned_job_desc)
        
        # Generate optimization suggestions
        suggestions, missing_keywords = generate_optimization_suggestions(
            cleaned_resume, cleaned_job_desc
        )
        
        # Calculate ATS compatibility score
        ats_score = calculate_ats_score(
            cleaned_resume, cleaned_job_desc, similarity_score, missing_keywords
        )
        
        return AnalysisResponse(
            similarity_score=round(similarity_score, 2),
            ats_compatibility_score=round(ats_score, 2),
            missing_keywords=missing_keywords,
            suggestions=suggestions
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing request: {str(e)}"
        )


@app.post("/analyze/json", response_model=AnalysisResponse)
async def analyze_resume_json(request: AnalysisRequest):
    """
    Alternative JSON endpoint for resume analysis (without file upload).
    
    Useful for testing and when resume is already in text format.
    """
    if not request.resume_text:
        raise HTTPException(
            status_code=400,
            detail="resume_text is required for JSON endpoint"
        )
    
    try:
        # Validate inputs
        if len(request.resume_text.strip()) < 50:
            raise HTTPException(
                status_code=400,
                detail="Resume content is too short or empty"
            )
        
        if len(request.job_description.strip()) < 50:
            raise HTTPException(
                status_code=400,
                detail="Job description is too short or empty"
            )
        
        # Clean and preprocess text
        cleaned_resume = clean_text(request.resume_text)
        cleaned_job_desc = clean_text(request.job_description)
        
        # Compute similarity score
        similarity_score = compute_similarity_score(cleaned_resume, cleaned_job_desc)
        
        # Generate optimization suggestions
        suggestions, missing_keywords = generate_optimization_suggestions(
            cleaned_resume, cleaned_job_desc
        )
        
        # Calculate ATS compatibility score
        ats_score = calculate_ats_score(
            cleaned_resume, cleaned_job_desc, similarity_score, missing_keywords
        )
        
        return AnalysisResponse(
            similarity_score=round(similarity_score, 2),
            ats_compatibility_score=round(ats_score, 2),
            missing_keywords=missing_keywords,
            suggestions=suggestions
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing request: {str(e)}"
        )


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

