"""
Tools for AI Topic Gatherer Recipe

Provides:
- tavily_search: AI-powered web search with full content
- get_current_date: Dynamic date provider

Enhanced with Rich console output for debugging visibility.
"""

import logging
from datetime import date
from typing import Any, Callable, Dict, List, Optional

logger = logging.getLogger(__name__)

# Rich imports for beautiful console output
try:
    from rich.console import Console
    from rich.panel import Panel
    console = Console()
    HAS_RICH = True
except ImportError:
    HAS_RICH = False
    console = None


def debug_print(message: str, style: str = "dim"):
    """Print debug message with optional rich styling."""
    if HAS_RICH:
        console.print(f"[{style}]{message}[/{style}]")
    else:
        print(message)


def success_print(message: str):
    if HAS_RICH:
        console.print(f"[bold green]✅ {message}[/bold green]")
    else:
        print(f"✅ {message}")


def warning_print(message: str):
    if HAS_RICH:
        console.print(f"[bold yellow]⚠️  {message}[/bold yellow]")
    else:
        print(f"⚠️  {message}")


def error_print(message: str):
    if HAS_RICH:
        console.print(f"[bold red]❌ {message}[/bold red]")
    else:
        print(f"❌ {message}")


def info_print(message: str):
    if HAS_RICH:
        console.print(f"[cyan]ℹ️  {message}[/cyan]")
    else:
        print(f"ℹ️  {message}")


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
    today = date.today().isoformat()
    debug_print(f"📅 Current date: {today}")
    return today


# =============================================================================
# Web Search Tool
# =============================================================================

@recipe_tool("tavily_search")
def tavily_search(query: str, max_results: int = 10) -> Dict[str, Any]:
    """
    AI-powered web search using Tavily.
    
    Args:
        query: Search query
        max_results: Maximum results (default: 10)
        
    Returns:
        Search results with answer and sources
    """
    info_print(f"🔍 Searching: '{query}' (max {max_results} results)")
    
    try:
        from praisonai_tools import TavilyTool
        tool = TavilyTool(search_depth="advanced", include_answer=True)
        # Disable raw_content for topic-gatherer to avoid context overflow
        result = tool.search(query=query, max_results=max_results, include_raw_content=False)
        
        num_results = len(result.get("results", []))
        success_print(f"Found {num_results} results for: '{query[:50]}...'")
        
        # Log raw_content availability
        has_raw = sum(1 for r in result.get("results", []) if r.get("raw_content"))
        if has_raw:
            debug_print(f"   📄 {has_raw} results include full page content")
        
        return result
    except ImportError:
        error_print("praisonai-tools not installed. Run: pip install praisonai-tools")
        return {"error": "Install with: pip install praisonai-tools tavily-python"}
    except Exception as e:
        error_print(f"Tavily search failed: {e}")
        logger.error(f"Tavily search failed: {e}")
        return {"error": str(e)}
