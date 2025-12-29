"""
AI Hashtag Optimizer Tools

Optimize hashtags and keywords for social media reach.
"""

import logging
import os
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


def call_llm(prompt: str, max_tokens: int = 500) -> str:
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


def generate_hashtags(
    topic: str,
    platform: str = "instagram",
    max_hashtags: int = 30,
    mix_popularity: bool = True,
) -> Dict[str, Any]:
    """
    Generate optimized hashtags for a topic.
    
    Args:
        topic: Content topic
        platform: Target platform
        max_hashtags: Maximum hashtags
        mix_popularity: Mix popular and niche hashtags
        
    Returns:
        Dictionary with hashtags
    """
    platform_limits = {
        "instagram": 30,
        "x": 5,
        "linkedin": 5,
        "tiktok": 10,
    }
    
    limit = min(max_hashtags, platform_limits.get(platform, 10))
    
    prompt = f"""Generate {limit} optimized hashtags for this topic: {topic}

Platform: {platform}
{"Mix popular (high reach) and niche (high engagement) hashtags" if mix_popularity else "Focus on relevant hashtags"}

Requirements:
- No spaces in hashtags
- Relevant to the topic
- Mix of broad and specific tags
- Include trending tags if applicable

Format: One hashtag per line, starting with #"""
    
    try:
        result = call_llm(prompt, max_tokens=300)
        
        hashtags = []
        for line in result.split("\n"):
            line = line.strip()
            if line.startswith("#"):
                tag = line.split()[0]  # Get just the hashtag
                hashtags.append(tag)
        
        return {
            "hashtags": hashtags[:limit],
            "platform": platform,
            "count": len(hashtags[:limit]),
        }
    except Exception as e:
        logger.error(f"Error generating hashtags: {e}")
        return {"error": str(e)}


def optimize_keywords(
    topic: str,
    content_type: str = "video",
    max_keywords: int = 20,
) -> Dict[str, Any]:
    """
    Generate optimized keywords for SEO.
    
    Args:
        topic: Content topic
        content_type: Type of content
        max_keywords: Maximum keywords
        
    Returns:
        Dictionary with keywords
    """
    prompt = f"""Generate {max_keywords} SEO keywords for this topic: {topic}

Content type: {content_type}

Include:
- Primary keywords (high search volume)
- Long-tail keywords (specific phrases)
- Related terms
- Question-based keywords

Format: One keyword/phrase per line"""
    
    try:
        result = call_llm(prompt, max_tokens=400)
        
        keywords = []
        for line in result.split("\n"):
            line = line.strip().lstrip("-•").strip()
            if line and len(line) > 2:
                keywords.append(line)
        
        return {
            "keywords": keywords[:max_keywords],
            "topic": topic,
            "count": len(keywords[:max_keywords]),
        }
    except Exception as e:
        logger.error(f"Error generating keywords: {e}")
        return {"error": str(e)}
