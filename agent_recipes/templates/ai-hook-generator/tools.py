"""
AI Hook Generator Tools

Generate multiple hook variants for video content:
- Question hooks
- Bold statement hooks
- Statistic hooks
- Story tease hooks
- Controversy hooks
"""

import logging
import os
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


def call_llm(prompt: str, max_tokens: int = 800) -> str:
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
            "temperature": 0.9,
        },
        timeout=60,
    )
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]


def generate_hooks(
    topic: str,
    num_variants: int = 5,
    styles: Optional[List[str]] = None,
    max_words: int = 15,
) -> Dict[str, Any]:
    """
    Generate multiple hook variants for a topic.
    
    Args:
        topic: The video topic
        num_variants: Number of hook variants to generate
        styles: Hook styles to use
        max_words: Maximum words per hook
        
    Returns:
        Dictionary with hook variants
    """
    styles = styles or ["question", "bold_statement", "statistic", "story_tease", "controversy"]
    
    style_examples = {
        "question": "Start with a provocative question",
        "bold_statement": "Make a bold, attention-grabbing claim",
        "statistic": "Lead with a surprising number or stat",
        "story_tease": "Tease an interesting story or outcome",
        "controversy": "Challenge a common belief",
    }
    
    styles_text = "\n".join(
        f"- {s}: {style_examples.get(s, 'Unique approach')}"
        for s in styles[:num_variants]
    )
    
    prompt = f"""Generate {num_variants} different video hooks for this topic: {topic}

Each hook must:
- Be under {max_words} words
- Grab attention in the first 2 seconds
- Make viewers want to keep watching
- Be speakable (sounds natural when said aloud)

Hook styles to use:
{styles_text}

Format each hook as:
[STYLE] Hook text here

Generate {num_variants} hooks:"""
    
    result = call_llm(prompt, max_tokens=600)
    
    # Parse hooks from response
    hooks = []
    for line in result.split("\n"):
        line = line.strip()
        if not line:
            continue
        
        # Try to extract style and hook
        if "[" in line and "]" in line:
            try:
                style_end = line.index("]")
                style = line[1:style_end].strip().lower()
                hook_text = line[style_end + 1:].strip()
                hooks.append({
                    "style": style,
                    "text": hook_text,
                    "word_count": len(hook_text.split()),
                })
            except Exception:
                hooks.append({
                    "style": "unknown",
                    "text": line,
                    "word_count": len(line.split()),
                })
        elif line and not line.startswith("#"):
            hooks.append({
                "style": "unknown",
                "text": line,
                "word_count": len(line.split()),
            })
    
    return {
        "hooks": hooks[:num_variants],
        "topic": topic,
        "total_generated": len(hooks),
    }


def rank_hooks(
    hooks: List[Dict[str, Any]],
) -> Dict[str, Any]:
    """
    Rank hooks by predicted engagement.
    
    Args:
        hooks: List of hook dictionaries
        
    Returns:
        Ranked hooks with scores
    """
    ranked = []
    
    for hook in hooks:
        text = hook.get("text", "").lower()
        score = 0.5
        
        # Engagement indicators
        if "?" in text:
            score += 0.15  # Questions engage
        if "you" in text:
            score += 0.1  # Direct address
        if any(word in text for word in ["secret", "truth", "actually", "never", "always"]):
            score += 0.1  # Power words
        if len(text.split()) <= 10:
            score += 0.1  # Concise is better
        
        # Penalize weak starts
        weak_starts = ["so", "well", "um", "like", "basically"]
        if any(text.startswith(w) for w in weak_starts):
            score -= 0.1
        
        ranked.append({
            **hook,
            "score": round(min(1.0, max(0.0, score)), 2),
        })
    
    ranked.sort(key=lambda x: x["score"], reverse=True)
    
    return {
        "ranked_hooks": ranked,
        "best_hook": ranked[0] if ranked else None,
    }
