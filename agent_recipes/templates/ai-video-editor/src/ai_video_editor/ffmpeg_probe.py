"""
Video probe functionality using ffprobe.
"""

import json
import os
import subprocess
from pathlib import Path

from .models import VideoProbeResult
from .utils import check_ffprobe


def probe(input_path: str) -> VideoProbeResult:
    """
    Probe a video file to extract metadata.
    
    Args:
        input_path: Path to video file
        
    Returns:
        VideoProbeResult with video metadata
    """
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Video file not found: {input_path}")
    
    available, msg = check_ffprobe()
    if not available:
        raise RuntimeError(f"ffprobe is required: {msg}")
    
    cmd = [
        "ffprobe",
        "-v", "quiet",
        "-print_format", "json",
        "-show_format",
        "-show_streams",
        input_path
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    except subprocess.TimeoutExpired:
        raise RuntimeError("ffprobe timed out")
    
    if result.returncode != 0:
        raise RuntimeError(f"ffprobe failed: {result.stderr}")
    
    try:
        data = json.loads(result.stdout)
    except json.JSONDecodeError as e:
        raise RuntimeError(f"Failed to parse ffprobe output: {e}")
    
    video_stream = None
    audio_stream = None
    
    for stream in data.get("streams", []):
        if stream.get("codec_type") == "video" and video_stream is None:
            video_stream = stream
        elif stream.get("codec_type") == "audio" and audio_stream is None:
            audio_stream = stream
    
    if video_stream is None:
        raise RuntimeError("No video stream found in file")
    
    format_info = data.get("format", {})
    
    fps = 30.0
    if "r_frame_rate" in video_stream:
        fps_parts = video_stream["r_frame_rate"].split("/")
        if len(fps_parts) == 2 and int(fps_parts[1]) != 0:
            fps = int(fps_parts[0]) / int(fps_parts[1])
        elif len(fps_parts) == 1:
            fps = float(fps_parts[0])
    elif "avg_frame_rate" in video_stream:
        fps_parts = video_stream["avg_frame_rate"].split("/")
        if len(fps_parts) == 2 and int(fps_parts[1]) != 0:
            fps = int(fps_parts[0]) / int(fps_parts[1])
    
    return VideoProbeResult(
        path=str(Path(input_path).absolute()),
        duration=float(format_info.get("duration", 0)),
        width=int(video_stream.get("width", 0)),
        height=int(video_stream.get("height", 0)),
        fps=round(fps, 3),
        codec=video_stream.get("codec_name", "unknown"),
        audio_codec=audio_stream.get("codec_name", "") if audio_stream else "",
        audio_channels=int(audio_stream.get("channels", 0)) if audio_stream else 0,
        audio_sample_rate=int(audio_stream.get("sample_rate", 0)) if audio_stream else 0,
        bitrate=int(format_info.get("bit_rate", 0)),
        file_size=int(format_info.get("size", 0)),
        format_name=format_info.get("format_name", "")
    )
