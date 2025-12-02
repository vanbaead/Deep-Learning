"""
Text preprocessing and cleaning utilities.
"""
import re
import string


def clean_text(text: str) -> str:
    """
    Clean and normalize text for processing.
    
    Args:
        text: Raw text input
        
    Returns:
        Cleaned text
    """
    if not text:
        return ""
    
    # Convert to lowercase
    text = text.lower()
    
    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Remove special characters but keep alphanumeric and basic punctuation
    text = re.sub(r'[^\w\s.,;:!?-]', ' ', text)
    
    # Trim whitespace
    text = text.strip()
    
    return text


def extract_keywords(text: str, min_length: int = 3) -> list:
    """
    Extract potential keywords from text.
    
    Args:
        text: Input text
        min_length: Minimum keyword length
        
    Returns:
        List of potential keywords
    """
    # Basic keyword extraction - split by common separators
    words = re.findall(r'\b\w+\b', text.lower())
    
    # Filter by length
    keywords = [word for word in words if len(word) >= min_length]
    
    return keywords

