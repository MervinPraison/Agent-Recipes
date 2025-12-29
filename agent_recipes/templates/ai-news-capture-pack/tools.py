"""
AI News Capture Pack Tools

Bundle assets per news story:
- Screenshots
- Metadata
- Source links
"""

import json
import logging
import os
import shutil
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


def capture_story_assets(
    urls: List[str],
    story_id: str,
    output_dir: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Capture all assets for a news story.
    
    Args:
        urls: List of URLs to capture
        story_id: Unique story identifier
        output_dir: Output directory
        
    Returns:
        Dictionary with captured assets
    """
    output_dir = output_dir or f"./captures/{story_id}"
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    assets = []
    
    try:
        from playwright.sync_api import sync_playwright
        
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(viewport={"width": 1920, "height": 1080})
            
            for i, url in enumerate(urls):
                try:
                    page.goto(url, wait_until="networkidle", timeout=30000)
                    
                    # Capture screenshot
                    screenshot_path = os.path.join(output_dir, f"capture_{i}.png")
                    page.screenshot(path=screenshot_path, full_page=True)
                    
                    # Extract metadata
                    title = page.title()
                    
                    assets.append({
                        "url": url,
                        "screenshot": screenshot_path,
                        "title": title,
                        "captured_at": datetime.now(timezone.utc).isoformat(),
                    })
                    
                except Exception as e:
                    logger.warning(f"Error capturing {url}: {e}")
                    assets.append({
                        "url": url,
                        "error": str(e),
                    })
            
            browser.close()
            
    except ImportError:
        logger.error("Playwright not installed")
        return {"error": "Playwright not installed"}
    
    return {
        "story_id": story_id,
        "assets": assets,
        "output_dir": output_dir,
        "total_captured": len([a for a in assets if "screenshot" in a]),
    }


def create_bundle(
    story_id: str,
    assets: List[Dict[str, Any]],
    output_dir: Optional[str] = None,
    include_metadata: bool = True,
) -> Dict[str, Any]:
    """
    Create a bundled pack of story assets.
    
    Args:
        story_id: Story identifier
        assets: List of asset dictionaries
        output_dir: Output directory
        include_metadata: Include metadata JSON
        
    Returns:
        Bundle info
    """
    output_dir = output_dir or "./bundles"
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    bundle_name = f"{story_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    bundle_dir = os.path.join(output_dir, bundle_name)
    Path(bundle_dir).mkdir(parents=True, exist_ok=True)
    
    bundled_files = []
    
    # Copy assets to bundle
    for asset in assets:
        if "screenshot" in asset and os.path.exists(asset["screenshot"]):
            filename = os.path.basename(asset["screenshot"])
            dest = os.path.join(bundle_dir, filename)
            shutil.copy2(asset["screenshot"], dest)
            bundled_files.append(filename)
    
    # Create metadata
    if include_metadata:
        metadata = {
            "story_id": story_id,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "assets": assets,
            "files": bundled_files,
        }
        metadata_path = os.path.join(bundle_dir, "metadata.json")
        with open(metadata_path, "w") as f:
            json.dump(metadata, f, indent=2)
    
    # Create zip
    zip_path = f"{bundle_dir}.zip"
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(bundle_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, bundle_dir)
                zf.write(file_path, arcname)
    
    return {
        "bundle_path": zip_path,
        "bundle_dir": bundle_dir,
        "files": bundled_files,
        "size_bytes": os.path.getsize(zip_path),
    }
