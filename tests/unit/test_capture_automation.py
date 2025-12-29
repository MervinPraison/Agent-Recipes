"""
Unit tests for Capture & Screen Automation Layer recipes.

TDD: These tests are written first and should FAIL until implementation is complete.
"""

import yaml


class TestScreenshotCapture:
    """Tests for Auto Screenshot Capture recipe."""
    
    def test_template_exists(self, templates_dir):
        """Test that ai-screenshot-capture template exists."""
        template_path = templates_dir / "ai-screenshot-capture"
        assert template_path.exists(), "ai-screenshot-capture template should exist"
    
    def test_high_res_support(self, templates_dir):
        """Test that screenshot capture supports high resolution."""
        recipe_path = templates_dir / "ai-screenshot-capture" / "recipe.yaml"
        with open(recipe_path) as f:
            recipe = yaml.safe_load(f)
        
        config = recipe.get("config", {})
        assert "resolution" in config or "quality" in config, \
            "Should support resolution/quality config"


class TestScreenRecorder:
    """Tests for Auto Screen Recording recipe."""
    
    def test_template_exists(self, templates_dir):
        """Test that ai-screen-recorder template exists."""
        template_path = templates_dir / "ai-screen-recorder"
        assert template_path.exists(), "ai-screen-recorder template should exist"
    
    def test_recording_config(self, templates_dir):
        """Test that screen recorder has recording config."""
        recipe_path = templates_dir / "ai-screen-recorder" / "recipe.yaml"
        with open(recipe_path) as f:
            recipe = yaml.safe_load(f)
        
        config = recipe.get("config", {})
        assert "fps" in config or "duration" in config, \
            "Should have recording configuration"


class TestNewsCapturePack:
    """Tests for News Page Capture Pack recipe."""
    
    def test_template_exists(self, templates_dir):
        """Test that ai-news-capture-pack template exists."""
        template_path = templates_dir / "ai-news-capture-pack"
        assert template_path.exists(), "ai-news-capture-pack template should exist"
    
    def test_bundles_assets(self, templates_dir):
        """Test that capture pack bundles assets."""
        tools_path = templates_dir / "ai-news-capture-pack" / "tools.py"
        content = tools_path.read_text()
        
        assert "bundle" in content.lower() or "pack" in content.lower(), \
            "Should bundle assets per story"
