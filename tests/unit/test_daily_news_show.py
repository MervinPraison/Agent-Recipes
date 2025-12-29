"""
Unit tests for Daily AI News Show Agent (end-to-end orchestrator).

TDD: These tests are written first and should FAIL until implementation is complete.
"""

import yaml


class TestDailyNewsShow:
    """Tests for Daily AI News Show orchestrator recipe."""
    
    def test_template_exists(self, templates_dir):
        """Test that ai-daily-news-show template exists."""
        template_path = templates_dir / "ai-daily-news-show"
        assert template_path.exists(), "ai-daily-news-show template should exist"
    
    def test_has_recipe_yaml(self, templates_dir):
        """Test that template has recipe.yaml."""
        recipe_path = templates_dir / "ai-daily-news-show" / "recipe.yaml"
        assert recipe_path.exists(), "recipe.yaml should exist"
    
    def test_pipeline_stages(self, templates_dir):
        """Test that orchestrator has all pipeline stages."""
        recipe_path = templates_dir / "ai-daily-news-show" / "recipe.yaml"
        with open(recipe_path) as f:
            recipe = yaml.safe_load(f)
        
        # Check for pipeline/workflow definition
        workflow = recipe.get("workflow", recipe.get("pipeline", recipe.get("agents", [])))
        assert workflow, "Should have workflow/pipeline definition"
    
    def test_human_approval_config(self, templates_dir):
        """Test that orchestrator supports human approval."""
        recipe_path = templates_dir / "ai-daily-news-show" / "recipe.yaml"
        with open(recipe_path) as f:
            recipe = yaml.safe_load(f)
        
        config = recipe.get("config", {})
        # Human approval should be configurable
        assert "human_approval" in config or "approval" in config or "review" in config, \
            "Should support human approval configuration"
    
    def test_output_bundle(self, templates_dir):
        """Test that orchestrator produces output bundle."""
        tools_path = templates_dir / "ai-daily-news-show" / "tools.py"
        content = tools_path.read_text()
        
        assert "bundle" in content.lower() or "output" in content.lower(), \
            "Should produce output bundle"
