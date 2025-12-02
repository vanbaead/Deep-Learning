"""
PDF text extraction utilities.
"""
from fastapi import UploadFile
import PyPDF2
import io


async def extract_text_from_pdf(file: UploadFile) -> str:
    """
    Extract text content from a PDF file.
    
    Args:
        file: Uploaded PDF file
        
    Returns:
        Extracted text content as string
    """
    try:
        # Read file content
        contents = await file.read()
        
        # Create PDF reader
        pdf_file = io.BytesIO(contents)
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        
        # Extract text from all pages
        text_parts = []
        for page in pdf_reader.pages:
            text_parts.append(page.extract_text())
        
        return "\n".join(text_parts)
    
    except Exception as e:
        raise Exception(f"Error extracting text from PDF: {str(e)}")

