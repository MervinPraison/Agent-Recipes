"""
Smoke Tests for AI Skill Generator Recipe with Real APIs.

These tests require:
- OPENAI_API_KEY
- TAVILY_API_KEY (optional, for better search)

Run with: pytest tests/smoke/test_skill_generator_smoke.py --run-smoke -v
"""

import os
import sys
from pathlib import Path

import pytest


pytestmark = pytest.mark.smoke

# Add templates to path
TEMPLATES_DIR = Path(__file__).parent.parent.parent / "agent_recipes" / "templates"


@pytest.fixture
def skip_if_no_openai():
    """Skip test if OPENAI_API_KEY is not set."""
    if not os.environ.get("OPENAI_API_KEY"):
        pytest.skip("OPENAI_API_KEY not set")


@pytest.fixture
def skip_if_no_search():
    """Skip test if no search provider is available."""
    has_tavily = bool(os.environ.get("TAVILY_API_KEY"))
    has_ddg = False
    try:
        from importlib.util import find_spec
        has_ddg = find_spec("duckduckgo_search") is not None
    except ImportError:
        pass
    
    if not has_tavily and not has_ddg:
        pytest.skip("No search provider available (need TAVILY_API_KEY or duckduckgo-search)")


class TestIdentifySourcesSmoke:
    """Smoke tests for identify_sources with real search."""
    
    def test_identify_sources_real_search(self, skip_if_no_search, templates_dir):
        """Test identify_sources with real search API."""
        recipe_dir = templates_dir / "ai-skill-generator"
        sys.path.insert(0, str(recipe_dir))
        
        try:
            import tools
            
            # Use a simple, well-documented topic
            sources = tools.identify_sources("python list comprehension")
            
            # Should return sources (may be less than 8 if search is limited)
            assert isinstance(sources, list)
            assert len(sources) > 0, "Should find at least some sources"
            
            # Each source should have required fields
            for source in sources:
                assert "url" in source
                assert "type" in source
                assert source["type"] in ["docs", "github", "stackoverflow", "blog"]
                assert "title" in source
                
            print(f"\n✅ Found {len(sources)} sources:")
            for s in sources:
                print(f"  [{s['type']}] {s['title'][:50]}...")
                print(f"       {s['url'][:60]}...")
        finally:
            sys.path.remove(str(recipe_dir))


class TestScrapeSourceSmoke:
    """Smoke tests for scrape_source with real crawling."""
    
    def test_scrape_docs_source(self, templates_dir):
        """Test scraping a documentation page."""
        recipe_dir = templates_dir / "ai-skill-generator"
        sys.path.insert(0, str(recipe_dir))
        
        try:
            import tools
            
            # Use a stable, well-known docs page
            result = tools.scrape_source(
                "https://docs.python.org/3/tutorial/datastructures.html",
                "docs"
            )
            
            assert isinstance(result, dict)
            
            if result.get("success"):
                assert len(result.get("content", "")) > 100
                assert result["source_type"] == "docs"
                print(f"\n✅ Scraped {len(result['content'])} chars from docs")
            else:
                print(f"\n⚠️ Scrape failed (may be network issue): {result.get('error')}")
        finally:
            sys.path.remove(str(recipe_dir))
    
    def test_scrape_github_source(self, templates_dir):
        """Test scraping a GitHub page."""
        recipe_dir = templates_dir / "ai-skill-generator"
        sys.path.insert(0, str(recipe_dir))
        
        try:
            import tools
            
            # Use a stable GitHub README
            result = tools.scrape_source(
                "https://github.com/python/cpython",
                "github"
            )
            
            assert isinstance(result, dict)
            assert result["source_type"] == "github"
            
            if result.get("success"):
                print(f"\n✅ Scraped {len(result.get('content', ''))} chars from GitHub")
            else:
                print(f"\n⚠️ GitHub scrape failed: {result.get('error')}")
        finally:
            sys.path.remove(str(recipe_dir))


