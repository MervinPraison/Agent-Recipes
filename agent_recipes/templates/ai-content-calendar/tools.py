"""
AI Content Calendar Tools

Generate content calendars with:
- Optimal posting times
- Platform-specific scheduling
- Topic distribution
"""

import json
import logging
import os
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


def call_llm(prompt: str, max_tokens: int = 1000) -> str:
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


def generate_calendar(
    topics: List[str],
    duration_days: int = 30,
    platforms: Optional[List[str]] = None,
    posts_per_day: int = 1,
) -> Dict[str, Any]:
    """
    Generate a content calendar.
    
    Args:
        topics: List of content topics
        duration_days: Calendar duration in days
        platforms: Target platforms
        posts_per_day: Posts per day
        
    Returns:
        Dictionary with calendar entries
    """
    platforms = platforms or ["youtube", "x", "linkedin"]
    
    # Optimal posting times by platform
    optimal_times = {
        "youtube": ["09:00", "12:00", "17:00"],
        "x": ["08:00", "12:00", "17:00", "20:00"],
        "linkedin": ["07:30", "12:00", "17:30"],
        "instagram": ["11:00", "14:00", "19:00"],
        "tiktok": ["07:00", "12:00", "19:00", "22:00"],
    }
    
    calendar = []
    start_date = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    
    topic_idx = 0
    
    for day in range(duration_days):
        current_date = start_date + timedelta(days=day)
        
        for post_num in range(posts_per_day):
            # Rotate through topics
            topic = topics[topic_idx % len(topics)]
            topic_idx += 1
            
            # Rotate through platforms
            platform = platforms[post_num % len(platforms)]
            
            # Get optimal time
            times = optimal_times.get(platform, ["12:00"])
            post_time = times[post_num % len(times)]
            
            calendar.append({
                "date": current_date.strftime("%Y-%m-%d"),
                "time": post_time,
                "platform": platform,
                "topic": topic,
                "status": "scheduled",
            })
    
    return {
        "calendar": calendar,
        "stats": {
            "total_posts": len(calendar),
            "duration_days": duration_days,
            "platforms": platforms,
        }
    }


def optimize_schedule(
    calendar: List[Dict[str, Any]],
    avoid_weekends: bool = False,
    peak_hours_only: bool = True,
) -> Dict[str, Any]:
    """
    Optimize a content calendar schedule.
    
    Args:
        calendar: Existing calendar entries
        avoid_weekends: Skip weekend posts
        peak_hours_only: Only schedule during peak hours
        
    Returns:
        Optimized calendar
    """
    optimized = []
    
    for entry in calendar:
        date_str = entry.get("date", "")
        
        try:
            date = datetime.strptime(date_str, "%Y-%m-%d")
            
            # Skip weekends if requested
            if avoid_weekends and date.weekday() >= 5:
                continue
            
            optimized.append(entry)
            
        except ValueError:
            optimized.append(entry)
    
    return {
        "calendar": optimized,
        "removed": len(calendar) - len(optimized),
    }


def export_calendar(
    calendar: List[Dict[str, Any]],
    output_path: str,
    format: str = "json",
) -> Dict[str, Any]:
    """
    Export calendar to file.
    
    Args:
        calendar: Calendar entries
        output_path: Output file path
        format: Export format (json, csv, ical)
        
    Returns:
        Export info
    """
    if format == "json":
        with open(output_path, "w") as f:
            json.dump(calendar, f, indent=2)
    elif format == "csv":
        import csv
        with open(output_path, "w", newline="") as f:
            if calendar:
                writer = csv.DictWriter(f, fieldnames=calendar[0].keys())
                writer.writeheader()
                writer.writerows(calendar)
    
    return {"path": output_path, "format": format, "entries": len(calendar)}
