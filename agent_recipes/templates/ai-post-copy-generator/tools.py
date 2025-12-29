"""
AI Post Copy Generator Tools

Generate platform-specific copy for social media posts.
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


def generate_post_copy(
    topic: str,
    platform: str = "x",
    tone: str = "professional",
    include_hashtags: bool = True,
    include_cta: bool = True,
) -> Dict[str, Any]:
    """
    Generate platform-specific post copy.
    
    Args:
        topic: Post topic
        platform: Target platform
        tone: Writing tone
        include_hashtags: Include hashtags
        include_cta: Include call to action
        
    Returns:
        Dictionary with generated copy
    """
    platform_limits = {
        "x": 280,
        "linkedin": 3000,
        "youtube": 5000,
        "instagram": 2200,
    }
    
    max_length = platform_limits.get(platform, 500)
    
    prompt = f"""Write a {platform} post about: {topic}

Requirements:
- Tone: {tone}
- Max length: {max_length} characters
- Platform: {platform}
{"- Include 3-5 relevant hashtags" if include_hashtags else ""}
{"- End with a call to action" if include_cta else ""}

Write engaging copy optimized for {platform}:"""
    
    try:
        copy = call_llm(prompt, max_tokens=400)
        
        return {
            "copy": copy.strip(),
            "platform": platform,
            "length": len(copy),
            "within_limit": len(copy) <= max_length,
        }
    except Exception as e:
        logger.error(f"Error generating copy: {e}")
        return {"error": str(e)}


def generate_multi_platform_copy(
    topic: str,
    platforms: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """
    Generate copy for multiple platforms.
    
    Args:
        topic: Post topic
        platforms: Target platforms
        
    Returns:
        Dictionary with copy for each platform
    """
    platforms = platforms or ["x", "linkedin", "youtube"]
    copies = {}
    
    for platform in platforms:
        result = generate_post_copy(topic, platform)
        copies[platform] = result
    
    return {"copies": copies, "topic": topic}
