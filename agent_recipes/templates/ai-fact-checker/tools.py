"""
AI Fact Checker Tools

Verify content accuracy with:
- Claim extraction
- Source verification
- Citation linking
- Confidence scoring
"""

import logging
import os
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


def call_llm(prompt: str, max_tokens: int = 1000) -> str:
    """Call OpenAI API for text generation."""
    import requests
    
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not set")
    
    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": "gpt-4o-mini",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": max_tokens,
            "temperature": 0.3,
        },
        timeout=60,
    )
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]


def extract_claims(
    content: str,
    claim_types: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """
    Extract verifiable claims from content.
    
    Args:
        content: Text content to analyze
        claim_types: Types of claims to extract
        
    Returns:
        Dictionary with extracted claims
    """
    claim_types = claim_types or ["factual", "statistical", "quote", "date"]
    
    prompt = f"""Extract all verifiable claims from this content:

{content[:3000]}

For each claim, identify:
1. The claim text
2. Claim type (factual, statistical, quote, date, attribution)
3. Confidence that this is a verifiable claim (HIGH/MEDIUM/LOW)

Format as:
CLAIM: [claim text]
TYPE: [type]
CONFIDENCE: [level]
---"""
    
    result = call_llm(prompt, max_tokens=1500)
    
    claims = []
    current_claim = {}
    
    for line in result.split("\n"):
        line = line.strip()
        if line.startswith("CLAIM:"):
            if current_claim:
                claims.append(current_claim)
            current_claim = {"claim": line[6:].strip()}
        elif line.startswith("TYPE:"):
            current_claim["type"] = line[5:].strip().lower()
        elif line.startswith("CONFIDENCE:"):
            current_claim["confidence"] = line[11:].strip().upper()
        elif line == "---" and current_claim:
            claims.append(current_claim)
            current_claim = {}
    
    if current_claim and "claim" in current_claim:
        claims.append(current_claim)
    
    return {
        "claims": claims,
        "total_claims": len(claims),
    }


def verify_claims(
    claims: List[Dict[str, Any]],
) -> Dict[str, Any]:
    """
    Verify extracted claims.
    
    Args:
        claims: List of claim dictionaries
        
    Returns:
        Dictionary with verification results
    """
    verified = []
    
    for claim in claims:
        claim_text = claim.get("claim", "")
        
        prompt = f"""Verify this claim and assess its accuracy:

Claim: {claim_text}

Provide:
1. VERDICT: TRUE / FALSE / PARTIALLY TRUE / UNVERIFIABLE
2. EXPLANATION: Brief explanation (1-2 sentences)
3. SUGGESTED_SOURCE: Type of source that could verify this

Format:
VERDICT: [verdict]
EXPLANATION: [explanation]
SUGGESTED_SOURCE: [source type]"""
        
        try:
            result = call_llm(prompt, max_tokens=300)
            
            verification = {
                **claim,
                "verdict": "UNVERIFIABLE",
                "explanation": "",
                "suggested_source": "",
            }
            
            for line in result.split("\n"):
                line = line.strip()
                if line.startswith("VERDICT:"):
                    verification["verdict"] = line[8:].strip().upper()
                elif line.startswith("EXPLANATION:"):
                    verification["explanation"] = line[12:].strip()
                elif line.startswith("SUGGESTED_SOURCE:"):
                    verification["suggested_source"] = line[17:].strip()
            
            verified.append(verification)
            
        except Exception as e:
            logger.warning(f"Error verifying claim: {e}")
            verified.append({
                **claim,
                "verdict": "ERROR",
                "explanation": str(e),
            })
    
    # Generate flags for problematic claims
    flags = []
    for v in verified:
        if v.get("verdict") in ["FALSE", "PARTIALLY TRUE"]:
            flags.append({
                "claim": v.get("claim", ""),
                "issue": v.get("verdict"),
                "explanation": v.get("explanation", ""),
            })
    
    return {
        "verified_claims": verified,
        "flags": flags,
        "stats": {
            "total": len(verified),
            "true": sum(1 for v in verified if v.get("verdict") == "TRUE"),
            "false": sum(1 for v in verified if v.get("verdict") == "FALSE"),
            "partial": sum(1 for v in verified if v.get("verdict") == "PARTIALLY TRUE"),
            "unverifiable": sum(1 for v in verified if v.get("verdict") == "UNVERIFIABLE"),
        }
    }


def find_citations(
    claims: List[Dict[str, Any]],
    use_web_search: bool = True,
) -> Dict[str, Any]:
    """
    Find citation sources for claims.
    
    Args:
        claims: List of claim dictionaries
        use_web_search: Use web search for citations
        
    Returns:
        Dictionary with citations
    """
    citations = []
    
    # Check for Tavily API
    tavily_key = os.environ.get("TAVILY_API_KEY")
    
    for claim in claims:
        claim_text = claim.get("claim", "")
        
        citation = {
            "claim": claim_text,
            "sources": [],
        }
        
        if use_web_search and tavily_key:
            try:
                import requests
                
                response = requests.post(
                    "https://api.tavily.com/search",
                    json={
                        "api_key": tavily_key,
                        "query": f"verify: {claim_text}",
                        "search_depth": "basic",
                        "max_results": 3,
                    },
                    timeout=30,
                )
                response.raise_for_status()
                data = response.json()
                
                for result in data.get("results", []):
                    citation["sources"].append({
                        "title": result.get("title", ""),
                        "url": result.get("url", ""),
                        "snippet": result.get("content", "")[:200],
                    })
                    
            except Exception as e:
                logger.warning(f"Error searching for citation: {e}")
        
        citations.append(citation)
    
    return {
        "citations": citations,
        "total_sources": sum(len(c["sources"]) for c in citations),
    }


def fact_check_content(
    content: str,
    include_citations: bool = True,
) -> Dict[str, Any]:
    """
    Full fact-checking pipeline.
    
    Args:
        content: Content to fact-check
        include_citations: Include source citations
        
    Returns:
        Complete fact-check report
    """
    # Extract claims
    extraction = extract_claims(content)
    claims = extraction.get("claims", [])
    
    # Verify claims
    verification = verify_claims(claims)
    
    # Find citations if requested
    citations = {}
    if include_citations:
        citations = find_citations(claims)
    
    return {
        "claims": verification.get("verified_claims", []),
        "flags": verification.get("flags", []),
        "citations": citations.get("citations", []),
        "stats": verification.get("stats", {}),
    }
