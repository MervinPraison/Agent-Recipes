"""
Tools for ai-pdf-summarizer recipe.
Uses OCRAgent for PDF text extraction and analysis.
"""

from praisonaiagents import OCRAgent
from praisonaiagents.tools import read_file

_ocr_agent = None

def _get_ocr_agent():
    global _ocr_agent
    if _ocr_agent is None:
        _ocr_agent = OCRAgent(llm="mistral/mistral-ocr-latest")
    return _ocr_agent


def extract_pdf_text(pdf_path: str, pages: list = None) -> str:
    """
    Extract text from PDF using OCR.
    
    Args:
        pdf_path: Path to PDF file or URL
        pages: Optional list of specific pages to extract
        
    Returns:
        Extracted text as markdown
    """
    agent = _get_ocr_agent()
    result = agent.extract(pdf_path, pages=pages)
    return result if isinstance(result, str) else str(result)


def read_pdf(pdf_path: str) -> str:
    """
    Quick read PDF and return text content.
    
    Args:
        pdf_path: Path to PDF file
        
    Returns:
        Extracted text
    """
    agent = _get_ocr_agent()
    return agent.read(pdf_path)


def extract_pdf_sections(pdf_path: str) -> str:
    """
    Extract text with section identification.
    
    Args:
        pdf_path: Path to PDF file
        
    Returns:
        Text with section headers identified
    """
    agent = _get_ocr_agent()
    text = agent.read(pdf_path)
    # The OCR returns markdown which preserves headers
    return text


def read_text_file(file_path: str) -> str:
    """
    Read plain text files.
    
    Args:
        file_path: Path to text file
        
    Returns:
        File content
    """
    return read_file(file_path)


TOOLS = [extract_pdf_text, read_pdf, extract_pdf_sections, read_text_file]


def get_all_tools():
    return TOOLS
