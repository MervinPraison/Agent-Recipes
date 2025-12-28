"""
Utility functions for AI Video Editor.

Provides:
- FFmpeg detection and command building
- File hashing for reproducibility
- Working directory management
- Time formatting utilities
"""

import hashlib
import os
import shutil
import subprocess
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
import json


def check_ffmpeg() -> Tuple[bool, str]:
    """Check if ffmpeg is available."""
    try:
        result = subprocess.run(
            ["ffmpeg", "-version"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            version_line = result.stdout.split("\n")[0]
            return True, version_line
        return False, "ffmpeg returned non-zero exit code"
    except FileNotFoundError:
        return False, "ffmpeg not found. Install with: brew install ffmpeg (macOS) or apt install ffmpeg (Linux)"
    except subprocess.TimeoutExpired:
        return False, "ffmpeg check timed out"
    except Exception as e:
        return False, f"Error checking ffmpeg: {e}"


def check_ffprobe() -> Tuple[bool, str]:
    """Check if ffprobe is available."""
    try:
        result = subprocess.run(
            ["ffprobe", "-version"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            version_line = result.stdout.split("\n")[0]
            return True, version_line
        return False, "ffprobe returned non-zero exit code"
    except FileNotFoundError:
        return False, "ffprobe not found. Install ffmpeg which includes ffprobe."
    except subprocess.TimeoutExpired:
        return False, "ffprobe check timed out"
    except Exception as e:
        return False, f"Error checking ffprobe: {e}"


def ensure_ffmpeg():
    """Raise error if ffmpeg is not available."""
    available, msg = check_ffmpeg()
    if not available:
        raise RuntimeError(f"FFmpeg is required but not available: {msg}")


def file_hash(path: str, algorithm: str = "sha256") -> str:
    """Compute hash of a file."""
    h = hashlib.new(algorithm)
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def create_workdir(input_path: str, base_dir: Optional[str] = None) -> Path:
    """Create a working directory for video processing."""
    if base_dir is None:
        base_dir = os.path.join(os.getcwd(), ".praison", "video")
    
    input_hash = file_hash(input_path)[:12]
    input_name = Path(input_path).stem
    workdir = Path(base_dir) / f"{input_name}_{input_hash}"
    
    workdir.mkdir(parents=True, exist_ok=True)
    (workdir / "audio").mkdir(exist_ok=True)
    (workdir / "segments").mkdir(exist_ok=True)
    (workdir / "output").mkdir(exist_ok=True)
    
    return workdir


def format_duration(seconds: float) -> str:
    """Format duration in human-readable format."""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    
    parts = []
    if hours > 0:
        parts.append(f"{hours}h")
    if minutes > 0 or hours > 0:
        parts.append(f"{minutes}m")
    parts.append(f"{secs}s")
    
    return " ".join(parts)


def parse_duration(duration_str: str) -> float:
    """Parse duration string to seconds."""
    import re
    
    total = 0.0
    
    h_match = re.search(r"(\d+)h", duration_str)
    if h_match:
        total += int(h_match.group(1)) * 3600
    
    m_match = re.search(r"(\d+)m", duration_str)
    if m_match:
        total += int(m_match.group(1)) * 60
    
    s_match = re.search(r"(\d+)s", duration_str)
    if s_match:
        total += int(s_match.group(1))
    
    if total == 0:
        try:
            total = float(duration_str)
        except ValueError:
            pass
    
    return total


def extract_audio(video_path: str, output_path: str, sample_rate: int = 16000, mono: bool = True) -> str:
    """Extract audio from video file."""
    ensure_ffmpeg()
    
    cmd = [
        "ffmpeg", "-y",
        "-i", video_path,
        "-vn",
        "-acodec", "pcm_s16le",
        "-ar", str(sample_rate),
    ]
    
    if mono:
        cmd.extend(["-ac", "1"])
    
    cmd.append(output_path)
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"Failed to extract audio: {result.stderr}")
    
    return output_path


def generate_edl(
    segments_to_keep: List[Tuple[float, float]],
    segments_to_remove: List[Tuple[float, float, str]],
    output_path: str,
    fps: float = 30.0
) -> str:
    """Generate Edit Decision List (EDL) file."""
    lines = [
        "TITLE: AI Video Editor EDL",
        "FCM: NON-DROP FRAME",
        ""
    ]
    
    for i, (start, end) in enumerate(segments_to_keep, 1):
        start_tc = _seconds_to_timecode(start, fps)
        end_tc = _seconds_to_timecode(end, fps)
        lines.append(f"{i:03d}  AX       V     C        {start_tc} {end_tc} {start_tc} {end_tc}")
    
    lines.append("")
    lines.append("* REMOVED SEGMENTS:")
    
    for start, end, reason in segments_to_remove:
        start_tc = _seconds_to_timecode(start, fps)
        end_tc = _seconds_to_timecode(end, fps)
        lines.append(f"* {start_tc} - {end_tc}: {reason}")
    
    content = "\n".join(lines)
    Path(output_path).write_text(content)
    return output_path


def _seconds_to_timecode(seconds: float, fps: float = 30.0) -> str:
    """Convert seconds to SMPTE timecode."""
    frames = int((seconds % 1) * fps)
    total_secs = int(seconds)
    hours = total_secs // 3600
    minutes = (total_secs % 3600) // 60
    secs = total_secs % 60
    return f"{hours:02d}:{minutes:02d}:{secs:02d}:{frames:02d}"


def save_config_snapshot(config: Dict[str, Any], workdir: Path) -> str:
    """Save configuration snapshot for reproducibility."""
    config_path = workdir / "config_snapshot.json"
    with open(config_path, "w") as f:
        json.dump(config, f, indent=2, default=str)
    return str(config_path)


def cleanup_workdir(workdir: Path, keep_output: bool = True):
    """Clean up working directory."""
    if not workdir.exists():
        return
    
    for item in workdir.iterdir():
        if keep_output and item.name == "output":
            continue
        if item.is_dir():
            shutil.rmtree(item)
        else:
            item.unlink()
