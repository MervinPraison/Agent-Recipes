"""
Tools for AI Skill Generator Recipe.

Custom tools for generating comprehensive SKILL.md files from multiple web sources.
Replicates the TinySkills approach: identify sources → parallel scrape → synthesize.

Tools:
- identify_sources: Use AI to find 8 relevant URLs (2 per source type)
- scrape_source: Extract content with type-specific prompts
- format_skill_md: Format content as Anthropic SKILL.md
- validate_url: Check if a URL is accessible

Source Types:
- docs: Official documentation, API references
- github: Code repositories, examples
- stackoverflow: Q&A, common problems and solutions
- blog: Tutorials, explanations, guides
"""

import logging
from typing import Any, Callable, Dict, List, Optional

logger = logging.getLogger(__name__)

# =============================================================================
# Constants
# =============================================================================

SOURCE_TYPES = ["docs", "github", "stackoverflow", "blog"]
SOURCES_PER_TYPE = 2
TOTAL_SOURCES = len(SOURCE_TYPES) * SOURCES_PER_TYPE  # 8

# =============================================================================
# Tool Registry
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
# Extraction Prompts (Source-Type Specific)
# =============================================================================

EXTRACTION_PROMPTS = {
    "docs": """Extract from this documentation page:
- API signatures and parameters
- Code examples and usage patterns
- Configuration options
- Best practices mentioned
- Version-specific information
Focus on practical, actionable information for developers.""",

    "github": """Extract from this GitHub repository/code:
- Code patterns and implementation details
- Project structure and architecture
- Dependencies and requirements
- README highlights
- Key functions/classes and their purposes
Focus on reusable code patterns and implementation approaches.""",

    "stackoverflow": """Extract from this StackOverflow Q&A:
- The core problem being solved
- The accepted/best answer solution
- Alternative approaches mentioned
- Common pitfalls warned about
- Code snippets that work
Focus on practical solutions to real problems.""",

    "blog": """Extract from this blog/tutorial:
- Step-by-step instructions
- Explanations of concepts
- Code examples with context
- Tips and tricks mentioned
- Real-world use cases
Focus on educational content and practical guidance.""",

    "default": """Extract the most relevant technical content:
- Key concepts and definitions
- Code examples if present
- Practical guidance
- Important warnings or notes
Focus on information useful for learning this topic."""
}


def get_extraction_prompt(source_type: str) -> str:
    """
    Get the extraction prompt for a specific source type.
    
    Args:
        source_type: One of 'docs', 'github', 'stackoverflow', 'blog'
        
    Returns:
        Extraction prompt string tailored to the source type
    """
    return EXTRACTION_PROMPTS.get(source_type, EXTRACTION_PROMPTS["default"])


# =============================================================================
# Internal Helper Functions
# =============================================================================

def _get_search_tool():
    """Lazy load search_web from praisonaiagents."""
    try:
        from praisonaiagents.tools import search_web
        return search_web
    except ImportError:
        logger.warning("praisonaiagents not installed, using fallback search")
        return _fallback_search


def _fallback_search(query: str, max_results: int = 10) -> List[Dict[str, Any]]:
    """Fallback search using DuckDuckGo if praisonaiagents not available."""
    try:
        from ddgs import DDGS
        ddgs = DDGS()
        # ddgs v8+ uses positional query argument
        results = list(ddgs.text(query, max_results=max_results))
        return [
            {"url": r.get("href", ""), "title": r.get("title", ""), "snippet": r.get("body", "")}
            for r in results
        ]
    except ImportError:
        # Try older duckduckgo_search package
        try:
            from duckduckgo_search import DDGS as OldDDGS
            ddgs = OldDDGS()
            results = list(ddgs.text(query, max_results=max_results))
            return [
                {"url": r.get("href", ""), "title": r.get("title", ""), "snippet": r.get("body", "")}
                for r in results
            ]
        except ImportError:
            logger.error("No search provider available. Install ddgs or duckduckgo-search.")
            return []
    except Exception as e:
        logger.error(f"Fallback search failed: {e}")
        return []


def _get_crawl_tool():
    """Lazy load web_crawl from praisonaiagents."""
    try:
        from praisonaiagents.tools.web_crawl import web_crawl
        return web_crawl
    except ImportError:
        logger.warning("praisonaiagents web_crawl not available, using fallback")
        return _fallback_crawl


