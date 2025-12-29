"""
Unit tests for Publishing & Distribution Layer recipes.

TDD: These tests are written first and should FAIL until implementation is complete.
"""

import yaml


class TestPublisherPack:
    """Tests for Cross-platform Publisher Pack recipe."""
    
    def test_template_exists(self, templates_dir):
        """Test that ai-publisher-pack template exists."""
        template_path = templates_dir / "ai-publisher-pack"
        assert template_path.exists(), "ai-publisher-pack template should exist"
    
    def test_multi_platform_output(self, templates_dir):
        """Test that publisher pack generates multi-platform outputs."""
        recipe_path = templates_dir / "ai-publisher-pack" / "recipe.yaml"
        with open(recipe_path) as f:
            recipe = yaml.safe_load(f)
        
        config = recipe.get("config", {})
        assert "platforms" in config, "Should support multiple platforms"


class TestContentCalendar:
    """Tests for Content Calendar Generator recipe."""
    
    def test_template_exists(self, templates_dir):
        """Test that ai-content-calendar template exists."""
        template_path = templates_dir / "ai-content-calendar"
        assert template_path.exists(), "ai-content-calendar template should exist"
    
    def test_scheduling_support(self, templates_dir):
        """Test that calendar generator supports scheduling."""
        tools_path = templates_dir / "ai-content-calendar" / "tools.py"
        content = tools_path.read_text()
        
        assert "schedule" in content.lower() or "calendar" in content.lower(), \
            "Should support scheduling"


class TestPostCopyGenerator:
    """Tests for Auto Post Copy Generator recipe."""
    
    def test_template_exists(self, templates_dir):
        """Test that ai-post-copy-generator template exists."""
        template_path = templates_dir / "ai-post-copy-generator"
        assert template_path.exists(), "ai-post-copy-generator template should exist"
    
    def test_platform_specific_copy(self, templates_dir):
        """Test that post copy is platform-specific."""
        recipe_path = templates_dir / "ai-post-copy-generator" / "recipe.yaml"
        with open(recipe_path) as f:
            recipe = yaml.safe_load(f)
        
        config = recipe.get("config", {})
        assert "platforms" in config or "platform" in config, \
            "Should generate platform-specific copy"


class TestHashtagOptimizer:
    """Tests for Hashtag/Keyword Optimizer recipe."""
    
    def test_template_exists(self, templates_dir):
        """Test that ai-hashtag-optimizer template exists."""
        template_path = templates_dir / "ai-hashtag-optimizer"
        assert template_path.exists(), "ai-hashtag-optimizer template should exist"
    
    def test_keyword_optimization(self, templates_dir):
        """Test that optimizer handles keywords."""
        tools_path = templates_dir / "ai-hashtag-optimizer" / "tools.py"
        content = tools_path.read_text()
        
        assert "hashtag" in content.lower() or "keyword" in content.lower(), \
            "Should optimize hashtags/keywords"
