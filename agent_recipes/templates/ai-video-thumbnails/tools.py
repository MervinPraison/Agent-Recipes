"""
Tools for ai-video-thumbnails recipe.
Uses VisionAgent for frame analysis and ImageAgent for thumbnail generation.
"""

from praisonaiagents import VisionAgent, ImageAgent
from praisonaiagents.tools import execute_command
import os

_vision_agent = None
_image_agent = None

def _get_vision_agent():
    global _vision_agent
    if _vision_agent is None:
        _vision_agent = VisionAgent(llm="gpt-4o")
    return _vision_agent

def _get_image_agent():
    global _image_agent
    if _image_agent is None:
        _image_agent = ImageAgent(llm="dall-e-3")
    return _image_agent


def extract_video_frames(video_path: str, output_dir: str = "frames", count: int = 10) -> str:
    """
    Extract frames from video at even intervals.
    
    Args:
        video_path: Path to video file
        output_dir: Directory to save frames
        count: Number of frames to extract
        
    Returns:
        List of frame file paths
    """
    os.makedirs(output_dir, exist_ok=True)
    
    # Use ffmpeg to extract frames
    result = execute_command(
        f"ffmpeg -i '{video_path}' -vf 'fps=1/{count}:round=down' '{output_dir}/frame_%03d.jpg'"
    )
    
    if result.get("return_code", 1) == 0:
        frames = sorted([f"{output_dir}/{f}" for f in os.listdir(output_dir) if f.endswith('.jpg')])
        return str(frames)
    return f"Error: {result.get('stderr', 'Failed to extract frames')}"


def analyze_frame(frame_path: str) -> str:
    """
    Analyze a video frame for thumbnail potential.
    
    Args:
        frame_path: Path to frame image
        
    Returns:
        Analysis of frame quality and content
    """
    agent = _get_vision_agent()
    return agent.analyze(
        frame_path,
        prompt="""Analyze this video frame for thumbnail potential. Rate on:
- Visual appeal (1-10)
- Subject clarity (1-10)  
- Color vibrancy (1-10)
- Emotion/interest capture (1-10)
Return: scores, description, and thumbnail recommendation."""
    )


def find_best_thumbnail(frames: list) -> str:
    """
    Compare multiple frames to find the best thumbnail.
    
    Args:
        frames: List of frame file paths
        
    Returns:
        Best frame selection with reasoning
    """
    agent = _get_vision_agent()
    return agent.compare(
        frames[:5],  # Compare up to 5 frames
        prompt="Which of these video frames would make the best thumbnail? Consider visual appeal, clarity, and engagement. Choose the best one and explain why."
    )


def generate_custom_thumbnail(prompt: str, size: str = "1280x720") -> str:
    """
    Generate a custom thumbnail based on video content.
    
    Args:
        prompt: Description of desired thumbnail
        size: Thumbnail dimensions
        
    Returns:
        URL or path to generated thumbnail
    """
    agent = _get_image_agent()
    result = agent.generate(prompt, size=size)
    return result.data[0].url if hasattr(result, 'data') else str(result)


def add_text_overlay(image_path: str, text: str, output_path: str = "thumbnail.jpg") -> str:
    """
    Add text overlay to thumbnail using ImageMagick.
    
    Args:
        image_path: Path to base image
        text: Text to overlay
        output_path: Output file path
        
    Returns:
        Path to processed thumbnail
    """
    result = execute_command(
        f"convert '{image_path}' -gravity south -background '#00000080' -fill white "
        f"-font Arial -pointsize 48 -annotate +0+20 '{text}' '{output_path}'"
    )
    return output_path if result.get("return_code", 1) == 0 else f"Error: {result.get('stderr')}"


TOOLS = [extract_video_frames, analyze_frame, find_best_thumbnail, generate_custom_thumbnail, add_text_overlay]


def get_all_tools():
    return TOOLS
