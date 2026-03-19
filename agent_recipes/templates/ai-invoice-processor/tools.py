"""
Tools for ai-invoice-processor recipe.
Uses OCRAgent for invoice extraction and structured data parsing.
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


def extract_invoice_text(invoice_path: str) -> str:
    """
    Extract text from invoice (PDF/image).
    
    Args:
        invoice_path: Path to invoice file
        
    Returns:
        Extracted text
    """
    agent = _get_ocr_agent()
    return agent.read(invoice_path)


def parse_invoice_data(text: str) -> str:
    """
    Parse invoice text into structured data.
    
    Args:
        text: Raw invoice text
        
    Returns:
        JSON string with invoice data
    """
    return f"""Parse this invoice into structured JSON:
{text}

Return JSON with:
- invoice_number: string
- date: string
- due_date: string
- vendor: name, address, contact
- customer: name, address
- line_items: list of (description, quantity, unit_price, total)
- subtotal: number
- tax: number
- total: number
- payment_terms: string
"""


def extract_amounts(text: str) -> str:
    """
    Extract monetary amounts from invoice text.
    
    Args:
        text: Invoice text
        
    Returns:
        JSON with amounts found
    """
    import re
    
    # Match common currency formats
    amount_pattern = r'[\$€£]\s*[\d,]+\.?\d*|\d+[\.,]\d{2}\s*(?:USD|EUR|GBP)?'
    amounts = re.findall(amount_pattern, text)
    
    return json.dumps({
        "amounts_found": amounts[:10],  # First 10 amounts
        "likely_total": amounts[-1] if amounts else None
    }, indent=2)


def validate_invoice(data: str) -> str:
    """
    Validate invoice data completeness.
    
    Args:
        data: JSON invoice data
        
    Returns:
        Validation result
    """
    try:
        invoice = json.loads(data)
        required = ['invoice_number', 'date', 'total', 'vendor']
        missing = [f for f in required if not invoice.get(f)]
        
        if missing:
            return f"Missing required fields: {', '.join(missing)}"
        return "Invoice data is complete"
    except json.JSONDecodeError:
        return "Invalid JSON data"


TOOLS = [extract_invoice_text, parse_invoice_data, extract_amounts, validate_invoice]


def get_all_tools():
    return TOOLS
