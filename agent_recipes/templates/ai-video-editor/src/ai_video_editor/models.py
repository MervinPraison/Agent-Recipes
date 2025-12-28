"""
Data models for AI Video Editor.

Defines data structures for:
- Video metadata and probe results
- Transcripts with word-level timestamps
- Edit plans and segments
- Final edit results
"""

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
import json


class SegmentCategory(str, Enum):
    """Category of segment to remove."""
    FILLER = "filler"
    TANGENT = "tangent"
    REPEAT = "repeat"
    NOISE = "noise"
    SILENCE = "silence"
    KEEP = "keep"


@dataclass
class Word:
    """A single word with timing information."""
    text: str
    start: float  # seconds
    end: float  # seconds
    confidence: float = 1.0
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "text": self.text,
            "start": self.start,
            "end": self.end,
            "confidence": self.confidence
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Word":
        return cls(
            text=data["text"],
            start=data["start"],
            end=data["end"],
            confidence=data.get("confidence", 1.0)
        )


@dataclass
class Segment:
    """A segment of video with timing and metadata."""
    start: float  # seconds
    end: float  # seconds
    category: SegmentCategory = SegmentCategory.KEEP
    reason: str = ""
    confidence: float = 1.0
    text: str = ""
    words: List[Word] = field(default_factory=list)
    
    @property
    def duration(self) -> float:
        return self.end - self.start
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "start": self.start,
            "end": self.end,
            "category": self.category.value,
            "reason": self.reason,
            "confidence": self.confidence,
            "text": self.text,
            "words": [w.to_dict() for w in self.words]
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Segment":
        return cls(
            start=data["start"],
            end=data["end"],
            category=SegmentCategory(data.get("category", "keep")),
            reason=data.get("reason", ""),
            confidence=data.get("confidence", 1.0),
            text=data.get("text", ""),
            words=[Word.from_dict(w) for w in data.get("words", [])]
        )


@dataclass
class Chapter:
    """A chapter marker for the video."""
    start: float  # seconds
    title: str
    description: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "start": self.start,
            "title": self.title,
            "description": self.description
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Chapter":
        return cls(
            start=data["start"],
            title=data["title"],
            description=data.get("description", "")
        )


@dataclass
class EditPlan:
    """Complete edit plan for a video."""
    segments_to_keep: List[Segment] = field(default_factory=list)
    segments_to_remove: List[Segment] = field(default_factory=list)
    chapters: List[Chapter] = field(default_factory=list)
    summary: str = ""
    topics: List[str] = field(default_factory=list)
    
    @property
    def total_keep_duration(self) -> float:
        return sum(s.duration for s in self.segments_to_keep)
    
    @property
    def total_remove_duration(self) -> float:
        return sum(s.duration for s in self.segments_to_remove)
    
    @property
    def removal_stats(self) -> Dict[str, float]:
        """Get duration removed by category."""
        stats: Dict[str, float] = {}
        for seg in self.segments_to_remove:
            cat = seg.category.value
            stats[cat] = stats.get(cat, 0) + seg.duration
        return stats
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "segments_to_keep": [s.to_dict() for s in self.segments_to_keep],
            "segments_to_remove": [s.to_dict() for s in self.segments_to_remove],
            "chapters": [c.to_dict() for c in self.chapters],
            "summary": self.summary,
            "topics": self.topics,
            "stats": {
                "total_keep_duration": self.total_keep_duration,
                "total_remove_duration": self.total_remove_duration,
                "removal_by_category": self.removal_stats
            }
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "EditPlan":
        return cls(
            segments_to_keep=[Segment.from_dict(s) for s in data.get("segments_to_keep", [])],
            segments_to_remove=[Segment.from_dict(s) for s in data.get("segments_to_remove", [])],
            chapters=[Chapter.from_dict(c) for c in data.get("chapters", [])],
            summary=data.get("summary", ""),
            topics=data.get("topics", [])
        )
    
    def to_json(self, path: Optional[Union[str, Path]] = None) -> str:
        """Export plan to JSON."""
        json_str = json.dumps(self.to_dict(), indent=2)
        if path:
            Path(path).write_text(json_str)
        return json_str
    
    @classmethod
    def from_json(cls, json_str_or_path: Union[str, Path]) -> "EditPlan":
        """Load plan from JSON string or file."""
        path = Path(json_str_or_path)
        if path.exists():
            data = json.loads(path.read_text())
        else:
            data = json.loads(str(json_str_or_path))
        return cls.from_dict(data)


