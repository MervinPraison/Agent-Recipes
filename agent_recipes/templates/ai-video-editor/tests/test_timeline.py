"""
Unit tests for timeline optimization.
"""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import pytest


class TestTimelineOptimization:
    """Test timeline optimization functions."""
    
    def test_merge_overlapping_segments(self):
        from ai_video_editor.models import Segment, SegmentCategory
        from ai_video_editor.timeline import _merge_overlapping
        
        segments = [
            Segment(start=0, end=10, category=SegmentCategory.KEEP),
            Segment(start=8, end=15, category=SegmentCategory.KEEP),
            Segment(start=20, end=25, category=SegmentCategory.KEEP),
        ]
        
        merged = _merge_overlapping(segments)
        
        assert len(merged) == 2
        assert merged[0].start == 0
        assert merged[0].end == 15
        assert merged[1].start == 20
    
    def test_get_keep_intervals(self):
        from ai_video_editor.models import EditPlan, Segment, SegmentCategory
        from ai_video_editor.timeline import get_keep_intervals
        
        plan = EditPlan(
            segments_to_keep=[
                Segment(start=10, end=20, category=SegmentCategory.KEEP),
                Segment(start=0, end=5, category=SegmentCategory.KEEP),
            ]
        )
        
        intervals = get_keep_intervals(plan)
        
        assert intervals[0] == (0, 5)
        assert intervals[1] == (10, 20)
    
    def test_calculate_final_duration(self):
        from ai_video_editor.models import EditPlan, Segment, SegmentCategory
        from ai_video_editor.timeline import calculate_final_duration
        
        plan = EditPlan(
            segments_to_keep=[
                Segment(start=0, end=10, category=SegmentCategory.KEEP),
                Segment(start=20, end=35, category=SegmentCategory.KEEP),
            ]
        )
        
        duration = calculate_final_duration(plan)
        assert duration == 25.0


class TestUtils:
    """Test utility functions."""
    
    def test_format_duration(self):
        from ai_video_editor.utils import format_duration
        
        assert format_duration(30) == "30s"
        assert format_duration(90) == "1m 30s"
        assert format_duration(3661) == "1h 1m 1s"
    
    def test_parse_duration(self):
        from ai_video_editor.utils import parse_duration
        
        assert parse_duration("30s") == 30.0
        assert parse_duration("5m") == 300.0
        assert parse_duration("1h30m") == 5400.0
        assert parse_duration("1h30m45s") == 5445.0
        assert parse_duration("90") == 90.0
    
    def test_file_hash(self, tmp_path):
        from ai_video_editor.utils import file_hash
        
        test_file = tmp_path / "test.txt"
        test_file.write_text("hello world")
        
        hash1 = file_hash(str(test_file))
        hash2 = file_hash(str(test_file))
        
        assert hash1 == hash2
        assert len(hash1) == 64
    
    def test_check_ffmpeg(self):
        from ai_video_editor.utils import check_ffmpeg
        
        available, msg = check_ffmpeg()
        assert isinstance(available, bool)
        assert isinstance(msg, str)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
