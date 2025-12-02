"""
Resume optimization logic - suggestions and ATS scoring.
"""
from typing import List, Tuple
from app.schemas import Suggestion
import re


def extract_skills_from_text(text: str) -> List[str]:
    """
    Extract potential skills/keywords from text.
    
    Args:
        text: Input text
        
    Returns:
        List of extracted skills/keywords
    """
    # Common technical skills patterns
    skill_patterns = [
        r'\b(python|java|javascript|react|node\.js|aws|docker|kubernetes|sql|git)\b',
        r'\b(machine learning|data science|web development|software engineering)\b',
        r'\b([A-Z]{2,})\b',  # Acronyms (AWS, API, etc.)
    ]
    
    skills = set()
    text_lower = text.lower()
    
    for pattern in skill_patterns:
        matches = re.findall(pattern, text_lower, re.IGNORECASE)
        if isinstance(matches[0], tuple) if matches else False:
            skills.update([m[0] if isinstance(m, tuple) else m for m in matches])
        else:
            skills.update(matches)
    
    return list(skills)


def generate_optimization_suggestions(
    resume_text: str,
    job_description: str
) -> Tuple[List[Suggestion], List[str]]:
    """
    Generate optimization suggestions based on resume-job comparison.
    
    Args:
        resume_text: Cleaned resume text
        job_description: Cleaned job description text
        
    Returns:
        Tuple of (suggestions list, missing keywords list)
    """
    suggestions = []
    missing_keywords = []
    
    # Extract skills from both texts
    resume_skills = set(extract_skills_from_text(resume_text))
    job_skills = set(extract_skills_from_text(job_description))
    
    # Find missing skills
    missing_skills = job_skills - resume_skills
    
    # Create suggestions for missing skills
    for skill in list(missing_skills)[:10]:  # Limit to top 10
        missing_keywords.append(skill)
        suggestions.append(Suggestion(
            category="missing_skill",
            title=f"Add {skill.title()} Experience",
            description=f"The job description mentions {skill}, but it's not clearly present in your resume. Consider adding relevant experience or projects involving {skill}.",
            priority="high" if skill in ['python', 'java', 'javascript', 'aws'] else "medium"
        ))
    
    # Basic phrasing suggestions (placeholder - can be enhanced)
    if len(resume_text.split()) < 200:
        suggestions.append(Suggestion(
            category="phrasing",
            title="Expand Resume Content",
            description="Your resume seems brief. Consider adding more detailed descriptions of your responsibilities and achievements using action verbs and quantifiable metrics.",
            priority="medium"
        ))
    
    return suggestions, missing_keywords


def calculate_ats_score(
    resume_text: str,
    job_description: str,
    similarity_score: float,
    missing_keywords: List[str]
) -> float:
    """
    Calculate ATS compatibility score (0-100).
    
    Scoring breakdown:
    - Keyword match percentage: 30%
    - Semantic similarity: 40%
    - Section completeness: 30%
    
    Args:
        resume_text: Cleaned resume text
        job_description: Cleaned job description text
        similarity_score: Semantic similarity score (0-100)
        missing_keywords: List of missing keywords
        
    Returns:
        ATS compatibility score (0-100)
    """
    # Extract keywords from job description
    job_keywords = set(extract_skills_from_text(job_description))
    resume_keywords = set(extract_skills_from_text(resume_text))
    
    # Keyword match percentage (30% weight)
    if len(job_keywords) > 0:
        matched_keywords = job_keywords & resume_keywords
        keyword_match_score = (len(matched_keywords) / len(job_keywords)) * 100
    else:
        keyword_match_score = 50.0
    
    # Semantic similarity (40% weight)
    similarity_component = similarity_score
    
    # Section completeness (30% weight) - basic check for common sections
    resume_lower = resume_text.lower()
    sections = ['experience', 'education', 'skills']
    found_sections = sum(1 for section in sections if section in resume_lower)
    completeness_score = (found_sections / len(sections)) * 100
    
    # Weighted average
    ats_score = (
        keyword_match_score * 0.30 +
        similarity_component * 0.40 +
        completeness_score * 0.30
    )
    
    return min(100, max(0, ats_score))

