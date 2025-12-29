"""
AI Signal Ranker Tools

Tools for ranking news articles by:
- Novelty: How new/unique is this information
- Velocity: How fast is this story spreading
- Relevance: How relevant to AI/tech audience
- Engagement: Social signals (comments, shares)
"""

import logging
import os
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


def calculate_novelty(
    article: Dict[str, Any],
    existing_topics: Optional[List[str]] = None,
) -> float:
    """
    Calculate novelty score for an article.
    
    Args:
        article: Article dictionary
        existing_topics: List of known topics to compare against
        
    Returns:
        Novelty score between 0 and 1
    """
    score = 0.5  # Base score
    
    title = article.get("title", "").lower()
    content = article.get("content", "").lower()
    text = f"{title} {content}"
    
    # Novelty indicators
    novelty_keywords = [
        "breakthrough", "first", "new", "revolutionary", "unprecedented",
        "announces", "launches", "releases", "introduces", "unveils",
        "discovers", "achieves", "beats", "surpasses", "record"
    ]
    
    for keyword in novelty_keywords:
        if keyword in text:
            score += 0.1
    
    # Check against existing topics
    if existing_topics:
        is_new_topic = not any(topic.lower() in text for topic in existing_topics)
        if is_new_topic:
            score += 0.2
    
    return min(1.0, score)


def calculate_velocity(
    article: Dict[str, Any],
    related_articles: Optional[List[Dict[str, Any]]] = None,
) -> float:
    """
    Calculate velocity score based on how fast the story is spreading.
    
    Args:
        article: Article dictionary
        related_articles: Other articles on the same topic
        
    Returns:
        Velocity score between 0 and 1
    """
    score = 0.3  # Base score
    
    # Check engagement metrics
    comments = article.get("comments", 0)
    article_score = article.get("score", 0)
    
    # Normalize engagement
    if comments > 100:
        score += 0.3
    elif comments > 50:
        score += 0.2
    elif comments > 10:
        score += 0.1
    
    if article_score > 500:
        score += 0.2
    elif article_score > 100:
        score += 0.1
    
    # Check recency
    published = article.get("published", "")
    if published:
        try:
            pub_time = datetime.fromisoformat(published.replace("Z", "+00:00"))
            hours_old = (datetime.now(timezone.utc) - pub_time).total_seconds() / 3600
            
            if hours_old < 2:
                score += 0.2
            elif hours_old < 6:
                score += 0.1
        except Exception:
            pass
    
    # Check if multiple sources are covering it
    if related_articles and len(related_articles) > 2:
        score += 0.2
    
    return min(1.0, score)


def calculate_relevance(
    article: Dict[str, Any],
    context: str = "AI technology news",
) -> float:
    """
    Calculate relevance score for target audience.
    
    Args:
        article: Article dictionary
        context: Context for relevance (e.g., "AI technology news")
        
    Returns:
        Relevance score between 0 and 1
    """
    score = 0.3  # Base score
    
    title = article.get("title", "").lower()
    content = article.get("content", "").lower()
    text = f"{title} {content}"
    
    # High relevance keywords for AI audience
    high_relevance = [
        "gpt", "llm", "openai", "anthropic", "claude", "gemini", "google ai",
        "machine learning", "deep learning", "neural network", "transformer",
        "ai agent", "rag", "fine-tuning", "training", "inference",
        "chatgpt", "copilot", "midjourney", "stable diffusion", "dall-e"
    ]
    
    medium_relevance = [
        "artificial intelligence", "automation", "robotics", "nlp",
        "computer vision", "speech recognition", "embedding", "vector",
        "model", "benchmark", "dataset", "research", "paper"
    ]
    
    for keyword in high_relevance:
        if keyword in text:
            score += 0.15
    
    for keyword in medium_relevance:
        if keyword in text:
            score += 0.05
    
    # Source quality bonus
    quality_sources = ["arxiv", "openai", "anthropic", "google", "meta", "microsoft"]
    source = article.get("source", "").lower()
    if any(qs in source for qs in quality_sources):
        score += 0.1
    
    return min(1.0, score)


def calculate_engagement(article: Dict[str, Any]) -> float:
    """
    Calculate engagement score from social signals.
    
    Args:
        article: Article dictionary
        
    Returns:
        Engagement score between 0 and 1
    """
    score = 0.2  # Base score
    
    comments = article.get("comments", 0)
    article_score = article.get("score", 0)
    
    # Logarithmic scaling for engagement
    import math
    
    if comments > 0:
        score += min(0.3, math.log10(comments + 1) / 10)
    
    if article_score > 0:
        score += min(0.3, math.log10(article_score + 1) / 10)
    
    # Check for author reputation (if available)
    author = article.get("author", "")
    if author and len(author) > 0:
        score += 0.1
    
    return min(1.0, score)


def rank_articles(
    articles: List[Dict[str, Any]],
    weights: Optional[Dict[str, float]] = None,
    context: str = "AI technology news",
    top_n: Optional[int] = None,
) -> Dict[str, Any]:
    """
    Rank articles by combined signal scores.
    
    Args:
        articles: List of article dictionaries
        weights: Custom weights for each signal
        context: Context for relevance scoring
        top_n: Return only top N articles
        
    Returns:
        Dictionary with ranked articles and signal breakdown
    """
    if not articles:
        return {"ranked_articles": [], "signals": {}}
    
    weights = weights or {
        "novelty": 0.3,
        "velocity": 0.25,
        "relevance": 0.25,
        "engagement": 0.2,
    }
    
    ranked = []
    
    for article in articles:
        signals = {
            "novelty": calculate_novelty(article),
            "velocity": calculate_velocity(article),
            "relevance": calculate_relevance(article, context),
            "engagement": calculate_engagement(article),
        }
        
        # Calculate weighted score
        total_score = sum(signals[k] * weights.get(k, 0.25) for k in signals)
        
        ranked.append({
            **article,
            "signals": signals,
            "total_score": round(total_score, 3),
        })
    
    # Sort by total score
    ranked.sort(key=lambda x: x["total_score"], reverse=True)
    
    if top_n:
        ranked = ranked[:top_n]
    
    return {
        "ranked_articles": ranked,
        "signals": {
            "weights_used": weights,
            "total_articles": len(ranked),
            "avg_score": sum(a["total_score"] for a in ranked) / len(ranked) if ranked else 0,
        }
    }
