"""
Tools for AI Code WordPress Generator Recipe

Provides:
- tavily_search: AI-powered web search
- check_duplicate: Semantic duplicate detection via praisonaiwp
- create_wp_post: WordPress post creation
- get_current_date: Dynamic date provider

Uses praisonaiwp SDK directly (not subprocess) for better performance.
Enhanced with Rich console output for debugging visibility.
"""

import logging
from datetime import date
from typing import Any, Callable, Dict, List, Optional

# Rich imports for beautiful console output
try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    from rich import print as rprint
    console = Console()
    HAS_RICH = True
except ImportError:
    HAS_RICH = False
    console = None

logger = logging.getLogger(__name__)


def debug_print(message: str, style: str = "dim"):
    """Print debug message with optional rich styling."""
    if HAS_RICH:
        console.print(f"[{style}]{message}[/{style}]")
    else:
        print(message)


def success_print(message: str):
    """Print success message."""
    if HAS_RICH:
        console.print(f"[bold green]✅ {message}[/bold green]")
    else:
        print(f"✅ {message}")


def warning_print(message: str):
    """Print warning message."""
    if HAS_RICH:
        console.print(f"[bold yellow]⚠️  {message}[/bold yellow]")
    else:
        print(f"⚠️  {message}")


def error_print(message: str):
    """Print error message."""
    if HAS_RICH:
        console.print(f"[bold red]❌ {message}[/bold red]")
    else:
        print(f"❌ {message}")


def info_print(message: str):
    """Print info message."""
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
# Lazy-initialized WordPress client
# =============================================================================

_wp_client = None
_ssh_manager = None
_detector = None


@recipe_tool("get_current_date")
def get_current_date() -> str:
    """Get current date formatted for news queries."""
    today = date.today().strftime("%B %d, %Y")
    debug_print(f"📅 Current date: {today}")
    return today


@recipe_tool("tavily_search")
def tavily_search(query: str, max_results: int = 3) -> Dict[str, Any]:
    """
    AI-powered web search using Tavily with full page content.
    
    Args:
        query: Search query
        max_results: Maximum results (default: 10)
        
    Returns:
        Search results with answer, sources, and full page content (raw_content)
    """
    info_print(f"🔍 Searching: '{query}' (max {max_results} results)")
    
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


@recipe_tool("crawl_url")
def crawl_url(url: str, extract_main_content: bool = True) -> Dict[str, Any]:
    """
    Crawl a URL and extract its content for deep research.
    """
    info_print(f"🌐 Crawling: {url[:60]}...")
    
    try:
        from praisonai_tools import Crawl4AITool
        tool = Crawl4AITool()
        result = tool.crawl(url=url)
        
        content_len = len(result.get("content", ""))
        success_print(f"Crawled {content_len} chars from: {url[:40]}...")
        
        return {
            "url": url,
            "title": result.get("title", ""),
            "content": result.get("content", result.get("text", "")),
            "success": True
        }
    except ImportError:
        debug_print("Crawl4AI not available, using Jina fallback...")
        try:
            import requests
            jina_url = f"https://r.jina.ai/{url}"
            resp = requests.get(jina_url, timeout=30)
            success_print(f"Jina crawled {len(resp.text)} chars")
            return {
                "url": url,
                "title": "",
                "content": resp.text[:10000],
                "success": True
            }
        except Exception as e:
            error_print(f"Crawl failed: {e}")
            return {"url": url, "content": "", "success": False, "error": str(e)}
    except Exception as e:
        error_print(f"Crawl failed for {url}: {e}")
        logger.error(f"Crawl failed for {url}: {e}")
        return {"url": url, "content": "", "success": False, "error": str(e)}


