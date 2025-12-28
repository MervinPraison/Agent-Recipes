"""
AI Video Editor - Self-contained recipe for PraisonAI

This module provides end-to-end AI-powered video editing:
- Transcription with word-level timestamps
- Filler word detection and removal
- Repetition detection
- Tangent/off-topic segment identification
- Timeline optimization
- FFmpeg-based rendering

Usage:
    python -m ai_video_editor.cli edit input.mp4 --preset podcast
    python -m ai_video_editor.cli probe input.mp4
    python -m ai_video_editor.cli transcript input.mp4
"""

__version__ = "1.0.0"

from .pipeline import edit, probe, transcript
from .config import PRESETS, EditConfig
from .models import (
    Word,
    Segment,
    SegmentCategory,
    EditPlan,
    VideoProbeResult,
    TranscriptResult,
    VideoEditResult,
)

__all__ = [
    "edit",
    "probe", 
    "transcript",
    "PRESETS",
    "EditConfig",
    "Word",
    "Segment",
    "SegmentCategory",
    "EditPlan",
    "VideoProbeResult",
    "TranscriptResult",
    "VideoEditResult",
]
