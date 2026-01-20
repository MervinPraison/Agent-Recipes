"""
Tools for AI Research Pipeline Recipe

Provides:
- tavily_search: AI-powered web search with full content
- check_duplicate: WordPress duplicate detection
- check_duplicates_batch: Batch duplicate checking

Enhanced with Rich console output for debugging visibility.
"""

import logging
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
# Lazy-loaded tool instances
# =============================================================================

_wp_tool = None
_tavily_tool = None


def _get_wp_tool():
    """Lazy load WordPressTool."""
    global _wp_tool
    if _wp_tool is None:
        try:
            from praisonai_tools import WordPressTool
            _wp_tool = WordPressTool(verbose=True)
            info_print("🔌 WordPress tool initialized")
        except ImportError:
            error_print("praisonai-tools[wordpress] not installed")
            raise ImportError("Install with: pip install praisonai-tools[wordpress]")
    return _wp_tool


def _get_tavily_tool():
    """Lazy load TavilyTool."""
    global _tavily_tool
    if _tavily_tool is None:
        try:
            from praisonai_tools import TavilyTool
            _tavily_tool = TavilyTool(search_depth="advanced", include_answer=True)
        except ImportError:
            error_print("praisonai-tools not installed")
            raise ImportError("Install with: pip install praisonai-tools")
    return _tavily_tool


# =============================================================================
# Search Tool
# =============================================================================

@recipe_tool("tavily_search")
def tavily_search(query: str, max_results: int = 10) -> Dict[str, Any]:
    """AI-powered web search using Tavily with full page content."""
    info_print(f"🔍 Searching: '{query}' (max {max_results} results)")
    
    try:
        tool = _get_tavily_tool()
        result = tool.search(query=query, max_results=max_results, include_raw_content=True)
        
        num_results = len(result.get("results", []))
        success_print(f"Found {num_results} results for: '{query[:50]}...'")
        
        has_raw = sum(1 for r in result.get("results", []) if r.get("raw_content"))
        if has_raw:
            debug_print(f"   📄 {has_raw} results include full page content")
        
        return result
    except ImportError:
        error_print("praisonai-tools not installed")
        return {"error": "Install with: pip install praisonai-tools"}
    except Exception as e:
        error_print(f"Tavily search failed: {e}")
        logger.error(f"Tavily search failed: {e}")
        return {"error": str(e)}


# =============================================================================
# Duplicate Detection Tools
# =============================================================================

@recipe_tool("check_duplicate")
def check_duplicate(title: str, content: str = "") -> Dict[str, Any]:
    """Check for duplicate content in WordPress."""
    debug_print(f"🔎 Checking: '{title[:50]}...'")
    
    try:
        wp = _get_wp_tool()
        result = wp.check_duplicate(title=title, content=content)
        
        if result.get("has_duplicates"):
            top = result.get("matches", [{}])[0]
            if HAS_RICH:
                console.print(Panel(
                    f"[bold]{title[:60]}...[/bold]\n"
                    f"[dim]Similar to:[/dim] {top.get('title', '')[:50]}...\n"
                    f"[dim]Similarity:[/dim] [red]{top.get('similarity', 0):.1%}[/red]",
                    title="🔴 DUPLICATE DETECTED",
                    border_style="red"
                ))
            else:
                print(f"🔴 DUPLICATE: '{title}' → similar to '{top.get('title')}'")
        else:
            if HAS_RICH:
                console.print(f"[bold green]🟢 UNIQUE:[/bold green] [white]{title[:70]}...[/white]")
            else:
                print(f"🟢 UNIQUE: '{title}'")
        
        return result
    except ImportError as e:
        error_print(str(e))
        return {"error": str(e), "status": "ERROR", "has_duplicates": False}
    except Exception as e:
        error_print(f"Duplicate check failed: {e}")
        return {"error": str(e), "status": "ERROR", "has_duplicates": False}


@recipe_tool("check_duplicates_batch")
def check_duplicates_batch(items: List[str]) -> Dict[str, Any]:
    """Check multiple items for duplicates."""
    info_print(f"🔎 Batch checking {len(items)} items...")
    
    try:
        wp = _get_wp_tool()
        result = wp.check_duplicates_batch(items=items)
        
        if result.get("has_duplicates"):
            top = result.get("matches", [{}])[0]
            warning_print(f"Found duplicate: '{top.get('title')}' ({top.get('similarity', 0):.1%})")
        else:
            success_print(f"All {len(items)} items are unique")
        
        return result
    except ImportError as e:
        error_print(str(e))
        return {"error": str(e), "status": "ERROR", "has_duplicates": False}
    except Exception as e:
        error_print(f"Batch duplicate check failed: {e}")
        return {"error": str(e), "status": "ERROR", "has_duplicates": False}


def cleanup():
    """Close connections when done."""
    global _wp_tool
    if _wp_tool:
        try:
            _wp_tool.cleanup()
            info_print("🔌 WordPress connection closed")
        except:
            pass
    _wp_tool = None
