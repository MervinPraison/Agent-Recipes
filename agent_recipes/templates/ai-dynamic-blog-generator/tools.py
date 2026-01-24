"""
Tools for AI Dynamic Blog Generator Recipe

Slim version - imports from praisonai-tools for DRY.

Provides:
- tavily_search: Via TavilyTool
- check_duplicate: Via WordPressTool
- create_wp_post: Via WordPressTool
- get_current_date: Recipe-specific
"""

import logging
from datetime import date
from typing import Any, Callable, Dict, List, Optional

logger = logging.getLogger(__name__)

# =============================================================================
# Rich console output (optional)
# =============================================================================

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
# Recipe Tools
# =============================================================================

@recipe_tool("get_current_date")
def get_current_date() -> str:
    """Get current date formatted for news queries."""
    today = date.today().strftime("%B %d, %Y")
    debug_print(f"📅 Current date: {today}")
    return today


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
    info_print(f"🔍 Searching: '{query}' (max {max_results} results)")
    
    try:
        # Try praisonai-tools first
        tool = _get_tavily_tool()
        result = tool.search(query=query, max_results=max_results)
        num_results = len(result.get("results", []))
        
        # Check if raw_content is present and count
        has_raw = sum(1 for r in result.get("results", []) if r.get("raw_content"))
        if has_raw > 0:
            success_print(f"Found {num_results} results for: '{query[:50]}...'")
            debug_print(f"   📄 {has_raw} results include full page content")
        else:
            success_print(f"Found {num_results} results for: '{query[:50]}...'")
        
        return result
    except ImportError:
        # Fallback to direct tavily import
        try:
            from tavily import TavilyClient
            import os
            client = TavilyClient(api_key=os.environ.get("TAVILY_API_KEY"))
            result = client.search(
                query=query,
                max_results=max_results,
                search_depth="advanced",
                include_raw_content=True,
                include_answer=True,
                topic="news"
            )
            num_results = len(result.get("results", []))
            success_print(f"Found {num_results} results for: '{query[:50]}...'")
            return result
        except ImportError:
            error_print("Tavily not installed. Run: pip install tavily-python")
            return {"error": "Install with: pip install tavily-python"}
    except Exception as e:
        error_print(f"Tavily search failed: {e}")
        logger.error(f"Tavily search failed: {e}")
        return {"error": str(e)}


@recipe_tool("tavily_extract")
def tavily_extract(url: str) -> Dict[str, Any]:
    """
    Extract full content from a specific URL using Tavily.
    
    Uses TavilyClient directly to get FULL content (no truncation).
    
    Args:
        url: URL to extract content from
        
    Returns:
        Extracted content with title and full text
    """
    info_print(f"📄 Extracting content from: '{url[:60]}...'")
    
    try:
        from tavily import TavilyClient
        import os
        
        api_key = os.environ.get("TAVILY_API_KEY")
        if not api_key:
            error_print("TAVILY_API_KEY not set")
            return {"error": "TAVILY_API_KEY not configured"}
        
        client = TavilyClient(api_key=api_key)
        
        # Extract FULL content - no truncation
        response = client.extract(urls=[url])
        results = response.get("results", [])
        
        if results:
            first = results[0]
            content = first.get("raw_content", "")
            
            # Log content size
            content_len = len(content)
            if content_len > 0:
                success_print(f"Extracted {content_len} chars from URL")
                # Show first 300 chars as preview
                preview = content[:300].replace('\n', ' ')
                debug_print(f"   Preview: {preview}...")
            else:
                warning_print("No content extracted from URL")
                return {"error": "Empty content from URL", "url": url}
            
            # Extract title from URL path
            url_title = url.split("/")[-1].replace("-", " ").title() if "/" in url else "Article"
            
            return {
                "url": first.get("url", url),
                "content": content,  # FULL content, no truncation
                "title": url_title
            }
        
        warning_print("No results from Tavily extract")
        return {"error": "No content returned", "url": url}
        
    except ImportError:
        error_print("Tavily not installed. Run: pip install tavily-python")
        return {"error": "Install with: pip install tavily-python"}
    except Exception as e:
        error_print(f"Tavily extract failed: {e}")
        logger.error(f"Tavily extract failed: {e}")
        return {"error": str(e)}




@recipe_tool("check_duplicate")
def check_duplicate(title: str, content: str = "") -> Dict[str, Any]:
    """
    Check for duplicate content in WordPress using semantic similarity.
    
    Delegates to WordPressTool from praisonai-tools.
    """
    debug_print(f"🔎 Checking: '{title[:50]}...'")
    
    try:
        wp = _get_wp_tool()
        result = wp.check_duplicate(title=title, content=content)
        
        # Rich output for visibility
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
        logger.error(f"Duplicate check failed: {e}")
        return {"error": str(e), "status": "ERROR", "has_duplicates": False}


@recipe_tool("create_wp_post")
def create_wp_post(
    title: str,
    content: str,
    status: str = "draft",
    category: str = "AI",
    author: str = "praison"
) -> Dict[str, Any]:
    """
    Create WordPress post with content validation.
    
    Delegates to WordPressTool from praisonai-tools.
    """
    info_print(f"📝 Creating post: '{title[:50]}...'")
    debug_print(f"   Status: {status}, Category: {category}, Author: {author}")
    
    try:
        wp = _get_wp_tool()
        result = wp.create_post(
            title=title,
            content=content,
            status=status,
            category=category,
            author=author,
            min_word_count=100,
            check_duplicates=True
        )
        
        if result.get("success"):
            post_id = result.get("post_id")
            if HAS_RICH and post_id:
                console.print(Panel(
                    f"[bold white]{title}[/bold white]\n"
                    f"[dim]Post ID:[/dim] [cyan]{post_id}[/cyan]\n"
                    f"[dim]Status:[/dim] [green]{status}[/green]\n"
                    f"[dim]Category:[/dim] {category}",
                    title="✅ POST CREATED",
                    border_style="green"
                ))
            elif post_id:
                success_print(f"Created post ID {post_id}: {title}")
            else:
                success_print(f"Post created: {title}")
        elif result.get("blocked") or result.get("duplicate"):
            warning_print(result.get("message", "Post blocked"))
        else:
            error_print(result.get("error", "Failed to create post"))
        
        return result
    except ImportError as e:
        error_print(str(e))
        return {"error": str(e), "success": False}
    except Exception as e:
        error_print(f"Failed to create post: {e}")
        logger.error(f"Failed to create post: {e}")
        return {"error": str(e), "success": False}


def cleanup():
    """Close connections when done."""
    global _wp_tool
    if _wp_tool:
        try:
            _wp_tool.cleanup()
            info_print("🔌 WordPress connection closed")
        except Exception:
            pass
    _wp_tool = None
