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


@recipe_tool("get_current_date")
def get_current_date() -> str:
    """Get current date formatted for news queries."""
    return date.today().strftime("%B %d, %Y")


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

@recipe_tool("check_duplicate")
def check_duplicate(title: str, content: str = "") -> Dict[str, Any]:
    """
    Check for duplicate content in WordPress using semantic similarity.
    
    Uses embedding-based comparison with persistent caching.
    
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
        from praisonaiwp.ai.duplicate_detector import DuplicateDetector
        
        wp = _get_wp_client()
        detector = DuplicateDetector(
            wp_client=wp,
            threshold=0.7,
            duplicate_threshold=0.95,
            verbose=0
        )
        
        # Index posts (uses persistent cache)
        indexed = detector.index_posts()
        logger.info(f"Indexed {indexed} posts for duplicate check")
        
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
