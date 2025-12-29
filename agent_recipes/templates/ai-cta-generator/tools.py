"""
AI CTA + Title Generator Tools

Generate platform-specific:
- Calls to action
- Video/post titles
- Thumbnail text
"""

import logging
import os
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


def call_llm(prompt: str, max_tokens: int = 600) -> str:
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
            "temperature": 0.8,
        },
        timeout=60,
    )
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]


def generate_ctas(
    topic: str,
    platform: str = "youtube",
    cta_type: str = "subscribe",
    num_variants: int = 5,
) -> Dict[str, Any]:
    """
    Generate platform-specific CTAs.
    
    Args:
        topic: Content topic
        platform: Target platform
        cta_type: Type of CTA
        num_variants: Number of variants
        
    Returns:
        Dictionary with CTA variants
    """
    platform_context = {
        "youtube": "YouTube video ending, asking viewers to subscribe and engage",
        "x": "Tweet or thread, asking for retweets and follows",
        "linkedin": "LinkedIn post, asking for comments and connections",
        "instagram": "Instagram post/reel, asking for saves and follows",
        "tiktok": "TikTok video, asking for follows and duets",
    }
    
    cta_context = {
        "subscribe": "Get them to subscribe/follow",
        "comment": "Encourage comments and discussion",
        "share": "Ask them to share with others",
        "click": "Drive clicks to a link",
        "follow": "Get them to follow for more content",
    }
    
    prompt = f"""Generate {num_variants} CTAs for this content:

Topic: {topic}
Platform: {platform} - {platform_context.get(platform, 'social media')}
Goal: {cta_context.get(cta_type, 'engage audience')}

Requirements:
- Natural, conversational tone
- Platform-appropriate language
- Create urgency without being pushy
- Each CTA should be different in approach

Format each CTA on its own line, numbered 1-{num_variants}."""
    
    result = call_llm(prompt, max_tokens=500)
    
    ctas = []
    for line in result.split("\n"):
        line = line.strip()
        if line and (line[0].isdigit() or line.startswith("-")):
            # Remove numbering
            cta_text = line.lstrip("0123456789.-) ").strip()
            if cta_text:
                ctas.append({
                    "text": cta_text,
                    "platform": platform,
                    "type": cta_type,
                })
    
    return {
        "ctas": ctas[:num_variants],
        "platform": platform,
        "cta_type": cta_type,
    }


def generate_titles(
    topic: str,
    platform: str = "youtube",
    num_variants: int = 5,
    include_emoji: bool = False,
) -> Dict[str, Any]:
    """
    Generate platform-optimized titles.
    
    Args:
        topic: Content topic
        platform: Target platform
        num_variants: Number of title variants
        include_emoji: Include emojis in titles
        
    Returns:
        Dictionary with title variants
    """
    platform_limits = {
        "youtube": 100,
        "x": 280,
        "linkedin": 150,
        "instagram": 125,
        "tiktok": 150,
    }
    
    max_chars = platform_limits.get(platform, 100)
    
    prompt = f"""Generate {num_variants} titles for this content:

Topic: {topic}
Platform: {platform}
Max characters: {max_chars}
{"Include relevant emojis" if include_emoji else "No emojis"}

Title styles to include:
- How-to / Tutorial
- Listicle (X things...)
- Question
- Bold statement
- Curiosity gap

Format each title on its own line, numbered 1-{num_variants}."""
    
    result = call_llm(prompt, max_tokens=400)
    
    titles = []
    for line in result.split("\n"):
        line = line.strip()
        if line and (line[0].isdigit() or line.startswith("-")):
            title_text = line.lstrip("0123456789.-) ").strip()
            if title_text:
                titles.append({
                    "text": title_text[:max_chars],
                    "platform": platform,
                    "char_count": len(title_text),
                })
    
    return {
        "titles": titles[:num_variants],
        "platform": platform,
    }
