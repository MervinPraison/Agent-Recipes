"""
Tools for AI Topic Gatherer Recipe

Provides:
- tavily_search: AI-powered web search
- get_current_date: Dynamic date provider
"""

import logging
from datetime import date
from typing import Any, Callable, Dict, List, Optional

logger = logging.getLogger(__name__)

# =============================================================================
# Recipe-Level Tool Registry
# =============================================================================

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


# =============================================================================
# Dynamic Date Provider
# =============================================================================

@recipe_tool("today")
def get_current_date() -> str:
    """Get current date in YYYY-MM-DD format."""
    return date.today().isoformat()


# =============================================================================
# Web Search Tool
# =============================================================================

@recipe_tool("tavily_search")
def tavily_search(query: str, max_results: int = 5) -> Dict[str, Any]:
    """
    AI-powered web search using Tavily.
    
    Args:
        query: Search query
        max_results: Maximum results (default: 5)
        
    Returns:
        Search results with answer and sources
    """
    try:
        from praisonai_tools import TavilyTool
        tool = TavilyTool(search_depth="advanced")
        return tool.search(query=query, max_results=max_results)
    except ImportError:
        return {"error": "Install with: pip install praisonai-tools tavily-python"}
    except Exception as e:
        logger.error(f"Tavily search failed: {e}")
        return {"error": str(e)}
