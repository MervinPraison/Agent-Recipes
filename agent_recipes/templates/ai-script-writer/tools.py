"""
AI Script Writer Tools

Multi-format script generation for:
- YouTube long-form (10+ min)
- YouTube Shorts (60s)
- 30-second hooks
- X/Twitter threads
- LinkedIn posts
- Image captions
"""

import logging
import os
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


def call_llm(prompt: str, max_tokens: int = 2000) -> str:
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
        timeout=120,
    )
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]


def write_youtube_script(
    topic: str,
    target_length: int = 600,
    tone: str = "educational",
    key_points: Optional[List[str]] = None,
    include_timestamps: bool = True,
) -> Dict[str, Any]:
    """
    Write a YouTube long-form video script.
    
    Args:
        topic: Video topic
        target_length: Target length in seconds
        tone: Script tone (educational, entertaining, professional)
        key_points: Key points to cover
        include_timestamps: Include timestamp markers
        
    Returns:
        Script with metadata
    """
    key_points_text = "\n".join(f"- {p}" for p in (key_points or []))
    
    prompt = f"""Write a YouTube video script about: {topic}

Target length: {target_length} seconds (~{target_length // 60} minutes)
Tone: {tone}
Key points to cover:
{key_points_text if key_points_text else "- Cover the main aspects of the topic"}

Structure the script with:
1. Hook (first 10 seconds) - grab attention immediately
2. Introduction - what viewers will learn
3. Main content - organized sections with clear transitions
4. Call to action - subscribe, comment, etc.
5. Outro

{"Include [TIMESTAMP: MM:SS] markers for each section." if include_timestamps else ""}

Write in a conversational, engaging style suitable for YouTube."""
    
    script = call_llm(prompt, max_tokens=3000)
    
    return {
        "script": script,
        "format": "youtube_long",
        "metadata": {
            "topic": topic,
            "target_length": target_length,
            "tone": tone,
            "word_count": len(script.split()),
        }
    }


def write_short_script(
    topic: str,
    duration: int = 60,
    style: str = "hook_first",
) -> Dict[str, Any]:
    """
    Write a YouTube Shorts / TikTok / Reels script.
    
    Args:
        topic: Video topic
        duration: Duration in seconds (30 or 60)
        style: Script style (hook_first, story, listicle)
        
    Returns:
        Script with metadata
    """
    prompt = f"""Write a {duration}-second short-form video script about: {topic}

Style: {style}
Platform: YouTube Shorts / TikTok / Reels

Requirements:
- Start with an attention-grabbing hook (first 2 seconds)
- Keep it punchy and fast-paced
- One clear message or takeaway
- End with a call to action or cliffhanger

Format:
[HOOK - 0:00]
(script)

[MAIN - 0:03]
(script)

[CTA - 0:{duration-5}]
(script)"""
    
    script = call_llm(prompt, max_tokens=500)
    
    return {
        "script": script,
        "format": "youtube_short",
        "metadata": {
            "topic": topic,
            "duration": duration,
            "style": style,
        }
    }


def write_thread(
    topic: str,
    num_tweets: int = 7,
    include_hook: bool = True,
) -> Dict[str, Any]:
    """
    Write an X/Twitter thread.
    
    Args:
        topic: Thread topic
        num_tweets: Number of tweets in thread
        include_hook: Include a hook tweet
        
    Returns:
        Thread with metadata
    """
    prompt = f"""Write a Twitter/X thread about: {topic}

Number of tweets: {num_tweets}

Requirements:
- Tweet 1: Strong hook that makes people want to read more
- Each tweet: Max 280 characters
- Use thread numbering (1/, 2/, etc.)
- Include a mix of insights, examples, and actionable tips
- Last tweet: Call to action (follow, retweet, etc.)

Format each tweet on its own line with the number prefix."""
    
    script = call_llm(prompt, max_tokens=1500)
    
    return {
        "script": script,
        "format": "x_thread",
        "metadata": {
            "topic": topic,
            "num_tweets": num_tweets,
        }
    }


def write_linkedin_post(
    topic: str,
    style: str = "thought_leadership",
    include_emoji: bool = True,
) -> Dict[str, Any]:
    """
    Write a LinkedIn post.
    
    Args:
        topic: Post topic
        style: Post style (thought_leadership, story, tips, announcement)
        include_emoji: Include emojis
        
    Returns:
        Post with metadata
    """
    prompt = f"""Write a LinkedIn post about: {topic}

Style: {style}
{"Include relevant emojis to break up text and add visual interest." if include_emoji else "No emojis."}

Requirements:
- Strong opening line (this shows in preview)
- Use line breaks for readability
- Include a personal angle or story
- End with a question to drive engagement
- Keep under 1300 characters for optimal engagement

Format for LinkedIn (short paragraphs, line breaks between sections)."""
    
    script = call_llm(prompt, max_tokens=800)
    
    return {
        "script": script,
        "format": "linkedin",
        "metadata": {
            "topic": topic,
            "style": style,
        }
    }


def write_image_caption(
    topic: str,
    platform: str = "instagram",
    include_hashtags: bool = True,
) -> Dict[str, Any]:
    """
    Write an image caption for social media.
    
    Args:
        topic: Caption topic/context
        platform: Target platform
        include_hashtags: Include hashtags
        
    Returns:
        Caption with metadata
    """
    prompt = f"""Write a {platform} image caption about: {topic}

Requirements:
- Engaging first line (shows in preview)
- Conversational tone
- Call to action
{"- Include 5-10 relevant hashtags at the end" if include_hashtags else ""}

Keep it concise but engaging."""
    
    script = call_llm(prompt, max_tokens=300)
    
    return {
        "script": script,
        "format": "image_caption",
        "metadata": {
            "topic": topic,
            "platform": platform,
        }
    }


def write_script(
    topic: str,
    format: str = "youtube_long",
    **kwargs,
) -> Dict[str, Any]:
    """
    Main entry point for script writing.
    
    Args:
        topic: Content topic
        format: Output format
        **kwargs: Format-specific options
        
    Returns:
        Script with metadata
    """
    format_handlers = {
        "youtube_long": write_youtube_script,
        "youtube_short": write_short_script,
        "x_thread": write_thread,
        "linkedin": write_linkedin_post,
        "image_caption": write_image_caption,
        "hook_30s": lambda t, **kw: write_short_script(t, duration=30, **kw),
    }
    
    handler = format_handlers.get(format, write_youtube_script)
    return handler(topic, **kwargs)
