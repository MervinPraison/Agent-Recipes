"""
Tools for Research-Post-To-WP Recipe

Provides:
- tavily_search: AI-powered web search
- check_duplicate: Semantic duplicate detection via praisonaiwp
- create_wp_post: WordPress post creation
- get_current_date: Dynamic date provider

Uses praisonaiwp SDK directly (not subprocess) for better performance.

Note: Uses local TOOLS dict for recipe-level tool registry.
The praisonaiagents.tools.registry pattern is for SDK-level tools.
"""

import logging
from datetime import date
from typing import Any, Callable, Dict, List, Optional

logger = logging.getLogger(__name__)

# =============================================================================
# Recipe-Level Tool Registry
# =============================================================================

# Local tools registry for this recipe
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
_detector = None  # Singleton detector for efficiency


@recipe_tool("get_current_date")
def get_current_date() -> str:
    """Get current date formatted for news queries."""
    return date.today().strftime("%B %d, %Y")


@recipe_tool("tavily_search")
def tavily_search(query: str, max_results: int = 10) -> Dict[str, Any]:
    """
    AI-powered web search using Tavily with full page content.
    
    Args:
        query: Search query
        max_results: Maximum results (default: 10)
        
    Returns:
        Search results with answer, sources, and full page content (raw_content)
    """
    try:
        from tavily import TavilyClient
        import os
        client = TavilyClient(api_key=os.environ.get("TAVILY_API_KEY"))
        result = client.search(
            query=query,
            max_results=max_results,
            search_depth="advanced",
            include_raw_content=True,  # Get full page content in markdown
            include_answer=True,
            topic="news"
        )
        return result
    except ImportError:
        return {"error": "Install with: pip install tavily-python"}
    except Exception as e:
        logger.error(f"Tavily search failed: {e}")
        return {"error": str(e)}


@recipe_tool("crawl_url")
def crawl_url(url: str, extract_main_content: bool = True) -> Dict[str, Any]:
    """
    Crawl a URL and extract its content for deep research.
    
    Args:
        url: The URL to crawl
        extract_main_content: Focus on main article content (default: True)
        
    Returns:
        {
            "url": str,
            "title": str,
            "content": str,
            "success": bool
        }
    """
    try:
        from praisonai_tools import Crawl4AITool
        tool = Crawl4AITool()
        result = tool.crawl(url=url)
        
        return {
            "url": url,
            "title": result.get("title", ""),
            "content": result.get("content", result.get("text", "")),
            "success": True
        }
    except ImportError:
        # Fallback to jina reader
        try:
            import requests
            jina_url = f"https://r.jina.ai/{url}"
            resp = requests.get(jina_url, timeout=30)
            return {
                "url": url,
                "title": "",
                "content": resp.text[:10000],  # Limit content
                "success": True
            }
        except Exception as e:
            return {"url": url, "content": "", "success": False, "error": str(e)}
    except Exception as e:
        logger.error(f"Crawl failed for {url}: {e}")
        return {"url": url, "content": "", "success": False, "error": str(e)}


def _get_wp_client():
    """Lazy initialization of WordPress client via SSH."""
    global _wp_client, _ssh_manager
    
    if _wp_client is not None:
        return _wp_client
    
    try:
        from praisonaiwp.core.config import Config
        from praisonaiwp.core.ssh_manager import SSHManager
        from praisonaiwp.core.wp_client import WPClient
        
        config = Config()
        server_config = config.get_server()
        
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
        
        logger.info(f"Connected to WordPress at {server_config['hostname']}")
        return _wp_client
        
    except ImportError:
        raise ImportError("Install with: pip install praisonaiwp")
    except Exception as e:
        logger.error(f"Failed to connect to WordPress: {e}")
        raise

def _ensure_index_sync(wp_client, detector) -> int:
    """
    Ensure embeddings index is in sync with WordPress posts.
    
    Compares WordPress post count with embeddings count.
    If there are new posts, indexes only the new ones (incremental).
    
    Returns:
        Number of indexed posts after sync
    """
    # Get WordPress post count
    all_posts = wp_client.list_posts(post_type='post', post_status='publish', per_page=2000)
    wp_count = len(all_posts)
    
    # Get embeddings count
    embeddings_count = detector.cache.count() if detector.cache else 0
    
    logger.info(f"Sync check: WordPress={wp_count} posts, Embeddings={embeddings_count} indexed")
    
    # If there are new posts, do incremental indexing (don't clear cache)
    if embeddings_count < wp_count:
        missing = wp_count - embeddings_count
        logger.info(f"Found {missing} new posts to index (incremental)")
        # index_posts will only index posts not already in cache
        indexed = detector.index_posts()
        logger.info(f"Total indexed: {indexed} posts")
        return indexed
    
    return embeddings_count