class TestValidateUrlSmoke:
    """Smoke tests for validate_url."""
    
    def test_validate_valid_url(self, templates_dir):
        """Test validating a known-good URL."""
        recipe_dir = templates_dir / "ai-skill-generator"
        sys.path.insert(0, str(recipe_dir))
        
        try:
            import tools
            
            result = tools.validate_url("https://www.python.org")
            
            assert result["valid"] is True
            assert result["status_code"] == 200
            print(f"\n✅ URL valid: {result}")
        finally:
            sys.path.remove(str(recipe_dir))
    
    def test_validate_invalid_url(self, templates_dir):
        """Test validating a known-bad URL."""
        recipe_dir = templates_dir / "ai-skill-generator"
        sys.path.insert(0, str(recipe_dir))
        
        try:
            import tools
            
            result = tools.validate_url("https://this-domain-does-not-exist-12345.com")
            
            assert result["valid"] is False
            print(f"\n✅ Invalid URL detected: {result.get('error', 'N/A')[:50]}")
        finally:
            sys.path.remove(str(recipe_dir))


class TestFullPipelineSmoke:
    """Smoke test for the full skill generation pipeline."""
    
    def test_full_pipeline_mock_llm(self, skip_if_no_search, templates_dir, tmp_path):
        """Test full pipeline with real search but mocked LLM synthesis."""
        recipe_dir = templates_dir / "ai-skill-generator"
        sys.path.insert(0, str(recipe_dir))
        
        try:
            import tools
            
            # Step 1: Identify sources (real search)
            print("\n📍 Step 1: Identifying sources...")
            sources = tools.identify_sources("python decorators")
            
            assert len(sources) > 0, "Should find sources"
            print(f"   Found {len(sources)} sources")
            
            # Step 2: Scrape first 2 sources (real crawl, limited for speed)
            print("\n📍 Step 2: Scraping sources...")
            scraped = []
            for source in sources[:2]:
                result = tools.scrape_source(source["url"], source["type"])
                if result.get("success"):
                    scraped.append(result)
                    print(f"   ✅ Scraped: {source['url'][:50]}...")
                else:
                    print(f"   ⚠️ Failed: {source['url'][:50]}...")
            
            assert len(scraped) > 0, "Should scrape at least one source"
            
            # Step 3: Format as SKILL.md (no LLM needed)
            print("\n📍 Step 3: Formatting SKILL.md...")
            content = {
                "topic": "Python Decorators",
                "sections": {
                    "quick_start": "```python\n@decorator\ndef func():\n    pass\n```",
                    "core_concepts": f"Extracted from {len(scraped)} sources...",
                    "patterns": "Common patterns from scraped content...",
                    "pitfalls": "Watch out for these issues..."
                }
            }
            
            md = tools.format_skill_md(content)
            
            assert "# Python Decorators" in md
            assert "## Quick Start" in md
            
            # Save to temp file
            output_path = tmp_path / "SKILL-python-decorators.md"
            output_path.write_text(md)
            
            assert output_path.exists()
            print(f"\n✅ SKILL.md saved to: {output_path}")
            print(f"   Size: {len(md)} chars")
            
        finally:
            sys.path.remove(str(recipe_dir))


class TestRecipeExecutionSmoke:
    """Smoke test for recipe execution via praisonai CLI."""
    
    def test_recipe_dry_run(self, skip_if_no_openai, templates_dir):
        """Test recipe dry-run validation."""
        import subprocess
        
        recipe_dir = templates_dir / "ai-skill-generator"
        
        # Try to validate the recipe (dry-run)
        result = subprocess.run(
            ["praisonai", "recipe", "run", str(recipe_dir), "--dry-run", "--var", "topic=test"],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        # Dry-run should succeed (exit 0) or fail gracefully
        print(f"\n📍 Dry-run output:\n{result.stdout[:500] if result.stdout else 'No output'}")
        if result.returncode != 0:
            print(f"⚠️ Dry-run stderr:\n{result.stderr[:500] if result.stderr else 'No stderr'}")
        
        # We just want to verify the command runs without crashing
        assert result.returncode in [0, 1], f"Unexpected exit code: {result.returncode}"
