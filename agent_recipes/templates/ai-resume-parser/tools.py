"""
Tools for ai-resume-parser recipe.
Uses OCRAgent for resume text extraction and structured parsing.
"""

from praisonaiagents import OCRAgent
from praisonaiagents.tools import read_file
import json

_ocr_agent = None

def _get_ocr_agent():
    global _ocr_agent
    if _ocr_agent is None:
        _ocr_agent = OCRAgent(llm="mistral/mistral-ocr-latest")
    return _ocr_agent


def extract_resume_text(resume_path: str) -> str:
    """
    Extract text from resume (PDF/image).
    
    Args:
        resume_path: Path to resume file
        
    Returns:
        Extracted text
    """
    agent = _get_ocr_agent()
    return agent.read(resume_path)


def parse_resume_sections(text: str) -> str:
    """
    Parse resume text into standard sections.
    Returns JSON with sections: contact, summary, experience, education, skills.
    
    Args:
        text: Raw resume text
        
    Returns:
        JSON string with parsed sections
    """
    # This returns the text for LLM to parse into structured format
    return f"""Parse this resume into structured JSON:
{text}

Return JSON with these sections:
- contact: name, email, phone, location, linkedin
- summary: professional summary
- experience: list of jobs with company, title, dates, description
- education: list of degrees with school, degree, dates
- skills: list of skills
"""


def extract_contact_info(text: str) -> str:
    """
    Extract contact information from resume text.
    
    Args:
        text: Resume text
        
    Returns:
        Contact information
    """
    import re
    
    email_pattern = r'[\w\.-]+@[\w\.-]+\.\w+'
    phone_pattern = r'[\+]?[\d\s\-\(\)]{10,}'
    
    emails = re.findall(email_pattern, text)
    phones = re.findall(phone_pattern, text)
    
    result = {
        "emails": emails[:2] if emails else [],
        "phones": [p.strip() for p in phones[:2]] if phones else []
    }
    return json.dumps(result, indent=2)


def read_text_file(file_path: str) -> str:
    """
    Read plain text resume files.
    
    Args:
        file_path: Path to text file
        
    Returns:
        File content
    """
    return read_file(file_path)


TOOLS = [extract_resume_text, parse_resume_sections, extract_contact_info, read_text_file]


def get_all_tools():
    return TOOLS
