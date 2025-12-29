"""
Unit tests for News Intelligence Layer recipes.

TDD: These tests are written first and should FAIL until implementation is complete.
"""

import yaml


class TestNewsCrawler:
    """Tests for AI News Crawler recipe."""
    
    def test_template_exists(self, templates_dir):
        """Test that ai-news-crawler template exists."""
        template_path = templates_dir / "ai-news-crawler"
        assert template_path.exists(), "ai-news-crawler template should exist"
    
    def test_template_has_recipe_yaml(self, templates_dir):
        """Test that template has recipe.yaml."""
        recipe_path = templates_dir / "ai-news-crawler" / "recipe.yaml"
        assert recipe_path.exists(), "recipe.yaml should exist"
    
    def test_template_has_tools(self, templates_dir):
        """Test that template has tools.py."""
        tools_path = templates_dir / "ai-news-crawler" / "tools.py"
        assert tools_path.exists(), "tools.py should exist"
    
    def test_crawler_sources_config(self, templates_dir):
        """Test that crawler has configurable sources."""
        import yaml
        recipe_path = templates_dir / "ai-news-crawler" / "recipe.yaml"
        with open(recipe_path) as f:
            recipe = yaml.safe_load(f)
        
        assert "config" in recipe, "Recipe should have config section"
        assert "sources" in recipe.get("config", {}), "Config should have sources"


class TestNewsDeduper:
    """Tests for News Deduper + Topic Clustering recipe."""
    
    def test_template_exists(self, templates_dir):
        """Test that ai-news-deduper template exists."""
        template_path = templates_dir / "ai-news-deduper"
        assert template_path.exists(), "ai-news-deduper template should exist"
    
    def test_deduplication_logic(self, templates_dir):
        """Test that deduper has deduplication logic."""
        tools_path = templates_dir / "ai-news-deduper" / "tools.py"
        assert tools_path.exists()
        
        content = tools_path.read_text()
        assert "deduplicate" in content.lower() or "dedup" in content.lower(), \
            "tools.py should contain deduplication logic"
    
    def test_clustering_logic(self, templates_dir):
        """Test that deduper has topic clustering."""
        tools_path = templates_dir / "ai-news-deduper" / "tools.py"
        content = tools_path.read_text()
        assert "cluster" in content.lower(), \
            "tools.py should contain clustering logic"


class TestSignalRanker:
    """Tests for Signal Ranker recipe."""
    
    def test_template_exists(self, templates_dir):
        """Test that ai-signal-ranker template exists."""
        template_path = templates_dir / "ai-signal-ranker"
        assert template_path.exists(), "ai-signal-ranker template should exist"
    
    def test_ranking_criteria(self, templates_dir):
        """Test that ranker has ranking criteria."""
        import yaml
        recipe_path = templates_dir / "ai-signal-ranker" / "recipe.yaml"
        with open(recipe_path) as f:
            recipe = yaml.safe_load(f)
        
        config = recipe.get("config", {})
        assert "ranking_criteria" in config or "criteria" in config, \
            "Recipe should have ranking criteria"


class TestContextEnricher:
    """Tests for Context Enricher recipe."""
    
    def test_template_exists(self, templates_dir):
        """Test that ai-context-enricher template exists."""
        template_path = templates_dir / "ai-context-enricher"
        assert template_path.exists(), "ai-context-enricher template should exist"
    
    def test_enrichment_features(self, templates_dir):
        """Test that enricher has required features."""
        tools_path = templates_dir / "ai-context-enricher" / "tools.py"
        content = tools_path.read_text()
        
        features = ["background", "prior_art", "hype"]
        found = sum(1 for f in features if f in content.lower())
        assert found >= 2, "tools.py should contain enrichment features"


class TestBriefGenerator:
    """Tests for Daily/Weekly Brief Generator recipe."""
    
    def test_template_exists(self, templates_dir):
        """Test that ai-brief-generator template exists."""
        template_path = templates_dir / "ai-brief-generator"
        assert template_path.exists(), "ai-brief-generator template should exist"
    
    def test_brief_formats(self, templates_dir):
        """Test that brief generator supports multiple formats."""
        import yaml
        recipe_path = templates_dir / "ai-brief-generator" / "recipe.yaml"
        with open(recipe_path) as f:
            recipe = yaml.safe_load(f)
        
        config = recipe.get("config", {})
        assert "formats" in config or "format" in config, \
            "Recipe should support brief formats"