def _get_wp_client():
    """Lazy initialization of WordPress client via SSH."""
    global _wp_client, _ssh_manager
    
    if _wp_client is not None:
        return _wp_client
    
    info_print("🔌 Connecting to WordPress via SSH...")
    
    try:
        from praisonaiwp.core.config import Config
        from praisonaiwp.core.ssh_manager import SSHManager
        from praisonaiwp.core.wp_client import WPClient
        
        config = Config()
        server_config = config.get_server()
        
        debug_print(f"   Host: {server_config['hostname']}")
        
        _ssh_manager = SSHManager(
            server_config['hostname'],
            server_config['username'],
            server_config['key_file'],
            server_config.get('port', 22)
        )
        _ssh_manager.__enter__()
        
        _wp_client = WPClient(
            _ssh_manager,
            server_config['wp_path'],
            server_config.get('php_bin', 'php'),
            server_config.get('wp_cli', '/usr/local/bin/wp'),
            verify_installation=False
        )
        
        success_print(f"Connected to WordPress at {server_config['hostname']}")
        return _wp_client
        
    except ImportError:
        error_print("praisonaiwp not installed. Run: pip install praisonaiwp")
        raise ImportError("Install with: pip install praisonaiwp")
    except Exception as e:
        error_print(f"Failed to connect to WordPress: {e}")
        logger.error(f"Failed to connect to WordPress: {e}")
        raise


def _ensure_index_sync(wp_client, detector) -> int:
    """Ensure embeddings index is in sync with WordPress posts."""
    debug_print("🔄 Syncing embeddings index with WordPress...")
    
    all_posts = wp_client.list_posts(post_type='post', post_status='publish', per_page=2000)
    wp_count = len(all_posts)
    
    embeddings_count = detector.cache.count() if detector.cache else 0
    
    debug_print(f"   WordPress posts: {wp_count}")
    debug_print(f"   Indexed embeddings: {embeddings_count}")
    
    if embeddings_count < wp_count:
        missing = wp_count - embeddings_count
        info_print(f"📥 Indexing {missing} new posts...")
        indexed = detector.index_posts()
        success_print(f"Indexed {indexed} total posts")
        return indexed
    
    debug_print("   ✓ Index is in sync")
    return embeddings_count


def _get_detector():
    """Get singleton DuplicateDetector instance for efficiency."""
    global _detector
    if _detector is None:
        info_print("🤖 Initializing duplicate detector...")
        
        from praisonaiwp.ai.duplicate_detector import DuplicateDetector
        wp = _get_wp_client()
        _detector = DuplicateDetector(
            wp_client=wp,
            threshold=0.7,
            duplicate_threshold=0.7,
            verbose=0
        )
        indexed = _ensure_index_sync(wp, _detector)
        if indexed == 0:
            indexed = _detector.index_posts()
        success_print(f"Detector ready with {indexed} posts indexed")
    return _detector


@recipe_tool("check_duplicate")
def check_duplicate(title: str, content: str = "") -> Dict[str, Any]:
    """
    Check for duplicate content in WordPress using semantic similarity.
    """
    debug_print(f"🔎 Checking: '{title[:50]}...'")
    
    try:
        detector = _get_detector()
        result = detector.check_duplicate(content=content, title=title)
        
        status = "DUPLICATE" if result.has_duplicates else "UNIQUE"
        matches = [
            {
                "post_id": m.post_id,
                "title": m.title,
                "similarity": round(m.similarity_score, 3),
                "status": m.status
            }
            for m in result.matches
        ]
        
        recommendation = ""
        if result.has_duplicates:
            top = result.matches[0]
            recommendation = f"Similar to existing post '{top.title}' (ID: {top.post_id}). Consider updating instead."
            
            # Rich output for duplicate
            if HAS_RICH:
                console.print(Panel(
                    f"[bold]{title[:60]}...[/bold]\n"
                    f"[dim]Similar to:[/dim] {top.title[:50]}...\n"
                    f"[dim]Similarity:[/dim] [red]{top.similarity_score:.1%}[/red]",
                    title="🔴 DUPLICATE DETECTED",
                    border_style="red"
                ))
            else:
                print(f"🔴 DUPLICATE: '{title}' → similar to '{top.title}' ({top.similarity_score:.1%})")
        else:
            recommendation = "Content appears unique. Safe to publish."
            
            # Rich output for unique
            if HAS_RICH:
                console.print(f"[bold green]🟢 UNIQUE:[/bold green] [white]{title[:70]}...[/white]")
            else:
                print(f"🟢 UNIQUE: '{title}'")
        
        return {
            "has_duplicates": result.has_duplicates,
            "status": status,
            "matches": matches,
            "total_checked": result.total_posts_checked,
            "recommendation": recommendation
        }
        
    except ImportError:
        error_print("praisonaiwp[ai] not installed")
        return {
            "error": "Install with: pip install praisonaiwp[ai]",
            "status": "ERROR",
            "has_duplicates": False
        }
    except Exception as e:
        error_print(f"Duplicate check failed: {e}")
        logger.error(f"Duplicate check failed: {e}")
        return {
            "error": str(e),
            "status": "ERROR",
            "has_duplicates": False
        }


