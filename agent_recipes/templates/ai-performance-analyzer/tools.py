"""
AI Performance Analyzer Tools

Analyze content performance metrics and generate insights.
"""

import logging
import os
from typing import Any, Dict, List, Optional

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


def analyze_metrics(
    metrics: Dict[str, Any],
    platform: str = "youtube",
) -> Dict[str, Any]:
    """
    Analyze performance metrics.
    
    Args:
        metrics: Metrics dictionary from platform export
        platform: Source platform
        
    Returns:
        Analysis results
    """
    # Extract key metrics
    views = metrics.get("views", metrics.get("impressions", 0))
    engagement = metrics.get("engagement", metrics.get("likes", 0) + metrics.get("comments", 0))
    shares = metrics.get("shares", metrics.get("retweets", 0))
    
    # Calculate rates
    engagement_rate = (engagement / views * 100) if views > 0 else 0
    
    analysis = {
        "platform": platform,
        "total_views": views,
        "total_engagement": engagement,
        "engagement_rate": round(engagement_rate, 2),
        "shares": shares,
        "performance_tier": _get_performance_tier(engagement_rate),
    }
    
    return {"analysis": analysis}


def _get_performance_tier(engagement_rate: float) -> str:
    """Determine performance tier based on engagement rate."""
    if engagement_rate >= 10:
        return "exceptional"
    elif engagement_rate >= 5:
        return "excellent"
    elif engagement_rate >= 2:
        return "good"
    elif engagement_rate >= 1:
        return "average"
    else:
        return "needs_improvement"


def generate_insights(
    metrics: Dict[str, Any],
    historical: Optional[List[Dict[str, Any]]] = None,
) -> Dict[str, Any]:
    """
    Generate AI-powered insights from metrics.
    
    Args:
        metrics: Current metrics
        historical: Historical metrics for comparison
        
    Returns:
        Insights and recommendations
    """
    metrics_summary = f"""
Views: {metrics.get('views', 'N/A')}
Likes: {metrics.get('likes', 'N/A')}
Comments: {metrics.get('comments', 'N/A')}
Shares: {metrics.get('shares', 'N/A')}
Watch Time: {metrics.get('watch_time', 'N/A')}
CTR: {metrics.get('ctr', 'N/A')}%
"""
    
    prompt = f"""Analyze these content performance metrics and provide actionable insights:

{metrics_summary}

Provide:
1. Key Performance Summary (2-3 sentences)
2. Top 3 Strengths
3. Top 3 Areas for Improvement
4. 3 Specific Recommendations

Be specific and actionable."""
    
    try:
        insights_text = call_llm(prompt, max_tokens=600)
        
        return {
            "insights": insights_text,
            "metrics_analyzed": list(metrics.keys()),
        }
    except Exception as e:
        logger.error(f"Error generating insights: {e}")
        return {"error": str(e)}


def compare_performance(
    current: Dict[str, Any],
    previous: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Compare current vs previous performance.
    
    Args:
        current: Current period metrics
        previous: Previous period metrics
        
    Returns:
        Comparison results
    """
    comparison = {}
    
    for key in current:
        if key in previous and isinstance(current[key], (int, float)):
            prev_val = previous[key]
            curr_val = current[key]
            
            if prev_val > 0:
                change_pct = ((curr_val - prev_val) / prev_val) * 100
            else:
                change_pct = 100 if curr_val > 0 else 0
            
            comparison[key] = {
                "current": curr_val,
                "previous": prev_val,
                "change": curr_val - prev_val,
                "change_percent": round(change_pct, 2),
                "trend": "up" if change_pct > 0 else "down" if change_pct < 0 else "flat",
            }
    
    return {"comparison": comparison}
