"""
AI Brief Generator Tools

Tools for generating news briefs:
- Daily briefs
- Weekly roundups
- Executive summaries
- Newsletter formatting
"""

import logging
import os
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


def call_llm(prompt: str, max_tokens: int = 1000) -> str:
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
            "temperature": 0.7,
        },
        timeout=90,
    )
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]


def generate_brief(
    articles: List[Dict[str, Any]],
    format: str = "daily",
    max_articles: int = 10,
    output_dir: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Generate a news brief from articles.
    
    Args:
        articles: List of article dictionaries
        format: Brief format (daily, weekly, executive)
        max_articles: Maximum articles to include
        output_dir: Optional directory to save output
        
    Returns:
        Dictionary with brief content
    """
    if not articles:
        return {"brief": "No articles available.", "summary": "", "highlights": []}
    
    # Limit articles
    articles = articles[:max_articles]
    
    # Format articles for prompt
    articles_text = ""
    for i, article in enumerate(articles, 1):
        articles_text += f"""
{i}. {article.get('title', 'Untitled')}
   Source: {article.get('source', 'Unknown')}
   URL: {article.get('url', '')}
   Content: {article.get('content', '')[:200]}
   Background: {article.get('background', '')}
"""
    
    format_instructions = {
        "daily": "Create a concise daily AI news brief (300-400 words) with key takeaways.",
        "weekly": "Create a comprehensive weekly AI roundup (500-700 words) with trends and analysis.",
        "executive": "Create a brief executive summary (150-200 words) with only the most critical developments.",
    }
    
    prompt = f"""You are an AI news editor creating a {format} brief.

{format_instructions.get(format, format_instructions['daily'])}

Articles to summarize:
{articles_text}

Create a well-structured brief with:
1. Opening hook/headline
2. Key developments (bullet points)
3. Why it matters section
4. What to watch next

Format in Markdown."""
    
    try:
        brief = call_llm(prompt, max_tokens=1500)
    except Exception as e:
        logger.error(f"Error generating brief: {e}")
        brief = "Error generating brief."
    
    # Generate highlights
    highlights = create_highlights(articles[:5])
    
    # Generate executive summary
    summary = _generate_summary(articles[:3])
    
    result = {
        "brief": brief,
        "summary": summary,
        "highlights": highlights,
        "metadata": {
            "format": format,
            "article_count": len(articles),
            "generated_at": datetime.now(timezone.utc).isoformat(),
        }
    }
    
    # Save to file if output_dir specified
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
        
        # Save markdown
        md_path = os.path.join(output_dir, f"brief_{format}.md")
        with open(md_path, "w") as f:
            f.write(f"# AI News Brief - {format.title()}\n\n")
            f.write(f"*Generated: {result['metadata']['generated_at']}*\n\n")
            f.write(brief)
        
        logger.info(f"Saved brief to {md_path}")
    
    return result


def create_highlights(
    articles: List[Dict[str, Any]],
    max_highlights: int = 5,
) -> List[Dict[str, str]]:
    """
    Create highlight snippets from top articles.
    
    Args:
        articles: List of article dictionaries
        max_highlights: Maximum number of highlights
        
    Returns:
        List of highlight dictionaries
    """
    highlights = []
    
    for article in articles[:max_highlights]:
        title = article.get("title", "")
        content = article.get("content", "")[:100]
        url = article.get("url", "")
        
        # Create a one-liner highlight
        if content:
            highlight_text = f"{title}: {content}..."
        else:
            highlight_text = title
        
        highlights.append({
            "title": title,
            "highlight": highlight_text[:200],
            "url": url,
            "source": article.get("source", ""),
        })
    
    return highlights


def _generate_summary(articles: List[Dict[str, Any]]) -> str:
    """Generate a brief executive summary."""
    if not articles:
        return ""
    
    titles = [a.get("title", "") for a in articles[:3]]
    
    prompt = f"""Create a 2-sentence executive summary of these AI news headlines:

{chr(10).join(f'- {t}' for t in titles)}

Summary:"""
    
    try:
        return call_llm(prompt, max_tokens=100).strip()
    except Exception:
        return ""


def format_newsletter(
    brief: str,
    highlights: List[Dict[str, str]],
    template: str = "default",
) -> str:
    """
    Format brief as a newsletter.
    
    Args:
        brief: Main brief content
        highlights: List of highlights
        template: Newsletter template name
        
    Returns:
        Formatted newsletter HTML/Markdown
    """
    newsletter = f"""# 🤖 AI News Brief

{brief}

---

## 📌 Quick Highlights

"""
    
    for h in highlights:
        newsletter += f"- **{h['title']}** - {h['source']}\n"
    
    newsletter += f"""
---

*This brief was generated automatically by PraisonAI.*
"""
    
    return newsletter
