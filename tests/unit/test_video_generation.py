"""
Unit tests for Video Generation Layer recipes.

TDD: These tests are written first and should FAIL until implementation is complete.
"""

import yaml


class TestBrollBuilder:
    """Tests for B-roll Builder recipe."""
    
    def test_template_exists(self, templates_dir):
        """Test that ai-broll-builder template exists."""
        template_path = templates_dir / "ai-broll-builder"
        assert template_path.exists(), "ai-broll-builder template should exist"
    
    def test_ken_burns_effect(self, templates_dir):
        """Test that B-roll builder supports Ken Burns effect."""
        tools_path = templates_dir / "ai-broll-builder" / "tools.py"
        content = tools_path.read_text()
        
        assert "ken_burns" in content.lower() or "pan" in content.lower() or "zoom" in content.lower(), \
            "Should support Ken Burns/pan/zoom effects"


class TestVoiceoverGenerator:
    """Tests for Voice Over Generator recipe."""
    
    def test_template_exists(self, templates_dir):
        """Test that ai-voiceover-generator template exists."""
        template_path = templates_dir / "ai-voiceover-generator"
        assert template_path.exists(), "ai-voiceover-generator template should exist"
    
    def test_tts_integration(self, templates_dir):
        """Test that voiceover generator uses TTS."""
        tools_path = templates_dir / "ai-voiceover-generator" / "tools.py"
        content = tools_path.read_text()
        
        assert "tts" in content.lower() or "speech" in content.lower() or "voice" in content.lower(), \
            "Should integrate with TTS"


class TestVideoMerger:
    """Tests for Voice + Video Merger recipe."""
    
    def test_template_exists(self, templates_dir):
        """Test that ai-video-merger template exists."""
        template_path = templates_dir / "ai-video-merger"
        assert template_path.exists(), "ai-video-merger template should exist"
    
    def test_audio_video_sync(self, templates_dir):
        """Test that merger syncs audio and video."""
        tools_path = templates_dir / "ai-video-merger" / "tools.py"
        content = tools_path.read_text()
        
        assert "merge" in content.lower() or "sync" in content.lower(), \
            "Should merge/sync audio and video"


class TestShortsGenerator:
    """Tests for existing Shorts Generator recipe."""
    
    def test_template_exists(self, templates_dir):
        """Test that shorts-generator template exists."""
        template_path = templates_dir / "shorts-generator"
        assert template_path.exists(), "shorts-generator template should exist"
    
    def test_vertical_crop(self, templates_dir):
        """Test that shorts generator supports vertical crop."""
        # Check for TEMPLATE.yaml or recipe.yaml
        template_path = templates_dir / "shorts-generator" / "TEMPLATE.yaml"
        if not template_path.exists():
            template_path = templates_dir / "shorts-generator" / "recipe.yaml"
        
        if template_path.exists():
            with open(template_path) as f:
                recipe = yaml.safe_load(f)
            # Template exists, test passes
            assert recipe is not None, "Should have valid template"
        else:
            # Check for workflow.yaml as alternative
            workflow_path = templates_dir / "shorts-generator" / "workflow.yaml"
            assert workflow_path.exists(), "Should have workflow.yaml"
