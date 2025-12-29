"""
AI B-roll Builder Tools

Create B-roll video with:
- Ken Burns effect
- Pan and zoom
- Crossfade transitions
"""

import logging
import os
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


def create_ken_burns(
    image_path: str,
    output_path: str,
    duration: float = 5.0,
    zoom_start: float = 1.0,
    zoom_end: float = 1.2,
    pan_x: float = 0.0,
    pan_y: float = 0.0,
) -> Dict[str, Any]:
    """
    Apply Ken Burns effect to an image.
    
    Args:
        image_path: Path to input image
        output_path: Path to output video
        duration: Duration in seconds
        zoom_start: Starting zoom level
        zoom_end: Ending zoom level
        pan_x: Horizontal pan (-1 to 1)
        pan_y: Vertical pan (-1 to 1)
        
    Returns:
        Dictionary with output info
    """
    try:
        # Use ffmpeg for Ken Burns effect
        zoom_expr = f"zoom+{(zoom_end - zoom_start) / (duration * 25)}"
        
        cmd = [
            "ffmpeg", "-y",
            "-loop", "1",
            "-i", image_path,
            "-vf", f"scale=8000:-1,zoompan=z='{zoom_expr}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={int(duration * 25)}:s=1920x1080:fps=25",
            "-c:v", "libx264",
            "-t", str(duration),
            "-pix_fmt", "yuv420p",
            output_path
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            logger.warning(f"FFmpeg warning: {result.stderr}")
        
        return {
            "path": output_path,
            "duration": duration,
            "effect": "ken_burns",
        }
        
    except Exception as e:
        logger.error(f"Error creating Ken Burns: {e}")
        return {"error": str(e)}


def apply_pan_zoom(
    image_path: str,
    output_path: str,
    duration: float = 5.0,
    effect: str = "zoom_in",
) -> Dict[str, Any]:
    """
    Apply pan or zoom effect to image.
    
    Args:
        image_path: Input image path
        output_path: Output video path
        duration: Duration in seconds
        effect: Effect type (zoom_in, zoom_out, pan_left, pan_right)
        
    Returns:
        Dictionary with output info
    """
    effects = {
        "zoom_in": "zoompan=z='zoom+0.001':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'",
        "zoom_out": "zoompan=z='1.5-on*0.001':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'",
        "pan_left": "zoompan=z='1.1':x='iw*on/100':y='ih/2-(ih/zoom/2)'",
        "pan_right": "zoompan=z='1.1':x='iw-iw*on/100':y='ih/2-(ih/zoom/2)'",
    }
    
    filter_expr = effects.get(effect, effects["zoom_in"])
    
    try:
        cmd = [
            "ffmpeg", "-y",
            "-loop", "1",
            "-i", image_path,
            "-vf", f"scale=4000:-1,{filter_expr}:d={int(duration * 25)}:s=1920x1080:fps=25",
            "-c:v", "libx264",
            "-t", str(duration),
            "-pix_fmt", "yuv420p",
            output_path
        ]
        
        subprocess.run(cmd, capture_output=True, check=True)
        
        return {
            "path": output_path,
            "duration": duration,
            "effect": effect,
        }
        
    except Exception as e:
        logger.error(f"Error applying effect: {e}")
        return {"error": str(e)}


def build_broll(
    images: List[str],
    output_path: Optional[str] = None,
    duration_per_image: float = 5.0,
    transition: str = "crossfade",
    transition_duration: float = 0.5,
) -> Dict[str, Any]:
    """
    Build B-roll video from multiple images.
    
    Args:
        images: List of image paths
        output_path: Output video path
        duration_per_image: Duration per image
        transition: Transition type
        transition_duration: Transition duration
        
    Returns:
        Dictionary with output info
    """
    import tempfile
    
    if not output_path:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = f"broll_{timestamp}.mp4"
    
    if not images:
        return {"error": "No images provided"}
    
    with tempfile.TemporaryDirectory() as temp_dir:
        clips = []
        effects = ["zoom_in", "zoom_out", "pan_left", "pan_right"]
        
        # Create individual clips with effects
        for i, image in enumerate(images):
            if not os.path.exists(image):
                logger.warning(f"Image not found: {image}")
                continue
            
            clip_path = os.path.join(temp_dir, f"clip_{i:03d}.mp4")
            effect = effects[i % len(effects)]
            
            result = apply_pan_zoom(image, clip_path, duration_per_image, effect)
            if "path" in result:
                clips.append(result["path"])
        
        if not clips:
            return {"error": "No clips created"}
        
        # Create concat file
        concat_file = os.path.join(temp_dir, "concat.txt")
        with open(concat_file, "w") as f:
            for clip in clips:
                f.write(f"file '{clip}'\n")
        
        # Concatenate clips
        try:
            cmd = [
                "ffmpeg", "-y",
                "-f", "concat",
                "-safe", "0",
                "-i", concat_file,
                "-c:v", "libx264",
                "-pix_fmt", "yuv420p",
                output_path
            ]
            
            subprocess.run(cmd, capture_output=True, check=True)
            
            return {
                "path": output_path,
                "clips": len(clips),
                "total_duration": len(clips) * duration_per_image,
            }
            
        except Exception as e:
            logger.error(f"Error building B-roll: {e}")
            return {"error": str(e)}