@dataclass
class VideoProbeResult:
    """Result of probing a video file."""
    path: str
    duration: float  # seconds
    width: int
    height: int
    fps: float
    codec: str
    audio_codec: str = ""
    audio_channels: int = 0
    audio_sample_rate: int = 0
    bitrate: int = 0
    file_size: int = 0
    format_name: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "path": self.path,
            "duration": self.duration,
            "width": self.width,
            "height": self.height,
            "fps": self.fps,
            "codec": self.codec,
            "audio_codec": self.audio_codec,
            "audio_channels": self.audio_channels,
            "audio_sample_rate": self.audio_sample_rate,
            "bitrate": self.bitrate,
            "file_size": self.file_size,
            "format_name": self.format_name
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "VideoProbeResult":
        return cls(**data)


@dataclass
class TranscriptResult:
    """Result of transcribing audio."""
    text: str
    words: List[Word] = field(default_factory=list)
    language: str = "en"
    duration: float = 0.0
    provider: str = "openai"
    
    def to_srt(self, path: Optional[Union[str, Path]] = None) -> str:
        """Export transcript to SRT format."""
        lines = []
        segments = []
        current_segment: List[Word] = []
        segment_start = 0.0
        
        for word in self.words:
            if not current_segment:
                segment_start = word.start
                current_segment.append(word)
            elif len(current_segment) >= 10 or (word.end - segment_start) > 5.0:
                segments.append((segment_start, current_segment[-1].end, current_segment))
                current_segment = [word]
                segment_start = word.start
            else:
                current_segment.append(word)
        
        if current_segment:
            segments.append((segment_start, current_segment[-1].end, current_segment))
        
        for i, (start, end, words) in enumerate(segments, 1):
            text = " ".join(w.text for w in words)
            start_ts = _format_srt_time(start)
            end_ts = _format_srt_time(end)
            lines.append(f"{i}")
            lines.append(f"{start_ts} --> {end_ts}")
            lines.append(text)
            lines.append("")
        
        srt_content = "\n".join(lines)
        if path:
            Path(path).write_text(srt_content)
        return srt_content
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "text": self.text,
            "words": [w.to_dict() for w in self.words],
            "language": self.language,
            "duration": self.duration,
            "provider": self.provider
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TranscriptResult":
        return cls(
            text=data["text"],
            words=[Word.from_dict(w) for w in data.get("words", [])],
            language=data.get("language", "en"),
            duration=data.get("duration", 0.0),
            provider=data.get("provider", "openai")
        )


@dataclass
class VideoEditResult:
    """Result of editing a video."""
    output_path: str
    report_path: str
    transcript_path: str
    srt_path: str
    edl_path: str
    
    original_duration: float
    final_duration: float
    time_saved: float
    
    edit_plan: EditPlan
    probe: VideoProbeResult
    transcript: TranscriptResult
    
    workdir: str = ""
    config_snapshot: Dict[str, Any] = field(default_factory=dict)
    
    @property
    def compression_ratio(self) -> float:
        if self.original_duration == 0:
            return 0
        return self.final_duration / self.original_duration
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "output_path": self.output_path,
            "report_path": self.report_path,
            "transcript_path": self.transcript_path,
            "srt_path": self.srt_path,
            "edl_path": self.edl_path,
            "original_duration": self.original_duration,
            "final_duration": self.final_duration,
            "time_saved": self.time_saved,
            "compression_ratio": self.compression_ratio,
            "edit_plan": self.edit_plan.to_dict(),
            "probe": self.probe.to_dict(),
            "transcript": self.transcript.to_dict(),
            "workdir": self.workdir,
            "config_snapshot": self.config_snapshot
        }
    
    def to_json(self, path: Optional[Union[str, Path]] = None) -> str:
        """Export result to JSON."""
        json_str = json.dumps(self.to_dict(), indent=2, default=str)
        if path:
            Path(path).write_text(json_str)
        return json_str


def _format_srt_time(seconds: float) -> str:
    """Format seconds as SRT timestamp (HH:MM:SS,mmm)."""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds % 1) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"
