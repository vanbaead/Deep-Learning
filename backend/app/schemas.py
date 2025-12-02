"""
Pydantic schemas for API request/response models.
"""
from pydantic import BaseModel, Field
from typing import List, Optional


class AnalysisRequest(BaseModel):
    """Request schema for resume analysis."""
    resume_text: Optional[str] = Field(None, description="Resume content as plain text")
    job_description: str = Field(..., description="Job description to match against")
    
    class Config:
        schema_extra = {
            "example": {
                "resume_text": "John Doe\nSoftware Engineer\n5 years experience...",
                "job_description": "We are looking for a software engineer with experience in Python..."
            }
        }


class Suggestion(BaseModel):
    """Individual optimization suggestion."""
    category: str = Field(..., description="Category: 'missing_skill', 'phrasing', or 'keyword'")
    title: str = Field(..., description="Suggestion title/header")
    description: str = Field(..., description="Detailed suggestion description")
    priority: str = Field(..., description="Priority level: 'high', 'medium', or 'low'")
    
    class Config:
        schema_extra = {
            "example": {
                "category": "missing_skill",
                "title": "Add Python Experience",
                "description": "The job requires Python, but your resume doesn't mention it.",
                "priority": "high"
            }
        }


class AnalysisResponse(BaseModel):
    """Response schema for resume analysis results."""
    similarity_score: float = Field(..., ge=0, le=100, description="Semantic similarity score (0-100)")
    ats_compatibility_score: float = Field(..., ge=0, le=100, description="ATS compatibility score (0-100)")
    missing_keywords: List[str] = Field(default_factory=list, description="List of missing keywords/skills")
    suggestions: List[Suggestion] = Field(default_factory=list, description="List of optimization suggestions")
    
    class Config:
        schema_extra = {
            "example": {
                "similarity_score": 75.5,
                "ats_compatibility_score": 68.2,
                "missing_keywords": ["Python", "AWS", "Docker"],
                "suggestions": [
                    {
                        "category": "missing_skill",
                        "title": "Add Python Experience",
                        "description": "The job requires Python, but your resume doesn't mention it.",
                        "priority": "high"
                    }
                ]
            }
        }

