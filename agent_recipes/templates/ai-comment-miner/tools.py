"""
AI Comment Miner Tools

Extract content ideas and insights from comments.
"""

import logging
import os
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


def call_llm(prompt: str, max_tokens: int = 800) -> str:
    """Call OpenAI API."""
    import requests
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not set")
    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json={"model": "gpt-4o-mini", "messages": [{"role": "user", "content": prompt}], "max_tokens": max_tokens},
        timeout=60,
    )
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]


def extract_ideas(
    comments: List[str],
    max_ideas: int = 10,
) -> Dict[str, Any]:
    """
    Extract content ideas from comments.
    
    Args:
        comments: List of comment texts
        max_ideas: Maximum ideas to extract
        
    Returns:
        Dictionary with extracted ideas
    """
    comments_text = "\n".join([f"- {c[:200]}" for c in comments[:50]])
    
    prompt = f"""Analyze these audience comments and extract content ideas:

{comments_text}

Extract:
1. Questions people are asking (potential video topics)
2. Pain points mentioned (problems to solve)
3. Requests for content (what they want to see)
4. Trending topics mentioned

Provide {max_ideas} specific, actionable content ideas based on these comments.
Format each idea on its own line."""
    
    try:
        result = call_llm(prompt, max_tokens=600)
        
        ideas = []
        for line in result.split("\n"):
            line = line.strip().lstrip("-•0123456789.").strip()
            if line and len(line) > 10:
                ideas.append(line)
        
        return {
            "ideas": ideas[:max_ideas],
            "comments_analyzed": len(comments),
        }
    except Exception as e:
        logger.error(f"Error extracting ideas: {e}")
        return {"error": str(e)}


def analyze_sentiment(
    comments: List[str],
) -> Dict[str, Any]:
    """
    Analyze sentiment of comments.
    
    Args:
        comments: List of comment texts
        
    Returns:
        Sentiment analysis results
    """
    positive = 0
    negative = 0
    neutral = 0
    
    positive_words = ["love", "great", "awesome", "amazing", "helpful", "thanks", "best", "excellent"]
    negative_words = ["hate", "bad", "terrible", "worst", "boring", "waste", "disappointed"]
    
    for comment in comments:
        comment_lower = comment.lower()
        pos_count = sum(1 for w in positive_words if w in comment_lower)
        neg_count = sum(1 for w in negative_words if w in comment_lower)
        
        if pos_count > neg_count:
            positive += 1
        elif neg_count > pos_count:
            negative += 1
        else:
            neutral += 1
    
    total = len(comments)
    
    return {
        "sentiment": {
            "positive": positive,
            "negative": negative,
            "neutral": neutral,
            "positive_rate": round(positive / total * 100, 1) if total > 0 else 0,
            "negative_rate": round(negative / total * 100, 1) if total > 0 else 0,
        },
        "total_analyzed": total,
    }


def mine_comments(
    comments: List[str],
) -> Dict[str, Any]:
    """
    Full comment mining pipeline.
    
    Args:
        comments: List of comment texts
        
    Returns:
        Complete mining results
    """
    ideas = extract_ideas(comments)
    sentiment = analyze_sentiment(comments)
    
    return {
        "ideas": ideas.get("ideas", []),
        "sentiment": sentiment.get("sentiment", {}),
        "total_comments": len(comments),
    }
