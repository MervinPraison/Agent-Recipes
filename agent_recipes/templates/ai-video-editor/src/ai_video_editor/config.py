"""
Configuration and presets for AI Video Editor.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


# Preset configurations
PRESETS = {
    "podcast": {
        "remove_fillers": True,
        "remove_repetitions": True,
        "remove_tangents": False,
        "remove_silence": True,
        "silence_threshold_ms": 700,
        "min_segment_length": 1.2,
        "padding_ms": 120,
        "filler_words": ["um", "uh", "like", "you know", "sort of", "kind of", "basically", "actually", "literally", "right"],
    },
    "meeting": {
        "remove_fillers": True,
        "remove_repetitions": True,
        "remove_tangents": True,
        "remove_silence": True,
        "silence_threshold_ms": 1000,
        "min_segment_length": 1.5,
        "padding_ms": 150,
        "filler_words": ["um", "uh", "like", "you know"],
    },
    "course": {
        "remove_fillers": True,
        "remove_repetitions": True,
        "remove_tangents": False,
        "remove_silence": True,
        "silence_threshold_ms": 500,
        "min_segment_length": 1.0,
        "padding_ms": 100,
        "filler_words": ["um", "uh"],
    },
    "clean": {
        "remove_fillers": True,
        "remove_repetitions": True,
        "remove_tangents": True,
        "remove_silence": True,
        "silence_threshold_ms": 600,
        "min_segment_length": 1.0,
        "padding_ms": 100,
        "filler_words": ["um", "uh", "like", "you know", "sort of", "kind of"],
    },
}


@dataclass
class EditConfig:
    """Configuration for video editing."""
    preset: str = "podcast"
    remove_fillers: bool = True
    remove_repetitions: bool = True
    remove_tangents: bool = False
    remove_silence: bool = True
    silence_threshold_ms: int = 700
    min_segment_length: float = 1.2
    padding_ms: int = 120
    filler_words: List[str] = field(default_factory=lambda: ["um", "uh", "like", "you know"])
    target_length: Optional[float] = None  # seconds
    auto_crop: str = "off"  # off, center, face
    captions: str = "srt"  # off, srt, burn
    provider: str = "auto"  # openai, local, auto
    use_llm: bool = True
    verbose: bool = False
    
    @classmethod
    def from_preset(cls, preset: str, **overrides) -> "EditConfig":
        """Create config from preset with optional overrides."""
        if preset not in PRESETS:
            raise ValueError(f"Unknown preset: {preset}. Available: {list(PRESETS.keys())}")
        
        config_dict = PRESETS[preset].copy()
        config_dict["preset"] = preset
        config_dict.update(overrides)
        
        return cls(**{k: v for k, v in config_dict.items() if k in cls.__dataclass_fields__})
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "preset": self.preset,
            "remove_fillers": self.remove_fillers,
            "remove_repetitions": self.remove_repetitions,
            "remove_tangents": self.remove_tangents,
            "remove_silence": self.remove_silence,
            "silence_threshold_ms": self.silence_threshold_ms,
            "min_segment_length": self.min_segment_length,
            "padding_ms": self.padding_ms,
            "filler_words": self.filler_words,
            "target_length": self.target_length,
            "auto_crop": self.auto_crop,
            "captions": self.captions,
            "provider": self.provider,
            "use_llm": self.use_llm,
            "verbose": self.verbose,
        }
