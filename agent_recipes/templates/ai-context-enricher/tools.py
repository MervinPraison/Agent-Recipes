"""
AI Context Enricher Tools

Tools for enriching news articles with:
- Background context
- Prior art references
- Stakeholder analysis (who benefits)
- Hype detection
"""

import logging
import os
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


def call_llm(prompt: str, max_tokens: int = 500) -> str:
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
            "temperature": 0.7,
        },
        timeout=60,
    )
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]


def add_background(
    article: Dict[str, Any],
    max_length: int = 300,
) -> Dict[str, Any]:
    """
    Add background context to an article.
    
    Args:
        article: Article dictionary
        max_length: Maximum length of background text
        
    Returns:
        Article with background field added
    """
    title = article.get("title", "")
    content = article.get("content", "")[:500]
    
    prompt = f"""Given this AI news article, provide brief background context that helps readers understand the significance.

Title: {title}
Content: {content}

Provide 2-3 sentences of background context explaining:
1. What problem this addresses
2. Why it matters now
3. Key context readers should know

Background:"""
    
    try:
        background = call_llm(prompt, max_tokens=200)
        article["background"] = background.strip()
    except Exception as e:
        logger.warning(f"Error adding background: {e}")
        article["background"] = ""
    
    return article


def find_prior_art(
    article: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Find and reference prior art related to the article.
    
    Args:
        article: Article dictionary
        
    Returns:
        Article with prior_art field added
    """
    title = article.get("title", "")
    content = article.get("content", "")[:500]
    
    prompt = f"""Given this AI news article, identify relevant prior art and historical context.

Title: {title}
Content: {content}

List 2-3 relevant prior developments or research that led to this:
- Include approximate dates if known
- Mention key papers, products, or milestones
- Keep each item to one sentence

Prior Art:"""
    
    try:
        prior_art = call_llm(prompt, max_tokens=250)
        article["prior_art"] = prior_art.strip()
    except Exception as e:
        logger.warning(f"Error finding prior art: {e}")
        article["prior_art"] = ""
    
    return article


def analyze_stakeholders(
    article: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Analyze who benefits and who is affected by this news.
    
    Args:
        article: Article dictionary
        
    Returns:
        Article with stakeholders field added
    """
    title = article.get("title", "")
    content = article.get("content", "")[:500]
    
    prompt = f"""Analyze the stakeholders for this AI news:

Title: {title}
Content: {content}

Identify:
1. Who benefits most from this development?
2. Who might be negatively affected?
3. What industries or groups should pay attention?

Keep response concise (3-4 sentences).

Stakeholder Analysis:"""
    
    try:
        stakeholders = call_llm(prompt, max_tokens=200)
        article["stakeholders"] = stakeholders.strip()
    except Exception as e:
        logger.warning(f"Error analyzing stakeholders: {e}")
        article["stakeholders"] = ""
    
    return article


def detect_hype(
    article: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Detect hype level and provide reality check.
    
    Args:
        article: Article dictionary
        
    Returns:
        Article with hype_analysis field added
    """
    title = article.get("title", "")
    content = article.get("content", "")[:500]
    
    prompt = f"""Analyze the hype level of this AI news:

Title: {title}
Content: {content}

Provide:
1. Hype Level: LOW / MEDIUM / HIGH / OVERHYPED
2. Reality Check: One sentence on what's actually new vs marketing
3. Confidence: How confident are you in this assessment (LOW/MEDIUM/HIGH)

Format as:
Hype Level: [level]
Reality Check: [assessment]
Confidence: [level]"""
    
    try:
        hype_analysis = call_llm(prompt, max_tokens=150)
        
        # Parse the response
        lines = hype_analysis.strip().split("\n")
        hype_data = {
            "raw": hype_analysis.strip(),
            "level": "MEDIUM",
            "reality_check": "",
            "confidence": "MEDIUM",
        }
        
        for line in lines:
            if "Hype Level:" in line:
                hype_data["level"] = line.split(":")[-1].strip().upper()
            elif "Reality Check:" in line:
                hype_data["reality_check"] = line.split(":", 1)[-1].strip()
            elif "Confidence:" in line:
                hype_data["confidence"] = line.split(":")[-1].strip().upper()
        
        article["hype_analysis"] = hype_data
    except Exception as e:
        logger.warning(f"Error detecting hype: {e}")
        article["hype_analysis"] = {"level": "UNKNOWN", "reality_check": "", "confidence": "LOW"}
    
    return article


def enrich_articles(
    articles: List[Dict[str, Any]],
    enrichment_types: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """
    Enrich multiple articles with context.
    
    Args:
        articles: List of article dictionaries
        enrichment_types: Types of enrichment to apply
        
    Returns:
        Dictionary with enriched articles
    """
    enrichment_types = enrichment_types or ["background", "prior_art", "stakeholders", "hype_detection"]
    
    enriched = []
    
    for article in articles:
        enriched_article = article.copy()
        
        if "background" in enrichment_types:
            enriched_article = add_background(enriched_article)
        
        if "prior_art" in enrichment_types:
            enriched_article = find_prior_art(enriched_article)
        
        if "stakeholders" in enrichment_types:
            enriched_article = analyze_stakeholders(enriched_article)
        
        if "hype_detection" in enrichment_types:
            enriched_article = detect_hype(enriched_article)
        
        enriched.append(enriched_article)
    
    return {
        "enriched_articles": enriched,
        "stats": {
            "total_enriched": len(enriched),
            "enrichment_types": enrichment_types,
        }
    }
