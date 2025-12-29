"""
Smoke tests for News Intelligence Layer with real API keys.

These tests require:
- OPENAI_API_KEY
- TAVILY_API_KEY (optional, for web search)

Run with: pytest tests/smoke/ --run-smoke
"""

import os
import pytest


pytestmark = pytest.mark.smoke


@pytest.fixture
def skip_if_no_openai():
    """Skip test if OPENAI_API_KEY is not set."""
    if not os.environ.get("OPENAI_API_KEY"):
        pytest.skip("OPENAI_API_KEY not set")


@pytest.fixture
def skip_if_no_tavily():
    """Skip test if TAVILY_API_KEY is not set."""
    if not os.environ.get("TAVILY_API_KEY"):
        pytest.skip("TAVILY_API_KEY not set")


class TestNewsCrawlerSmoke:
    """Smoke tests for AI News Crawler."""
    
    def test_crawl_ai_news(self, skip_if_no_openai, skip_if_no_tavily, templates_dir, temp_output_dir):
        """Test crawling AI news with real API."""
        from agent_recipes.recipe_runtime.core import RecipeConfig
        
        # Import the crawler
        import sys
        sys.path.insert(0, str(templates_dir / "ai-news-crawler"))
        from tools import crawl_ai_news
        
        result = crawl_ai_news(
            sources=["hackernews"],
            max_articles=3,
            output_dir=str(temp_output_dir),
        )
        
        assert result is not None
        assert "articles" in result or isinstance(result, list)


class TestBriefGeneratorSmoke:
    """Smoke tests for Brief Generator."""
    
    def test_generate_daily_brief(self, skip_if_no_openai, templates_dir, temp_output_dir, sample_news_data):
        """Test generating daily brief with real API."""
        import sys
        sys.path.insert(0, str(templates_dir / "ai-brief-generator"))
        from tools import generate_brief
        
        result = generate_brief(
            articles=sample_news_data["articles"],
            format="daily",
            output_dir=str(temp_output_dir),
        )
        
        assert result is not None
        assert "brief" in result or "summary" in result
