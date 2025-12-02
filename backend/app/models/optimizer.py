"""
Resume optimization logic - suggestions and ATS scoring.
"""
from typing import List, Tuple
from app.schemas import Suggestion
import re

# Curated list of common technical keywords we want to detect.
TECHNICAL_SKILLS = {
    # Languages
    'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'go', 'rust', 'swift',
    'kotlin', 'php', 'ruby', 'r', 'scala', 'matlab',
    # Frameworks & libraries
    'react', 'angular', 'vue', 'node.js', 'express', 'django', 'flask', 'spring',
    'laravel', 'rails', 'asp.net',
    # Databases
    'sql', 'mysql', 'postgresql', 'mongodb', 'redis', 'elasticsearch', 'dynamodb',
    # Cloud & devops
    'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'jenkins', 'terraform', 'ansible',
    'ci/cd', 'github actions', 'gitlab',
    # Tools & platforms
    'git', 'linux', 'rest api', 'graphql', 'microservices', 'agile', 'scrum',
    # Data / ML
    'machine learning', 'deep learning', 'data science', 'pandas', 'numpy',
    'tensorflow', 'pytorch', 'scikit-learn', 'spark', 'hadoop',
    # Frontend
    'html', 'css', 'sass', 'webpack', 'babel', 'npm', 'yarn'
}

# Stop words (non-skills) to filter out during extraction.
STOP_WORDS = {
    'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having',
    'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'or', 'but', 'if', 'then',
    'else', 'when', 'where', 'how', 'why', 'what', 'who', 'which', 'that', 'this',
    'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her',
    'us', 'them', 'my', 'your', 'his', 'her', 'its', 'our', 'their', 'should', 'would',
    'could', 'may', 'might', 'must', 'can', 'will', 'shall', 'seek', 'seeking',
    'ideal', 'candidate', 'looking', 'want', 'needs', 'need', 'required', 'requires',
    'requirement', 'requirements', 'years', 'year', 'experience', 'experiences',
    'platform', 'platforms', 'responsible', 'responsibilities'
}


def extract_skills_from_text(text: str) -> List[str]:
    """
    Extract potential technical skills/keywords from text.
    """
    if not text:
        return []

    text_lower = text.lower()
    skills = set()

    # Match curated technical skills by substring.
    for skill in TECHNICAL_SKILLS:
        if skill in text_lower:
            skills.add(skill)

    # Capture acronyms with 2-5 uppercase letters (e.g., AWS, API).
    acronyms = re.findall(r'\b[A-Z]{2,5}\b', text)
    for acronym in acronyms:
        acronym_lower = acronym.lower()
        if acronym_lower not in STOP_WORDS:
            skills.add(acronym_lower)

    # Additional multi-word patterns not covered by simple lookup.
    multi_word_patterns = [
        r'\b(machine learning|deep learning|data science|web development|software engineering|cloud computing|devops|full stack|front end|back end|ui/ux)\b',
        r'\b(node\.js|react\.js|angular\.js|rest api|graphql api)\b'
    ]
    for pattern in multi_word_patterns:
        matches = re.findall(pattern, text_lower, re.IGNORECASE)
        for match in matches:
            if isinstance(match, tuple):
                skills.update(match)
            else:
                skills.add(match)

    # Remove stop words and very short tokens.
    filtered_skills = {
        skill.strip()
        for skill in skills
        if skill and skill not in STOP_WORDS and len(skill) > 2
    }

    return sorted(filtered_skills)


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

    # Prioritize critical skills first.
    priority_skills = {
        'python', 'java', 'javascript', 'react', 'node.js', 'aws',
        'docker', 'kubernetes', 'sql', 'machine learning', 'data science'
    }
    missing_skills_sorted = sorted(
        missing_skills,
        key=lambda skill: (skill not in priority_skills, skill)
    )
    
    # Create suggestions for missing skills (limit to 10 meaningful skills)
    for skill in missing_skills_sorted:
        if skill in STOP_WORDS or len(skill) < 3:
            continue
        missing_keywords.append(skill)
        suggestions.append(Suggestion(
            category="missing_skill",
            title=f"Add {skill.title()} Experience",
            description=f"The job description mentions {skill}, but it's not clearly present in your resume. Consider adding relevant experience or projects involving {skill}.",
            priority="high" if skill in priority_skills else "medium"
        ))
        if len(missing_keywords) >= 10:
            break
    
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
    job_keywords = {
        keyword for keyword in extract_skills_from_text(job_description)
        if keyword not in STOP_WORDS
    }
    resume_keywords = {
        keyword for keyword in extract_skills_from_text(resume_text)
        if keyword not in STOP_WORDS
    }
    
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

