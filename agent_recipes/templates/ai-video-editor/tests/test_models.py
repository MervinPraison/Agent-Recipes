"""
Unit tests for AI Video Editor models.
"""

import sys
import os
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import pytest


class TestWord:
    """Test Word model."""
    
    def test_word_serialization(self):
        from ai_video_editor.models import Word
        
        word = Word(text="hello", start=1.0, end=1.5, confidence=0.95)
        data = word.to_dict()
        
        assert data["text"] == "hello"
        assert data["start"] == 1.0
        assert data["end"] == 1.5
        assert data["confidence"] == 0.95
        
        word2 = Word.from_dict(data)
        assert word2.text == word.text
        assert word2.start == word.start


class TestSegment:
    """Test Segment model."""
    
    def test_segment_duration(self):
        from ai_video_editor.models import Segment, SegmentCategory
        
        seg = Segment(start=10.0, end=15.5, category=SegmentCategory.KEEP)
        assert seg.duration == 5.5
    
    def test_segment_serialization(self):
        from ai_video_editor.models import Segment, SegmentCategory
        
        seg = Segment(
            start=0.0,
            end=10.0,
            category=SegmentCategory.FILLER,
            reason="um",
            text="um"
        )
        
        data = seg.to_dict()
        assert data["category"] == "filler"
        
        seg2 = Segment.from_dict(data)
        assert seg2.category == SegmentCategory.FILLER


class TestEditPlan:
    """Test EditPlan model."""
    
    def test_edit_plan_stats(self):
        from ai_video_editor.models import EditPlan, Segment, SegmentCategory
        
        plan = EditPlan(
            segments_to_keep=[
                Segment(start=0, end=10, category=SegmentCategory.KEEP),
                Segment(start=15, end=25, category=SegmentCategory.KEEP),
            ],
            segments_to_remove=[
                Segment(start=10, end=12, category=SegmentCategory.FILLER),
                Segment(start=12, end=15, category=SegmentCategory.SILENCE),
            ]
        )
        
        assert plan.total_keep_duration == 20.0
        assert plan.total_remove_duration == 5.0
        
        stats = plan.removal_stats
        assert stats["filler"] == 2.0
        assert stats["silence"] == 3.0
    
    def test_edit_plan_json(self, tmp_path):
        from ai_video_editor.models import EditPlan, Segment, SegmentCategory
        
        plan = EditPlan(
            segments_to_keep=[
                Segment(start=0, end=10, category=SegmentCategory.KEEP, reason="intro"),
            ],
            summary="Test video",
            topics=["testing"]
        )
        
        json_path = tmp_path / "plan.json"
        plan.to_json(json_path)
        
        plan2 = EditPlan.from_json(json_path)
        assert plan2.summary == "Test video"
        assert len(plan2.segments_to_keep) == 1
        assert plan2.topics == ["testing"]


class TestTranscriptResult:
    """Test TranscriptResult model."""
    
    def test_transcript_to_srt(self, tmp_path):
        from ai_video_editor.models import TranscriptResult, Word
        
        transcript = TranscriptResult(
            text="Hello world this is a test",
            words=[
                Word(text="Hello", start=0.0, end=0.5),
                Word(text="world", start=0.5, end=1.0),
                Word(text="this", start=1.0, end=1.3),
                Word(text="is", start=1.3, end=1.5),
                Word(text="a", start=1.5, end=1.6),
                Word(text="test", start=1.6, end=2.0),
            ],
            duration=2.0
        )
        
        srt_path = tmp_path / "captions.srt"
        srt_content = transcript.to_srt(srt_path)
        
        assert srt_path.exists()
        assert "Hello world this is a test" in srt_content
        assert "-->" in srt_content


class TestPresets:
    """Test preset configurations."""
    
    def test_presets_exist(self):
        from ai_video_editor.config import PRESETS
        
        assert "podcast" in PRESETS
        assert "meeting" in PRESETS
        assert "course" in PRESETS
        assert "clean" in PRESETS
    
    def test_podcast_preset(self):
        from ai_video_editor.config import PRESETS
        
        podcast = PRESETS["podcast"]
        assert podcast["remove_fillers"] is True
        assert "um" in podcast["filler_words"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
