"""
AI Screenshot Capture Tools

High-resolution screenshot capture with:
- Full page capture
- Element highlighting
- Auto-scroll
- Multiple format support
"""

import logging
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


def capture_screenshot(
    url: str,
    output_path: Optional[str] = None,
    width: int = 1920,
    height: int = 1080,
    full_page: bool = False,
    quality: int = 95,
) -> Dict[str, Any]:
    """
    Capture a screenshot of a URL.
    
    Args:
        url: URL to capture
        output_path: Path to save screenshot
        width: Viewport width
        height: Viewport height
        full_page: Capture full page
        quality: Image quality (1-100)
        
    Returns:
        Dictionary with screenshot info
    """
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        logger.error("Playwright not installed. Run: pip install playwright && playwright install")
        return {"error": "Playwright not installed"}
    
    if not output_path:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = f"screenshot_{timestamp}.png"
    
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(viewport={"width": width, "height": height})
            page.goto(url, wait_until="networkidle")
            
            page.screenshot(
                path=output_path,
                full_page=full_page,
                quality=quality if output_path.endswith(".jpg") else None,
            )
            
            browser.close()
        
        return {
            "path": output_path,
            "url": url,
            "width": width,
            "height": height,
            "full_page": full_page,
            "captured_at": datetime.now(timezone.utc).isoformat(),
        }
        
    except Exception as e:
        logger.error(f"Error capturing screenshot: {e}")
        return {"error": str(e)}


def capture_full_page(
    url: str,
    output_dir: Optional[str] = None,
    scroll_delay: float = 0.5,
) -> Dict[str, Any]:
    """
    Capture full page with auto-scroll.
    
    Args:
        url: URL to capture
        output_dir: Directory to save screenshots
        scroll_delay: Delay between scrolls
        
    Returns:
        Dictionary with capture info
    """
    output_dir = output_dir or "./screenshots"
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = os.path.join(output_dir, f"fullpage_{timestamp}.png")
    
    return capture_screenshot(url, output_path, full_page=True)


def highlight_and_capture(
    url: str,
    selectors: List[str],
    output_dir: Optional[str] = None,
    highlight_color: str = "yellow",
) -> Dict[str, Any]:
    """
    Highlight elements and capture screenshots.
    
    Args:
        url: URL to capture
        selectors: CSS selectors to highlight
        output_dir: Directory to save screenshots
        highlight_color: Highlight color
        
    Returns:
        Dictionary with captures
    """
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        return {"error": "Playwright not installed"}
    
    output_dir = output_dir or "./screenshots"
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    captures = []
    
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(viewport={"width": 1920, "height": 1080})
            page.goto(url, wait_until="networkidle")
            
            for i, selector in enumerate(selectors):
                try:
                    # Add highlight style
                    page.evaluate(f"""
                        const el = document.querySelector('{selector}');
                        if (el) {{
                            el.style.backgroundColor = '{highlight_color}';
                            el.style.outline = '3px solid red';
                        }}
                    """)
                    
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    output_path = os.path.join(output_dir, f"highlight_{i}_{timestamp}.png")
                    
                    page.screenshot(path=output_path)
                    
                    captures.append({
                        "path": output_path,
                        "selector": selector,
                    })
                    
                    # Remove highlight
                    page.evaluate(f"""
                        const el = document.querySelector('{selector}');
                        if (el) {{
                            el.style.backgroundColor = '';
                            el.style.outline = '';
                        }}
                    """)
                    
                except Exception as e:
                    logger.warning(f"Error highlighting {selector}: {e}")
            
            browser.close()
        
        return {
            "captures": captures,
            "url": url,
            "total": len(captures),
        }
        
    except Exception as e:
        logger.error(f"Error in highlight capture: {e}")
        return {"error": str(e)}


def bundle_captures(
    captures: List[Dict[str, Any]],
    output_dir: str,
    bundle_name: str = "capture_pack",
) -> Dict[str, Any]:
    """
    Bundle multiple captures into a pack.
    
    Args:
        captures: List of capture dictionaries
        output_dir: Output directory
        bundle_name: Name for the bundle
        
    Returns:
        Bundle info
    """
    import json
    import shutil
    
    bundle_dir = os.path.join(output_dir, bundle_name)
    Path(bundle_dir).mkdir(parents=True, exist_ok=True)
    
    manifest = {
        "name": bundle_name,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "files": [],
    }
    
    for capture in captures:
        if "path" in capture and os.path.exists(capture["path"]):
            filename = os.path.basename(capture["path"])
            dest = os.path.join(bundle_dir, filename)
            shutil.copy2(capture["path"], dest)
            manifest["files"].append({
                "filename": filename,
                "original": capture.get("url", ""),
            })
    
    manifest_path = os.path.join(bundle_dir, "manifest.json")
    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=2)
    
    return {
        "bundle_dir": bundle_dir,
        "manifest": manifest,
        "file_count": len(manifest["files"]),
    }