@recipe_tool("check_duplicates_batch")
def check_duplicates_batch(items: List[str]) -> Dict[str, Any]:
    """Check multiple items for duplicates."""
    info_print(f"🔎 Batch checking {len(items)} items...")
    
    try:
        detector = _get_detector()
        result = detector.check_duplicates_batch(items=items, any_match=True)
        
        status = "DUPLICATE" if result.has_duplicates else "UNIQUE"
        matches = [
            {
                "post_id": m.post_id,
                "title": m.title,
                "similarity": round(m.similarity_score, 3),
                "status": m.status
            }
            for m in result.matches
        ]
        
        if result.has_duplicates:
            top = result.matches[0]
            warning_print(f"Found duplicate: '{top.title}' ({top.similarity_score:.1%})")
            recommendation = f"Similar to existing post '{top.title}' (ID: {top.post_id})."
        else:
            success_print(f"All {len(items)} items are unique")
            recommendation = "All content appears unique. Safe to publish."
        
        return {
            "has_duplicates": result.has_duplicates,
            "status": status,
            "matches": matches,
            "total_checked": result.total_posts_checked,
            "items_checked": len(items),
            "recommendation": recommendation
        }
        
    except ImportError:
        error_print("praisonaiwp[ai] not installed")
        return {
            "error": "Install with: pip install praisonaiwp[ai]",
            "status": "ERROR",
            "has_duplicates": False
        }
    except Exception as e:
        error_print(f"Batch duplicate check failed: {e}")
        logger.error(f"Batch duplicate check failed: {e}")
        return {
            "error": str(e),
            "status": "ERROR",
            "has_duplicates": False
        }


