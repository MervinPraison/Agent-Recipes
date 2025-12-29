"""
AI Screen Recorder Tools

Record browser navigation with:
- Configurable FPS
- Action scripting
- Video output
"""

import logging
import os
import subprocess
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


def record_navigation(
    url: str,
    output_path: Optional[str] = None,
    duration: int = 30,
    fps: int = 10,
    width: int = 1920,
    height: int = 1080,
) -> Dict[str, Any]:
    """
    Record browser navigation as video.
    
    Args:
        url: URL to record
        output_path: Output video path
        duration: Recording duration in seconds
        fps: Frames per second
        width: Viewport width
        height: Viewport height
        
    Returns:
        Dictionary with recording info
    """
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        return {"error": "Playwright not installed"}
    
    if not output_path:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = f"recording_{timestamp}.mp4"
    
    # Create temp directory for frames
    with tempfile.TemporaryDirectory() as temp_dir:
        frames = []
        
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page(viewport={"width": width, "height": height})
                page.goto(url, wait_until="networkidle")
                
                # Capture frames
                import time
                frame_interval = 1.0 / fps
                total_frames = duration * fps
                
                for i in range(min(total_frames, 300)):  # Cap at 300 frames
                    frame_path = os.path.join(temp_dir, f"frame_{i:05d}.png")
                    page.screenshot(path=frame_path)
                    frames.append(frame_path)
                    
                    # Scroll slowly
                    page.evaluate("window.scrollBy(0, 50)")
                    time.sleep(frame_interval)
                
                browser.close()
            
            # Combine frames with ffmpeg
            if frames:
                frame_pattern = os.path.join(temp_dir, "frame_%05d.png")
                cmd = [
                    "ffmpeg", "-y",
                    "-framerate", str(fps),
                    "-i", frame_pattern,
                    "-c:v", "libx264",
                    "-pix_fmt", "yuv420p",
                    output_path
                ]
                subprocess.run(cmd, capture_output=True, check=True)
            
            return {
                "path": output_path,
                "url": url,
                "duration": len(frames) / fps,
                "fps": fps,
                "frames": len(frames),
            }
            
        except Exception as e:
            logger.error(f"Error recording: {e}")
            return {"error": str(e)}


def record_actions(
    url: str,
    actions: List[Dict[str, Any]],
    output_path: Optional[str] = None,
    fps: int = 10,
) -> Dict[str, Any]:
    """
    Record scripted browser actions.
    
    Args:
        url: Starting URL
        actions: List of actions to perform
        output_path: Output video path
        fps: Frames per second
        
    Returns:
        Dictionary with recording info
    """
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        return {"error": "Playwright not installed"}
    
    if not output_path:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = f"actions_{timestamp}.mp4"
    
    with tempfile.TemporaryDirectory() as temp_dir:
        frames = []
        frame_count = 0
        
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page(viewport={"width": 1920, "height": 1080})
                page.goto(url, wait_until="networkidle")
                
                import time
                
                for action in actions:
                    action_type = action.get("type", "wait")
                    
                    if action_type == "click":
                        page.click(action.get("selector", "body"))
                    elif action_type == "scroll":
                        page.evaluate(f"window.scrollBy(0, {action.get('amount', 100)})")
                    elif action_type == "wait":
                        time.sleep(action.get("duration", 1))
                    elif action_type == "goto":
                        page.goto(action.get("url", url))
                    
                    # Capture frame after action
                    frame_path = os.path.join(temp_dir, f"frame_{frame_count:05d}.png")
                    page.screenshot(path=frame_path)
                    frames.append(frame_path)
                    frame_count += 1
                
                browser.close()
            
            # Combine frames
            if frames:
                frame_pattern = os.path.join(temp_dir, "frame_%05d.png")
                cmd = [
                    "ffmpeg", "-y",
                    "-framerate", str(fps),
                    "-i", frame_pattern,
                    "-c:v", "libx264",
                    "-pix_fmt", "yuv420p",
                    output_path
                ]
                subprocess.run(cmd, capture_output=True, check=True)
            
            return {
                "path": output_path,
                "actions_performed": len(actions),
                "frames": len(frames),
            }
            
        except Exception as e:
            logger.error(f"Error recording actions: {e}")
            return {"error": str(e)}
