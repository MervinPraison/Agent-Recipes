"""
AI Angle Generator Tools

Generate multiple content angles:
- Controversial takes
- Educational approaches
- Business/ROI focus
- Risk analysis
- Future predictions
- Personal stories
- Comparisons
"""

import logging
import os
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


def call_llm(prompt: str, max_tokens: int = 1500) -> str:
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


def generate_angles(
    topic: str,
    angle_types: Optional[List[str]] = None,
    num_angles: int = 5,
) -> Dict[str, Any]:
    """
    Generate multiple content angles for a topic.
    
    Args:
        topic: The topic to generate angles for
        angle_types: Types of angles to generate
        num_angles: Number of angles to generate
        
    Returns:
        Dictionary with generated angles
    """
    angle_types = angle_types or [
        "controversial", "educational", "business", 
        "risk", "future_prediction"
    ]
    
    angle_descriptions = {
        "controversial": "A bold, contrarian take that challenges conventional wisdom",
        "educational": "An informative, step-by-step teaching approach",
        "business": "Focus on ROI, business impact, and practical applications",
        "risk": "Highlight potential dangers, downsides, or things to watch out for",
        "future_prediction": "Make predictions about where this is heading",
        "personal_story": "Frame through personal experience or case study",
        "comparison": "Compare and contrast with alternatives or competitors",
    }
    
    angles_text = "\n".join(
        f"- {angle}: {angle_descriptions.get(angle, 'Unique perspective')}"
        for angle in angle_types[:num_angles]
    )
    
    prompt = f"""Generate {num_angles} different content angles for this topic: {topic}

For each angle type, provide:
1. A compelling title/headline
2. The main hook or thesis
3. 3 key talking points
4. Target audience

Angle types to generate:
{angles_text}

Format each angle clearly with the type as a header."""
    
    result = call_llm(prompt, max_tokens=2000)
    
    # Parse angles from response
    angles = []
    current_angle = None
    
    for line in result.split("\n"):
        line = line.strip()
        if not line:
            continue
        
        # Check if this is a new angle header
        for angle_type in angle_types:
            if angle_type.lower() in line.lower() and (":" in line or "#" in line):
                if current_angle:
                    angles.append(current_angle)
                current_angle = {
                    "type": angle_type,
                    "content": [],
                }
                break
        
        if current_angle:
            current_angle["content"].append(line)
    
    if current_angle:
        angles.append(current_angle)
    
    # Format angles
    formatted_angles = []
    for angle in angles:
        formatted_angles.append({
            "type": angle["type"],
            "content": "\n".join(angle["content"]),
        })
    
    return {
        "angles": formatted_angles,
        "topic": topic,
        "raw_response": result,
    }


def evaluate_angles(
    angles: List[Dict[str, Any]],
    criteria: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """
    Evaluate and rank generated angles.
    
    Args:
        angles: List of angle dictionaries
        criteria: Evaluation criteria
        
    Returns:
        Ranked angles with scores
    """
    criteria = criteria or ["engagement_potential", "uniqueness", "clarity"]
    
    evaluated = []
    for angle in angles:
        # Simple scoring based on content length and keywords
        content = angle.get("content", "")
        score = 0.5
        
        # Engagement indicators
        engagement_words = ["you", "your", "discover", "secret", "truth", "actually"]
        for word in engagement_words:
            if word in content.lower():
                score += 0.1
        
        # Uniqueness (longer content often more unique)
        if len(content) > 200:
            score += 0.1
        
        evaluated.append({
            **angle,
            "score": min(1.0, score),
        })
    
    # Sort by score
    evaluated.sort(key=lambda x: x["score"], reverse=True)
    
    return {
        "ranked_angles": evaluated,
        "criteria_used": criteria,
    }