def _fallback_crawl(url: str) -> Dict[str, Any]:
    """Fallback crawl using requests if praisonaiagents not available."""
    try:
        import requests
        from bs4 import BeautifulSoup
        
        resp = requests.get(url, timeout=30, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(resp.text, "html.parser")
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        
        text = soup.get_text(separator="\n", strip=True)
        title = soup.title.string if soup.title else ""
        
        return {"url": url, "content": text[:10000], "title": title, "success": True}
    except Exception as e:
        logger.error(f"Fallback crawl failed: {e}")
        return {"url": url, "content": "", "title": "", "success": False, "error": str(e)}


def _search_for_topic(topic: str, max_results: int = 20) -> List[Dict[str, Any]]:
    """
    Search for URLs related to a topic.
    
    Args:
        topic: The topic to search for
        max_results: Maximum number of results to return
        
    Returns:
        List of search results with url, title, snippet
    """
    search = _get_search_tool()
    
    # Search with different queries to get diverse results
    queries = [
        f"{topic} documentation tutorial",
        f"{topic} github examples",
        f"{topic} stackoverflow best practices",
        f"{topic} blog tutorial guide"
    ]
    
    all_results = []
    seen_urls = set()
    
    for query in queries:
        try:
            results = search(query, max_results=max_results // len(queries))
            if isinstance(results, list):
                for r in results:
                    url = r.get("url", r.get("href", ""))
                    if url and url not in seen_urls:
                        seen_urls.add(url)
                        all_results.append({
                            "url": url,
                            "title": r.get("title", ""),
                            "snippet": r.get("snippet", r.get("body", r.get("content", "")))
                        })
        except Exception as e:
            logger.warning(f"Search failed for '{query}': {e}")
    
    return all_results[:max_results]


def _categorize_url(url: str, title: str = "", snippet: str = "") -> str:
    """
    Categorize a URL into one of the source types.
    
    Args:
        url: The URL to categorize
        title: Optional title for context
        snippet: Optional snippet for context
        
    Returns:
        Source type: 'docs', 'github', 'stackoverflow', or 'blog'
    """
    url_lower = url.lower()
    title_lower = (title or "").lower()
    
    # GitHub detection
    if "github.com" in url_lower or "gitlab.com" in url_lower:
        return "github"
    
    # StackOverflow detection
    if "stackoverflow.com" in url_lower or "stackexchange.com" in url_lower:
        return "stackoverflow"
    
    # Documentation detection (common doc sites and patterns)
    doc_patterns = [
        "docs.", ".docs.", "/docs/", "/documentation/", "/api/", "/reference/",
        "developer.", "devdocs.", "readthedocs.", ".io/docs", "/guide/"
    ]
    if any(p in url_lower for p in doc_patterns):
        return "docs"
    
    # Official docs by domain
    official_doc_domains = [
        "reactjs.org", "react.dev", "vuejs.org", "angular.io", "python.org", 
        "nodejs.org", "developer.mozilla.org", "docs.microsoft.com", 
        "cloud.google.com/docs", "aws.amazon.com/documentation", 
        "kubernetes.io/docs", "typescriptlang.org", "rust-lang.org"
    ]
    if any(d in url_lower for d in official_doc_domains):
        return "docs"
    
    # Blog detection
    blog_patterns = [
        "blog.", "/blog/", "medium.com", "dev.to", "hashnode.", "substack.",
        "wordpress.", "blogger.", "tumblr.", "/posts/", "/articles/"
    ]
    if any(p in url_lower for p in blog_patterns):
        return "blog"
    
    # Default to blog for tutorials and articles
    tutorial_keywords = ["tutorial", "guide", "how to", "introduction", "getting started"]
    if any(k in title_lower for k in tutorial_keywords):
        return "blog"
    
    # Default fallback
    return "blog"


def _categorize_urls(search_results: List[Dict[str, Any]]) -> List[Dict[str, str]]:
    """
    Categorize search results and select 2 per source type.
    
    Args:
        search_results: List of search results with url, title, snippet
        
    Returns:
        List of 8 categorized sources with url, type, title, reason
    """
    categorized = {t: [] for t in SOURCE_TYPES}
    
    # First pass: categorize all URLs
    for result in search_results:
        url = result.get("url", "")
        title = result.get("title", "")
        snippet = result.get("snippet", "")
        
        if not url:
            continue
        
        source_type = _categorize_url(url, title, snippet)
        
        if len(categorized[source_type]) < SOURCES_PER_TYPE:
            categorized[source_type].append({
                "url": url,
                "type": source_type,
                "title": title or url.split("/")[-1],
                "reason": _generate_reason(source_type, title, snippet)
            })
    
    # Flatten and ensure we have sources
    selected = []
    for source_type in SOURCE_TYPES:
        sources = categorized[source_type]
        selected.extend(sources[:SOURCES_PER_TYPE])
    
    # If we don't have enough, fill with remaining results
    if len(selected) < TOTAL_SOURCES:
        for result in search_results:
            if len(selected) >= TOTAL_SOURCES:
                break
            url = result.get("url", "")
            if url and not any(s["url"] == url for s in selected):
                source_type = _categorize_url(url)
                selected.append({
                    "url": url,
                    "type": source_type,
                    "title": result.get("title", url),
                    "reason": "Additional relevant source"
                })
    
    return selected[:TOTAL_SOURCES]


def _generate_reason(source_type: str, title: str, snippet: str) -> str:
    """Generate a reason for why this source was selected."""
    reasons = {
        "docs": "Official documentation with API reference and examples",
        "github": "Source code and implementation examples",
        "stackoverflow": "Community Q&A with practical solutions",
        "blog": "Tutorial with step-by-step explanations"
    }
    base_reason = reasons.get(source_type, "Relevant learning resource")
    
    if title:
        return f"{base_reason}: {title[:50]}"
    return base_reason


def _fetch_url_content(url: str) -> Dict[str, Any]:
    """
    Fetch content from a URL using available crawl tools.
    
    Args:
        url: URL to fetch
        
    Returns:
        Dict with url, content, title, success
    """
    crawl = _get_crawl_tool()
    
    try:
        result = crawl(url)
        
        if isinstance(result, dict):
            return {
                "url": url,
                "content": result.get("content", result.get("text", "")),
                "title": result.get("title", ""),
                "success": result.get("success", True) if "success" in result else bool(result.get("content"))
            }
        elif isinstance(result, str):
            return {"url": url, "content": result, "title": "", "success": True}
        else:
            return {"url": url, "content": str(result), "title": "", "success": True}
    except Exception as e:
        logger.error(f"Failed to fetch {url}: {e}")
        return {"url": url, "content": "", "title": "", "success": False, "error": str(e)}


# =============================================================================
# Main Tools (Exported)
# =============================================================================

@recipe_tool("identify_sources")
def identify_sources(topic: str, sources_per_type: int = 2) -> List[Dict[str, str]]:
    """
    Use AI-powered search to identify relevant learning sources for a topic.
    
    Finds 8 URLs total: 2 documentation, 2 GitHub, 2 StackOverflow, 2 blog/tutorial.
    
    Args:
        topic: The topic to find sources for (e.g., "react hooks", "kubernetes pods")
        sources_per_type: Number of sources per type (default: 2)
        
    Returns:
        List of 8 source dicts, each with:
        - url: The source URL
        - type: One of 'docs', 'github', 'stackoverflow', 'blog'
        - title: Title of the source
        - reason: Why this source was selected
        
    Example:
        >>> sources = identify_sources("react hooks")
        >>> len(sources)
        8
        >>> sources[0]
        {'url': 'https://react.dev/reference/react/hooks', 'type': 'docs', 
         'title': 'React Hooks Reference', 'reason': 'Official documentation...'}
    """
    logger.info(f"Identifying sources for topic: {topic}")
    
    # Search for relevant URLs
    search_results = _search_for_topic(topic, max_results=30)
    
    if not search_results:
        logger.warning(f"No search results found for '{topic}'")
        return []
    
    # Categorize and select 2 per type
    sources = _categorize_urls(search_results)
    
    logger.info(f"Identified {len(sources)} sources for '{topic}'")
    return sources


@recipe_tool("scrape_source")
def scrape_source(url: str, source_type: str = "blog") -> Dict[str, Any]:
    """
    Scrape content from a URL with type-specific extraction.
    
    Uses different extraction strategies based on source type:
    - docs: Focus on API reference, parameters, examples
    - github: Focus on code patterns, implementation
    - stackoverflow: Focus on problems and solutions
    - blog: Focus on tutorials and explanations
    
    Args:
        url: The URL to scrape
        source_type: One of 'docs', 'github', 'stackoverflow', 'blog'
        
    Returns:
        Dict with:
        - url: The scraped URL
        - content: Raw content from the page
        - extracted: Key information extracted based on source type
        - source_type: The type used for extraction
        - success: Whether scraping succeeded
        
    Example:
        >>> result = scrape_source("https://react.dev/reference/react/useState", "docs")
        >>> result['success']
        True
        >>> 'useState' in result['content']
        True
    """
    logger.info(f"Scraping {source_type} source: {url}")
    
    # Get the extraction prompt for this source type
    extraction_prompt = get_extraction_prompt(source_type)
    
    # Fetch the content
    fetch_result = _fetch_url_content(url)
    
    if not fetch_result.get("success"):
        return {
            "url": url,
            "content": "",
            "extracted": "",
            "source_type": source_type,
            "success": False,
            "error": fetch_result.get("error", "Failed to fetch URL")
        }
    
    content = fetch_result.get("content", "")
    
    # Truncate very long content
    max_content_length = 15000
    if len(content) > max_content_length:
        content = content[:max_content_length] + "\n\n[Content truncated...]"
    
    return {
        "url": url,
        "content": content,
        "extracted": content,
        "source_type": source_type,
        "extraction_prompt": extraction_prompt,
        "success": True
    }


@recipe_tool("format_skill_md")
def format_skill_md(content: Dict[str, Any]) -> str:
    """
    Format extracted content as a SKILL.md file following Anthropic's format.
    
    The SKILL.md format includes:
    - Quick Start: Get up and running in minutes
    - Core Concepts: Essential knowledge
    - Essential Patterns: Common usage patterns
    - Common Pitfalls: Mistakes to avoid
    
    Args:
        content: Dict with:
            - topic: The skill topic
            - sections: Dict with quick_start, core_concepts, patterns, pitfalls
            
    Returns:
        Formatted markdown string ready to save as SKILL.md
        
    Example:
        >>> content = {
        ...     "topic": "React Hooks",
        ...     "sections": {
        ...         "quick_start": "npm install react",
        ...         "core_concepts": "Hooks let you use state...",
        ...         "patterns": "useEffect for side effects...",
        ...         "pitfalls": "Don't call hooks conditionally"
        ...     }
        ... }
        >>> md = format_skill_md(content)
        >>> "# React Hooks" in md
        True
    """
    topic = content.get("topic", "Unknown Topic")
    sections = content.get("sections", {})
    
    # Build the SKILL.md content
    md_parts = [
        f"# {topic}",
        "",
        f"> A comprehensive skill guide for {topic}",
        "",
        "---",
        "",
        "## Quick Start",
        "",
        sections.get("quick_start", "_No quick start information available._"),
        "",
        "---",
        "",
        "## Core Concepts",
        "",
        sections.get("core_concepts", "_No core concepts information available._"),
        "",
        "---",
        "",
        "## Essential Patterns",
        "",
        sections.get("patterns", "_No patterns information available._"),
        "",
        "---",
        "",
        "## Common Pitfalls",
        "",
        sections.get("pitfalls", "_No pitfalls information available._"),
        "",
        "---",
        "",
        "## Sources",
        "",
        "_Generated from multiple web sources using AI Skill Generator._",
        ""
    ]
    
    return "\n".join(md_parts)


@recipe_tool("validate_url")
def validate_url(url: str) -> Dict[str, Any]:
    """
    Validate that a URL is accessible and returns content.
    
    Args:
        url: URL to validate
        
    Returns:
        Dict with url, valid (bool), status_code, error (if any)
    """
    try:
        import requests
        resp = requests.head(url, timeout=10, allow_redirects=True, 
                            headers={"User-Agent": "Mozilla/5.0"})
        return {
            "url": url,
            "valid": resp.status_code < 400,
            "status_code": resp.status_code,
            "final_url": resp.url
        }
    except Exception as e:
        return {
            "url": url,
            "valid": False,
            "error": str(e)
        }


# =============================================================================
# Exports
# =============================================================================

__all__ = [
    "SOURCE_TYPES",
    "SOURCES_PER_TYPE", 
    "TOTAL_SOURCES",
    "get_extraction_prompt",
    "identify_sources",
    "scrape_source",
    "format_skill_md",
    "validate_url",
    "get_all_tools",
    "get_tool",
    "TOOLS"
]