@recipe_tool("create_wp_post")
def create_wp_post(
    title: str,
    content: str,
    status: str = "draft",
    category: str = "News",
    author: str = "praison"
) -> Dict[str, Any]:
    """Create WordPress post with Gutenberg blocks, category, and author."""
    import subprocess
    import re
    
    info_print(f"📝 Creating post: '{title[:50]}...'")
    debug_print(f"   Status: {status}, Category: {category}, Author: {author}")
    
    # Title blocklist
    BLOCKED_TITLE_PATTERNS = [
        "verified", "my great article", "sample", "test article",
        "i'm sorry", "i can't assist", "as an ai", "i cannot",
        "placeholder", "example", "[theme", "[title", "[actual",
        "[same content", "unchanged content",
    ]
    
    normalized_title = title.strip().lower()
    for pattern in BLOCKED_TITLE_PATTERNS:
        if pattern in normalized_title:
            error_print(f"BLOCKED: Title contains '{pattern}'")
            return {
                "post_id": None,
                "status": "rejected",
                "message": f"REJECTED: Title '{title}' is invalid",
                "success": False,
                "blocked": True
            }
    
    if len(title.strip()) < 10:
        error_print(f"BLOCKED: Title too short ({len(title)} chars)")
        return {
            "post_id": None,
            "status": "rejected",
            "message": f"REJECTED: Title too short",
            "success": False,
            "blocked": True
        }
    
    # Session deduplication
    if not hasattr(create_wp_post, '_created_titles'):
        create_wp_post._created_titles = set()
    
    if normalized_title in create_wp_post._created_titles:
        warning_print(f"SESSION DUPLICATE: Already created this session")
        return {
            "post_id": None,
            "status": "skipped",
            "message": f"SKIPPED: Already created in this session",
            "success": True,
            "duplicate": True
        }
    
    # Mandatory duplicate check
    debug_print("   Running duplicate check...")
    try:
        dup_result = check_duplicate(title=title, content=content[:500] if content else "")
        if dup_result.get("has_duplicates"):
            top_match = dup_result.get("matches", [{}])[0]
            warning_print(f"DUPLICATE: Similar to post {top_match.get('post_id')}")
            return {
                "post_id": None,
                "status": "duplicate",
                "message": f"BLOCKED: Similar to '{top_match.get('title')}'",
                "success": False,
                "duplicate": True,
                "similar_post": top_match
            }
        debug_print("   ✓ Duplicate check passed")
    except Exception as e:
        warning_print(f"Duplicate check failed, proceeding: {e}")
    
    # Add to session
    create_wp_post._created_titles.add(normalized_title)
    
    try:
        # Convert markdown to HTML
        try:
            import markdown
            html_content = markdown.markdown(
                content,
                extensions=['tables', 'fenced_code', 'nl2br']
            )
        except ImportError:
            html_content = content
            html_content = re.sub(r'^#### (.+)$', r'<h4>\1</h4>', html_content, flags=re.MULTILINE)
            html_content = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html_content, flags=re.MULTILINE)
            html_content = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html_content, flags=re.MULTILINE)
            html_content = re.sub(r'^# (.+)$', r'<h1>\1</h1>', html_content, flags=re.MULTILINE)
            html_content = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html_content)
        
        # Pass through Gutenberg blocks unchanged
        if '<!-- wp:' in content:
            html_content = content
        
        debug_print(f"   Content size: {len(html_content)} chars")
        
        cmd = [
            "praisonaiwp", "create", title,
            "--content", html_content,
            "--status", status,
            "--category", category,
            "--author", author
        ]
        
        info_print("   📤 Uploading to WordPress...")
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        
        output = result.stdout + result.stderr
        match = re.search(r'post[:\s]+(?:ID[:\s]*)?(\\d+)', output, re.IGNORECASE)
        
        if match:
            post_id = int(match.group(1))
            if HAS_RICH:
                console.print(Panel(
                    f"[bold white]{title}[/bold white]\n"
                    f"[dim]Post ID:[/dim] [cyan]{post_id}[/cyan]\n"
                    f"[dim]Status:[/dim] [green]{status}[/green]\n"
                    f"[dim]Category:[/dim] {category}",
                    title="✅ POST CREATED",
                    border_style="green"
                ))
            else:
                success_print(f"Created post ID {post_id}: {title}")
            return {
                "post_id": post_id,
                "status": status,
                "category": category,
                "author": author,
                "message": f"Created {status} post with ID: {post_id}",
                "success": True
            }
        elif result.returncode == 0:
            success_print(f"Post created (ID not parsed)")
            return {
                "post_id": None,
                "status": status,
                "message": f"Post created successfully",
                "output": output[:500],
                "success": True
            }
        else:
            error_print(f"CLI failed: {output[:200]}")
            return {"error": output[:500], "success": False}
            
    except subprocess.TimeoutExpired:
        error_print("Command timed out after 120s")
        return {"error": "Command timed out after 120s", "success": False}
    except Exception as e:
        error_print(f"Failed to create post: {e}")
        logger.error(f"Failed to create post: {e}")
        return {"error": str(e), "success": False}


def cleanup():
    """Close SSH connection when done."""
    global _ssh_manager, _wp_client
    if _ssh_manager:
        try:
            _ssh_manager.__exit__(None, None, None)
            info_print("🔌 SSH connection closed")
        except:
            pass
    _ssh_manager = None
    _wp_client = None
