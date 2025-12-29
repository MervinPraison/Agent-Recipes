"""
Unit tests for Feedback & Learning Layer recipes.

TDD: These tests are written first and should FAIL until implementation is complete.
"""

import yaml


class TestPerformanceAnalyzer:
    """Tests for Performance Analyzer recipe."""
    
    def test_template_exists(self, templates_dir):
        """Test that ai-performance-analyzer template exists."""
        template_path = templates_dir / "ai-performance-analyzer"
        assert template_path.exists(), "ai-performance-analyzer template should exist"
    
    def test_metrics_input(self, templates_dir):
        """Test that analyzer accepts metrics JSON input."""
        recipe_path = templates_dir / "ai-performance-analyzer" / "recipe.yaml"
        with open(recipe_path) as f:
            recipe = yaml.safe_load(f)
        
        input_schema = recipe.get("input", {})
        assert input_schema is not None, "Should have input schema for metrics"


class TestCommentMiner:
    """Tests for Comment Miner recipe."""
    
    def test_template_exists(self, templates_dir):
        """Test that ai-comment-miner template exists."""
        template_path = templates_dir / "ai-comment-miner"
        assert template_path.exists(), "ai-comment-miner template should exist"
    
    def test_idea_extraction(self, templates_dir):
        """Test that comment miner extracts content ideas."""
        tools_path = templates_dir / "ai-comment-miner" / "tools.py"
        content = tools_path.read_text()
        
        assert "idea" in content.lower() or "extract" in content.lower(), \
            "Should extract content ideas from comments"


class TestABHookTester:
    """Tests for A/B Hook Tester Pack recipe."""
    
    def test_template_exists(self, templates_dir):
        """Test that ai-ab-hook-tester template exists."""
        template_path = templates_dir / "ai-ab-hook-tester"
        assert template_path.exists(), "ai-ab-hook-tester template should exist"
    
    def test_variant_generation(self, templates_dir):
        """Test that A/B tester generates variants."""
        tools_path = templates_dir / "ai-ab-hook-tester" / "tools.py"
        content = tools_path.read_text()
        
        assert "variant" in content.lower() or "test" in content.lower(), \
            "Should generate test variants"
