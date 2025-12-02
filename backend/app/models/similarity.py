"""
Semantic similarity scoring using Sentence-BERT.
"""
from sentence_transformers import SentenceTransformer
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import os


# Global model variable (will be loaded on first use)
_model = None
_model_name = "sentence-transformers/all-MiniLM-L6-v2"


def _load_model():
    """Load the Sentence-BERT model (lazy loading)."""
    global _model
    if _model is None:
        print(f"Loading Sentence-BERT model: {_model_name}")
        _model = SentenceTransformer(_model_name)
        print("Model loaded successfully!")
    return _model


def compute_similarity_score(resume_text: str, job_description: str) -> float:
    """
    Compute semantic similarity score between resume and job description.
    
    Args:
        resume_text: Cleaned resume text
        job_description: Cleaned job description text
        
    Returns:
        Similarity score between 0 and 100
    """
    try:
        model = _load_model()
        
        # Generate embeddings
        resume_embedding = model.encode([resume_text])[0]
        job_embedding = model.encode([job_description])[0]
        
        # Compute cosine similarity
        similarity = cosine_similarity(
            [resume_embedding],
            [job_embedding]
        )[0][0]
        
        # Convert to 0-100 scale
        score = (similarity + 1) * 50  # cosine similarity is -1 to 1, scale to 0-100
        
        return min(100, max(0, score))
    
    except Exception as e:
        # Fallback to basic scoring if model fails
        print(f"Error computing similarity: {e}")
        return 50.0  # Return neutral score on error

