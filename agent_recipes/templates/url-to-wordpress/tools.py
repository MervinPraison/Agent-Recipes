"""
Tools for this recipe.

Uses native SDK tools that have auto-fallback providers:
- web_crawl: Tavily → Crawl4AI → httpx (auto-detects best available)
- search_web: Tavily → Exa → You.com → DuckDuckGo (auto-detects best available)
"""

# Import native tools with correct function path
# NOTE: Must use full path since praisonaiagents.tools returns module for web_crawl
from praisonaiagents.tools.web_crawl import web_crawl
from praisonaiagents.tools import search_web


# Export tools for use in agents.yaml
TOOLS = [web_crawl, search_web]


def get_all_tools():
    """Get all tools defined in this recipe."""
    return TOOLS