def _get_detector():
    """Get singleton DuplicateDetector instance for efficiency."""
    global _detector
    if _detector is None:
        from praisonaiwp.ai.duplicate_detector import DuplicateDetector
        wp = _get_wp_client()
        _detector = DuplicateDetector(
            wp_client=wp,
            threshold=0.7,
            duplicate_threshold=0.7,
            verbose=0
        )
        # CRITICAL: Ensure embeddings are in sync with WordPress
        indexed = _ensure_index_sync(wp, _detector)
        if indexed == 0:
            indexed = _detector.index_posts()
        logger.info(f"Indexed {indexed} posts for duplicate check (singleton)")
    return _detector


@recipe_tool("check_duplicate")
def check_duplicate(title: str, content: str = "") -> Dict[str, Any]:
    """
    Check for duplicate content in WordPress using semantic similarity.
    
    Uses embedding-based comparison with persistent caching.
    Uses singleton detector for efficiency in parallel workflows.
    
    Args:
        title: Article title to check
        content: Article content (optional, improves accuracy)
        
    Returns:
        {
            "has_duplicates": bool,
            "status": "UNIQUE" | "DUPLICATE",
            "matches": [...],
            "total_checked": int,
            "recommendation": str
        }
    """
    try:
        detector = _get_detector()
        
        # Check for duplicates
        result = detector.check_duplicate(content=content, title=title)
        
        # Build response
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
        else:
            recommendation = "Content appears unique. Safe to publish."
        
        return {
            "has_duplicates": result.has_duplicates,
            "status": status,
            "matches": matches,
            "total_checked": result.total_posts_checked,
            "recommendation": recommendation
        }
        
    except ImportError:
        return {
            "error": "Install with: pip install praisonaiwp[ai]",
            "status": "ERROR",
            "has_duplicates": False
        }
    except Exception as e:
        logger.error(f"Duplicate check failed: {e}")
        return {
            "error": str(e),
            "status": "ERROR",
            "has_duplicates": False
        }


