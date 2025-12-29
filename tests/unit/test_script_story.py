"""
Unit tests for Script & Story Layer recipes.

TDD: These tests are written first and should FAIL until implementation is complete.
"""

import yaml


class TestScriptWriter:
    """Tests for Multi-Format Script Writer recipe."""
    
    def test_template_exists(self, templates_dir):
        """Test that ai-script-writer template exists."""
        template_path = templates_dir / "ai-script-writer"
        assert template_path.exists(), "ai-script-writer template should exist"
    
    def test_supports_multiple_formats(self, templates_dir):
        """Test that script writer supports multiple formats."""
        recipe_path = templates_dir / "ai-script-writer" / "recipe.yaml"
        with open(recipe_path) as f:
            recipe = yaml.safe_load(f)
        
        config = recipe.get("config", {})
        formats = config.get("formats", [])
        
        required_formats = ["youtube_long", "youtube_short", "x_thread", "linkedin"]
        for fmt in required_formats:
            assert fmt in formats or any(fmt in str(f).lower() for f in formats), \
                f"Script writer should support {fmt} format"


class TestAngleGenerator:
    """Tests for Angle Generator recipe."""
    
    def test_template_exists(self, templates_dir):
        """Test that ai-angle-generator template exists."""
        template_path = templates_dir / "ai-angle-generator"
        assert template_path.exists(), "ai-angle-generator template should exist"
    
    def test_angle_types(self, templates_dir):
        """Test that angle generator has multiple angle types."""
        recipe_path = templates_dir / "ai-angle-generator" / "recipe.yaml"
        with open(recipe_path) as f:
            recipe = yaml.safe_load(f)
        
        config = recipe.get("config", {})
        angles = config.get("angle_types", config.get("angles", []))
        
        assert len(angles) >= 3, "Should have at least 3 angle types"


class TestHookGenerator:
    """Tests for Hook Generator recipe."""
    
    def test_template_exists(self, templates_dir):
        """Test that ai-hook-generator template exists."""
        template_path = templates_dir / "ai-hook-generator"
        assert template_path.exists(), "ai-hook-generator template should exist"
    
    def test_generates_variants(self, templates_dir):
        """Test that hook generator creates multiple variants."""
        tools_path = templates_dir / "ai-hook-generator" / "tools.py"
        content = tools_path.read_text()
        
        assert "variant" in content.lower() or "multiple" in content.lower(), \
            "Hook generator should create multiple variants"


class TestCTAGenerator:
    """Tests for CTA + Title Generator recipe."""
    
    def test_template_exists(self, templates_dir):
        """Test that ai-cta-generator template exists."""
        template_path = templates_dir / "ai-cta-generator"
        assert template_path.exists(), "ai-cta-generator template should exist"
    
    def test_platform_specific(self, templates_dir):
        """Test that CTA generator is platform-specific."""
        recipe_path = templates_dir / "ai-cta-generator" / "recipe.yaml"
        with open(recipe_path) as f:
            recipe = yaml.safe_load(f)
        
        config = recipe.get("config", {})
        assert "platforms" in config or "platform" in config, \
            "CTA generator should support platform-specific CTAs"


class TestFactChecker:
    """Tests for Fact-check Helper recipe."""
    
    def test_template_exists(self, templates_dir):
        """Test that ai-fact-checker template exists."""
        template_path = templates_dir / "ai-fact-checker"
        assert template_path.exists(), "ai-fact-checker template should exist"
    
    def test_citation_support(self, templates_dir):
        """Test that fact checker supports citations."""
        tools_path = templates_dir / "ai-fact-checker" / "tools.py"
        content = tools_path.read_text()
        
        assert "citation" in content.lower() or "source" in content.lower(), \
            "Fact checker should support citations"
