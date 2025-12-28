"""
Unit tests for heuristic-based content analysis.
"""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import pytest


class TestFillerDetection:
    """Test filler word detection."""
    
    def test_detect_fillers(self):
        from ai_video_editor.models import TranscriptResult, Word
        from ai_video_editor.heuristics import detect_fillers
        
        transcript = TranscriptResult(
            text="So um I think uh this is like really important",
            words=[
                Word(text="So", start=0.0, end=0.2),
                Word(text="um", start=0.3, end=0.5),
                Word(text="I", start=0.6, end=0.7),
                Word(text="think", start=0.7, end=1.0),
                Word(text="uh", start=1.1, end=1.3),
                Word(text="this", start=1.4, end=1.6),
                Word(text="is", start=1.6, end=1.8),
                Word(text="like", start=1.9, end=2.1),
                Word(text="really", start=2.2, end=2.5),
                Word(text="important", start=2.5, end=3.0),
            ],
            duration=3.0
        )
        
        filler_words = ["um", "uh", "like"]
        fillers = detect_fillers(transcript, filler_words)
        
        assert len(fillers) == 3
        assert fillers[0].text == "um"
        assert fillers[1].text == "uh"
        assert fillers[2].text == "like"
    
    def test_detect_fillers_case_insensitive(self):
        from ai_video_editor.models import TranscriptResult, Word
        from ai_video_editor.heuristics import detect_fillers
        
        transcript = TranscriptResult(
            text="UM this is UH important",
            words=[
                Word(text="UM", start=0.0, end=0.3),
                Word(text="this", start=0.4, end=0.6),
                Word(text="is", start=0.6, end=0.8),
                Word(text="UH", start=0.9, end=1.1),
                Word(text="important", start=1.2, end=1.6),
            ],
            duration=1.6
        )
        
        fillers = detect_fillers(transcript, ["um", "uh"])
        assert len(fillers) == 2


class TestRepetitionDetection:
    """Test repetition detection."""
    
    def test_detect_repetitions(self):
        from ai_video_editor.models import TranscriptResult, Word
        from ai_video_editor.heuristics import detect_repetitions
        
        transcript = TranscriptResult(
            text="I think I think this is good",
            words=[
                Word(text="I", start=0.0, end=0.1),
                Word(text="think", start=0.1, end=0.4),
                Word(text="I", start=0.5, end=0.6),
                Word(text="think", start=0.6, end=0.9),
                Word(text="this", start=1.0, end=1.2),
                Word(text="is", start=1.2, end=1.4),
                Word(text="good", start=1.4, end=1.7),
            ],
            duration=1.7
        )
        
        repetitions = detect_repetitions(transcript, window_size=5, min_repeat_words=2)
        assert len(repetitions) >= 1


class TestSilenceDetection:
    """Test silence detection."""
    
    def test_detect_silence(self):
        from ai_video_editor.models import TranscriptResult, Word
        from ai_video_editor.heuristics import detect_silence
        
        transcript = TranscriptResult(
            text="Hello world",
            words=[
                Word(text="Hello", start=0.0, end=0.5),
                Word(text="world", start=2.0, end=2.5),
            ],
            duration=2.5
        )
        
        silences = detect_silence(transcript, threshold_ms=1000)
        assert len(silences) == 1
        assert silences[0].start == 0.5
        assert silences[0].end == 2.0
    
    def test_no_silence_below_threshold(self):
        from ai_video_editor.models import TranscriptResult, Word
        from ai_video_editor.heuristics import detect_silence
        
        transcript = TranscriptResult(
            text="Hello world",
            words=[
                Word(text="Hello", start=0.0, end=0.5),
                Word(text="world", start=0.8, end=1.3),
            ],
            duration=1.3
        )
        
        silences = detect_silence(transcript, threshold_ms=700)
        assert len(silences) == 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