@recipe_tool("check_duplicates_batch")
def check_duplicates_batch(items: List[str]) -> Dict[str, Any]:
    """
    Check multiple items (sentences, paragraphs, titles) for duplicates.
    
    More robust than single-string checking - checks each item independently
    and aggregates results. Use this when you have multiple pieces of content
    to verify against existing posts.
    
    Args:
        items: List of strings to check (sentences, paragraphs, titles)
        
    Returns:
        {
            "has_duplicates": bool,
            "status": "UNIQUE" | "DUPLICATE",
            "matches": [...],
            "total_checked": int,
            "items_checked": int,
            "recommendation": str
        }
    
    Example:
        check_duplicates_batch([
            "OpenAI launches new model",
            "GPT-5 announced at conference",
            "AI breakthrough in 2026"
        ])
    """
    try:
        detector = _get_detector()
        
        # Use batch checking
        result = detector.check_duplicates_batch(items=items, any_match=True)
        
        # Build response
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
        else:
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
        return {
            "error": "Install with: pip install praisonaiwp[ai]",
            "status": "ERROR",
            "has_duplicates": False
        }
    except Exception as e:
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
    """
    Create WordPress post with Gutenberg blocks, category, and author.
    
    Uses praisonaiwp CLI for full feature support including:
    - Automatic Gutenberg block conversion
    - Category assignment
    - Author assignment
    - Deduplication (same title won't be created twice)
    
    Args:
        title: Post title
        content: Post content (markdown/HTML, auto-converted to Gutenberg)
        status: Post status (draft, publish, private)
        category: Category name (default: News)
        author: Author username (default: praison)
        
    Returns:
        {"post_id": int, "status": str, "message": str}
    """
    import subprocess
    import re
    
    # ==========================================================================
    # TITLE BLOCKLIST - Reject invalid titles
    # ==========================================================================
    BLOCKED_TITLE_PATTERNS = [
        "verified",
        "my great article",
        "sample",
        "test article",
        "i'm sorry",
        "i can't assist",
        "as an ai",
        "i cannot",
        "placeholder",
        "example",
        "[theme",
        "[title",
        "[actual",
        "[same content",
        "unchanged content",
    ]
    
    normalized_title = title.strip().lower()
    for pattern in BLOCKED_TITLE_PATTERNS:
        if pattern in normalized_title:
            logger.error(f"BLOCKED TITLE: '{title}' contains '{pattern}'")
            return {
                "post_id": None,
                "status": "rejected",
                "message": f"REJECTED: Title '{title}' is invalid (contains '{pattern}'). Provide a real article title.",
                "success": False,
                "blocked": True
            }
    
    # Must be at least 10 characters for a real title
    if len(title.strip()) < 10:
        logger.error(f"BLOCKED TITLE: '{title}' too short")
        return {
            "post_id": None,
            "status": "rejected", 
            "message": f"REJECTED: Title '{title}' is too short. Provide a descriptive title.",
            "success": False,
            "blocked": True
        }
    
    # Session-level deduplication to prevent multiple posts with same title
    if not hasattr(create_wp_post, '_created_titles'):
        create_wp_post._created_titles = set()
    
    # Check if this title was already created in this session
    normalized_title = title.strip().lower()
    if normalized_title in create_wp_post._created_titles:
        logger.info(f"SESSION DUPLICATE - Skipping: {title}")
        return {
            "post_id": None,
            "status": "skipped",
            "message": f"SKIPPED: '{title}' already created in this session",
            "success": True,
            "duplicate": True
        }
    
    # ==========================================================================
    # MANDATORY DUPLICATE CHECK - Verify against WordPress before posting
    # ==========================================================================
    try:
        dup_result = check_duplicate(title=title, content=content[:500] if content else "")
        if dup_result.get("has_duplicates"):
            top_match = dup_result.get("matches", [{}])[0]
            logger.warning(f"DUPLICATE DETECTED: '{title}' similar to post {top_match.get('post_id')}")
            return {
                "post_id": None,
                "status": "duplicate",
                "message": f"BLOCKED: Content similar to existing post '{top_match.get('title')}' (ID: {top_match.get('post_id')}, similarity: {top_match.get('similarity', 0):.1%})",
                "success": False,
                "duplicate": True,
                "similar_post": top_match
            }
        logger.info(f"Duplicate check passed for: {title}")
    except Exception as e:
        logger.warning(f"Duplicate check failed, proceeding with caution: {e}")
    
    # Add to session immediately to prevent race conditions
    create_wp_post._created_titles.add(normalized_title)
    logger.info(f"CREATING POST: {title}")
    
    try:
        # Convert markdown to HTML first
        # CLI expects HTML for Gutenberg block conversion
        try:
            import markdown
            html_content = markdown.markdown(
                content,
                extensions=['tables', 'fenced_code', 'nl2br']
            )
        except ImportError:
            # Fallback: basic markdown-like conversion
            html_content = content
            # Convert headers
            html_content = re.sub(r'^#### (.+)$', r'<h4>\1</h4>', html_content, flags=re.MULTILINE)
            html_content = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html_content, flags=re.MULTILINE)
            html_content = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html_content, flags=re.MULTILINE)
            html_content = re.sub(r'^# (.+)$', r'<h1>\1</h1>', html_content, flags=re.MULTILINE)
            # Convert bold
            html_content = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html_content)
            # Convert checkmarks to list items
            html_content = re.sub(r'^✅ (.+)$', r'<li>✅ \1</li>', html_content, flags=re.MULTILINE)
            # Convert blockquotes
            html_content = re.sub(r'^> (.+)$', r'<blockquote>\1</blockquote>', html_content, flags=re.MULTILINE)
            # Wrap paragraphs
            lines = html_content.split('\n\n')
            processed = []
            for line in lines:
                if line.strip() and not line.strip().startswith('<'):
                    processed.append(f'<p>{line.strip()}</p>')
                else:
                    processed.append(line)
            html_content = '\n'.join(processed)
        
        # If content already has Gutenberg blocks (<!-- wp:), pass through unchanged
        # Agent is expected to output Gutenberg format directly
        if '<!-- wp:' in content:
            html_content = content
        
        # Build CLI command with content
        cmd = [
            "praisonaiwp", "create", title,
            "--content", html_content,
            "--status", status,
            "--category", category,
            "--author", author
        ]
        
        # Run command
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=120
        )
        
        # Parse output for post ID
        output = result.stdout + result.stderr
        
        # Look for "Created post ID: XXXXX" pattern
        match = re.search(r'post[:\s]+(?:ID[:\s]*)?(\d+)', output, re.IGNORECASE)
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
            # Success but couldn't parse ID
            logger.info(f"Post created but ID not parsed: {output[:200]}")
            return {
                "post_id": None,
                "status": status,
                "message": f"Post created successfully",
                "output": output[:500],
                "success": True
            }
        else:
            logger.error(f"CLI failed: {output}")
            return {
                "error": output[:500],
                "success": False
            }
            
    except subprocess.TimeoutExpired:
        return {"error": "Command timed out after 120s", "success": False}
    except Exception as e:
        logger.error(f"Failed to create post: {e}")
        return {"error": str(e), "success": False}


def cleanup():
    """Close SSH connection when done."""
    global _ssh_manager, _wp_client
    if _ssh_manager:
        try:
            _ssh_manager.__exit__(None, None, None)
            logger.info("SSH connection closed")
        except:
            pass
    _ssh_manager = None
    _wp_client = None
