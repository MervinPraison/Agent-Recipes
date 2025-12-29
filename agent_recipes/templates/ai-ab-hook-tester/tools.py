"""
AI A/B Hook Tester Tools

Generate test variants and tracking plans for hook optimization.
"""

import logging
import os
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


def call_llm(prompt: str, max_tokens: int = 600) -> str:
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


def generate_test_variants(
    original_hook: str,
    topic: str,
    num_variants: int = 3,
) -> Dict[str, Any]:
    """
    Generate A/B test variants for a hook.
    
    Args:
        original_hook: Original hook text
        topic: Content topic
        num_variants: Number of variants to generate
        
    Returns:
        Dictionary with variants
    """
    prompt = f"""Create {num_variants} A/B test variants for this video hook:

Original Hook: "{original_hook}"
Topic: {topic}

For each variant:
1. Use a different psychological trigger (curiosity, fear, benefit, controversy)
2. Keep it under 15 words
3. Make it distinctly different from the original

Format each variant as:
VARIANT [number]: [hook text]
TRIGGER: [psychological trigger used]
HYPOTHESIS: [why this might perform better]"""
    
    try:
        result = call_llm(prompt, max_tokens=500)
        
        variants = []
        current_variant = {}
        
        for line in result.split("\n"):
            line = line.strip()
            if line.startswith("VARIANT"):
                if current_variant:
                    variants.append(current_variant)
                current_variant = {"text": line.split(":", 1)[-1].strip()}
            elif line.startswith("TRIGGER:"):
                current_variant["trigger"] = line.split(":", 1)[-1].strip()
            elif line.startswith("HYPOTHESIS:"):
                current_variant["hypothesis"] = line.split(":", 1)[-1].strip()
        
        if current_variant:
            variants.append(current_variant)
        
        # Add control (original)
        all_variants = [
            {"text": original_hook, "trigger": "control", "hypothesis": "Original baseline"}
        ] + variants[:num_variants]
        
        return {
            "variants": all_variants,
            "original": original_hook,
            "total_variants": len(all_variants),
        }
    except Exception as e:
        logger.error(f"Error generating variants: {e}")
        return {"error": str(e)}


def create_tracking_plan(
    variants: List[Dict[str, Any]],
    test_duration_days: int = 7,
    metrics: List[str] = None,
) -> Dict[str, Any]:
    """
    Create a tracking plan for A/B test.
    
    Args:
        variants: List of variant dictionaries
        test_duration_days: Test duration in days
        metrics: Metrics to track
        
    Returns:
        Tracking plan
    """
    metrics = metrics or ["ctr", "watch_time", "engagement"]
    
    start_date = datetime.now(timezone.utc)
    end_date = start_date + timedelta(days=test_duration_days)
    
    tracking_plan = {
        "test_id": f"ab_test_{start_date.strftime('%Y%m%d_%H%M%S')}",
        "start_date": start_date.isoformat(),
        "end_date": end_date.isoformat(),
        "duration_days": test_duration_days,
        "variants": [
            {
                "id": f"variant_{i}",
                "text": v.get("text", ""),
                "trigger": v.get("trigger", ""),
            }
            for i, v in enumerate(variants)
        ],
        "metrics": {
            m: {"description": _get_metric_description(m), "target": _get_metric_target(m)}
            for m in metrics
        },
        "sample_size_per_variant": 1000,
        "statistical_significance": 0.95,
        "instructions": [
            "Run each variant for equal time/impressions",
            "Track all specified metrics",
            "Wait for statistical significance before declaring winner",
            "Document any external factors that might affect results",
        ],
    }
    
    return {"tracking_plan": tracking_plan}


def _get_metric_description(metric: str) -> str:
    """Get description for a metric."""
    descriptions = {
        "ctr": "Click-through rate from thumbnail/title",
        "watch_time": "Average watch time in seconds",
        "engagement": "Likes + comments + shares",
        "retention": "Percentage of video watched",
        "conversion": "Desired action completion rate",
    }
    return descriptions.get(metric, metric)


def _get_metric_target(metric: str) -> str:
    """Get target for a metric."""
    targets = {
        "ctr": ">5%",
        "watch_time": ">60 seconds",
        "engagement": ">3%",
        "retention": ">50%",
        "conversion": ">2%",
    }
    return targets.get(metric, "improve over control")
