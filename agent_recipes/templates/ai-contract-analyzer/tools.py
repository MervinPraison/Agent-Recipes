"""
Tools for ai-contract-analyzer recipe.
Uses OCRAgent for contract text extraction and analysis.
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


def extract_contract_text(contract_path: str) -> str:
    """
    Extract text from contract document (PDF/image).
    
    Args:
        contract_path: Path to contract file
        
    Returns:
        Extracted text
    """
    agent = _get_ocr_agent()
    return agent.read(contract_path)


def identify_key_clauses(text: str) -> str:
    """
    Identify key clauses in contract text.
    
    Args:
        text: Contract text
        
    Returns:
        Key clauses identified
    """
    return f"""Analyze this contract and identify key clauses:
{text[:5000]}...

List these clause types if present:
- Parties involved
- Effective date and term
- Payment terms
- Termination conditions
- Confidentiality provisions
- Liability limitations
- Dispute resolution
- Governing law
"""


def extract_dates_deadlines(text: str) -> str:
    """
    Extract important dates and deadlines from contract.
    
    Args:
        text: Contract text
        
    Returns:
        JSON with dates found
    """
    import re
    
    # Common date patterns
    date_patterns = [
        r'\d{1,2}[/\-\.]\d{1,2}[/\-\.]\d{2,4}',
        r'(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{1,2},?\s+\d{4}',
        r'\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{4}'
    ]
    
    dates = []
    for pattern in date_patterns:
        dates.extend(re.findall(pattern, text, re.IGNORECASE))
    
    return json.dumps({"dates_found": list(set(dates))[:20]}, indent=2)


def read_text_file(file_path: str) -> str:
    """
    Read plain text contract files.
    
    Args:
        file_path: Path to text file
        
    Returns:
        File content
    """
    return read_file(file_path)


TOOLS = [extract_contract_text, identify_key_clauses, extract_dates_deadlines, read_text_file]


def get_all_tools():
    return TOOLS
