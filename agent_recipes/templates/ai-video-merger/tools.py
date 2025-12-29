"""
AI Video Merger Tools

Merge and sync audio with video:
- Audio/video merging
- Track synchronization
- Audio normalization
"""

import logging
import os
import subprocess
from datetime import datetime
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)


def merge_audio_video(
    video_path: str,
    audio_path: str,
    output_path: Optional[str] = None,
    replace_audio: bool = True,
    normalize: bool = True,
) -> Dict[str, Any]:
    """
    Merge audio track with video.
    
    Args:
        video_path: Path to video file
        audio_path: Path to audio file
        output_path: Output file path
        replace_audio: Replace existing audio
        normalize: Normalize audio levels
        
    Returns:
        Dictionary with output info
    """
    if not os.path.exists(video_path):
        return {"error": f"Video not found: {video_path}"}
    if not os.path.exists(audio_path):
        return {"error": f"Audio not found: {audio_path}"}
    
    if not output_path:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = f"merged_{timestamp}.mp4"
    
    try:
        if replace_audio:
            # Replace audio entirely
            cmd = [
                "ffmpeg", "-y",
                "-i", video_path,
                "-i", audio_path,
                "-c:v", "copy",
                "-c:a", "aac",
                "-map", "0:v:0",
                "-map", "1:a:0",
                "-shortest",
                output_path
            ]
        else:
            # Mix audio tracks
            cmd = [
                "ffmpeg", "-y",
                "-i", video_path,
                "-i", audio_path,
                "-filter_complex", "[0:a][1:a]amix=inputs=2:duration=first[a]",
                "-c:v", "copy",
                "-map", "0:v:0",
                "-map", "[a]",
                output_path
            ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            logger.warning(f"FFmpeg stderr: {result.stderr}")
        
        if os.path.exists(output_path):
            return {
                "path": output_path,
                "video_source": video_path,
                "audio_source": audio_path,
                "size_bytes": os.path.getsize(output_path),
            }
        else:
            return {"error": "Output file not created"}
        
    except Exception as e:
        logger.error(f"Error merging: {e}")
        return {"error": str(e)}


def sync_tracks(
    video_path: str,
    audio_path: str,
    output_path: Optional[str] = None,
    audio_offset: float = 0.0,
) -> Dict[str, Any]:
    """
    Sync audio track with video with offset adjustment.
    
    Args:
        video_path: Path to video file
        audio_path: Path to audio file
        output_path: Output file path
        audio_offset: Audio offset in seconds (positive = delay audio)
        
    Returns:
        Dictionary with output info
    """
    if not output_path:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = f"synced_{timestamp}.mp4"
    
    try:
        if audio_offset >= 0:
            # Delay audio
            cmd = [
                "ffmpeg", "-y",
                "-i", video_path,
                "-itsoffset", str(audio_offset),
                "-i", audio_path,
                "-c:v", "copy",
                "-c:a", "aac",
                "-map", "0:v:0",
                "-map", "1:a:0",
                "-shortest",
                output_path
            ]
        else:
            # Delay video (advance audio)
            cmd = [
                "ffmpeg", "-y",
                "-itsoffset", str(-audio_offset),
                "-i", video_path,
                "-i", audio_path,
                "-c:v", "copy",
                "-c:a", "aac",
                "-map", "0:v:0",
                "-map", "1:a:0",
                "-shortest",
                output_path
            ]
        
        subprocess.run(cmd, capture_output=True, check=True)
        
        return {
            "path": output_path,
            "audio_offset": audio_offset,
        }
        
    except Exception as e:
        logger.error(f"Error syncing: {e}")
        return {"error": str(e)}


def get_duration(file_path: str) -> float:
    """Get duration of audio/video file in seconds."""
    try:
        cmd = [
            "ffprobe",
            "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            file_path
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return float(result.stdout.strip())
    except Exception:
        return 0.0
