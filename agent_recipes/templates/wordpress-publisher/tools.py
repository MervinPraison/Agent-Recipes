"""
Tools for WordPress Publisher Recipe

Provides:
- create_wp_post: WordPress post creation with Gutenberg support

Uses praisonaiwp CLI for publishing.
"""

import logging
import subprocess
import re
from typing import Any, Callable, Dict, List, Optional

logger = logging.getLogger(__name__)

# Recipe-Level Tool Registry
TOOLS: Dict[str, Callable] = {}


def recipe_tool(name: str):
    """Decorator to register a tool in the recipe-level registry."""
    def decorator(func: Callable) -> Callable:
        TOOLS[name] = func
        return func
    return decorator


def get_all_tools() -> List[Callable]:
    """Get all registered tool functions for this recipe."""
    return list(TOOLS.values())


def get_tool(name: str) -> Optional[Callable]:
    """Get a specific tool by name."""
    return TOOLS.get(name)


@recipe_tool("create_wp_post")
def create_wp_post(
    title: str,
    content: str,
    status: str = "publish",
    category: str = "News",
    author: str = "praison"
) -> Dict[str, Any]:
    """
    Create WordPress post with Gutenberg blocks, category, and author.
    
    Args:
        title: Post title
        content: Post content (Gutenberg blocks expected)
        status: Post status (draft, publish, private)
        category: Category name (default: News)
        author: Author username (default: praison)
        
    Returns:
        {"post_id": int, "status": str, "message": str}
    """
    # Title blocklist
    BLOCKED_TITLE_PATTERNS = [
        "verified", "my great article", "sample", "test article",
        "i'm sorry", "i can't assist", "as an ai", "i cannot",
        "placeholder", "example", "[theme", "[title", "[actual",
    ]
    
    normalized_title = title.strip().lower()
    for pattern in BLOCKED_TITLE_PATTERNS:
        if pattern in normalized_title:
            logger.error(f"BLOCKED TITLE: '{title}' contains '{pattern}'")
            return {
                "post_id": None,
                "status": "rejected",
                "message": f"REJECTED: Title '{title}' is invalid",
                "success": False,
                "blocked": True
            }
    
    if len(title.strip()) < 10:
        return {
            "post_id": None,
            "status": "rejected",
            "message": f"REJECTED: Title '{title}' too short",
            "success": False,
            "blocked": True
        }
    
    # Session-level deduplication
    if not hasattr(create_wp_post, '_created_titles'):
        create_wp_post._created_titles = set()
    
    if normalized_title in create_wp_post._created_titles:
        return {
            "post_id": None,
            "status": "skipped",
            "message": f"SKIPPED: '{title}' already created in this session",
            "success": True,
            "duplicate": True
        }
    
    create_wp_post._created_titles.add(normalized_title)
    logger.info(f"CREATING POST: {title}")
    
    try:
        # If content has Gutenberg blocks, pass through unchanged
        if '<!-- wp:' in content:
            html_content = content
        else:
            # Basic conversion for non-Gutenberg content
            html_content = content
        
        cmd = [
            "praisonaiwp", "create", title,
            "--content", html_content,
            "--status", status,
            "--category", category,
            "--author", author
        ]
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=120
        )
        
        output = result.stdout + result.stderr
        
        match = re.search(r'post[:\s]+(?:ID[:\s]*)?(\\d+)', output, re.IGNORECASE)
        if match:
            post_id = int(match.group(1))
            logger.info(f"SUCCESS: Created post ID {post_id} - {title}")
            return {
                "post_id": post_id,
                "status": status,
                "category": category,
                "author": author,
                "message": f"Created {status} post with ID: {post_id}",
                "success": True
            }
        elif result.returncode == 0:
            return {
                "post_id": None,
                "status": status,
                "message": "Post created successfully",
                "output": output[:500],
                "success": True
            }
        else:
            logger.error(f"CLI failed: {output}")
            return {"error": output[:500], "success": False}
            
    except subprocess.TimeoutExpired:
        return {"error": "Command timed out after 120s", "success": False}
    except Exception as e:
        logger.error(f"Failed to create post: {e}")
        return {"error": str(e), "success": False}
