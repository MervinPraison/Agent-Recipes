"""
AI Publisher Pack Tools

Create cross-platform publishing packs:
- Platform-specific metadata
- Optimized assets
- Ready-to-upload bundles
"""

import json
import logging
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


def create_publisher_pack(
    content: Dict[str, Any],
    platforms: Optional[List[str]] = None,
    output_dir: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Create a publisher pack for multiple platforms.
    
    Args:
        content: Content dictionary with title, description, video, etc.
        platforms: Target platforms
        output_dir: Output directory
        
    Returns:
        Dictionary with pack info
    """
    platforms = platforms or ["youtube", "x", "linkedin"]
    output_dir = output_dir or "./publisher_packs"
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    pack_dir = os.path.join(output_dir, f"pack_{timestamp}")
    Path(pack_dir).mkdir(parents=True, exist_ok=True)
    
    packs = []
    
    for platform in platforms:
        platform_dir = os.path.join(pack_dir, platform)
        Path(platform_dir).mkdir(parents=True, exist_ok=True)
        
        # Generate platform-specific metadata
        metadata = generate_platform_metadata(content, platform)
        
        # Save metadata
        metadata_path = os.path.join(platform_dir, "metadata.json")
        with open(metadata_path, "w") as f:
            json.dump(metadata, f, indent=2)
        
        # Create upload instructions
        instructions = generate_upload_instructions(platform, metadata)
        instructions_path = os.path.join(platform_dir, "UPLOAD_INSTRUCTIONS.md")
        with open(instructions_path, "w") as f:
            f.write(instructions)
        
        packs.append({
            "platform": platform,
            "directory": platform_dir,
            "metadata": metadata,
        })
    
    # Create master manifest
    manifest = {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "platforms": platforms,
        "packs": [{
            "platform": p["platform"],
            "directory": p["directory"],
        } for p in packs],
    }
    
    manifest_path = os.path.join(pack_dir, "manifest.json")
    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=2)
    
    return {
        "pack_dir": pack_dir,
        "packs": packs,
        "manifest": manifest_path,
    }


def generate_platform_metadata(
    content: Dict[str, Any],
    platform: str,
) -> Dict[str, Any]:
    """
    Generate platform-specific metadata.
    
    Args:
        content: Source content
        platform: Target platform
        
    Returns:
        Platform-specific metadata
    """
    title = content.get("title", "Untitled")
    description = content.get("description", "")
    tags = content.get("tags", [])
    
    platform_configs = {
        "youtube": {
            "title": title[:100],
            "description": description[:5000],
            "tags": tags[:500],
            "category": content.get("category", "22"),  # People & Blogs
            "privacy": "public",
            "made_for_kids": False,
        },
        "x": {
            "text": f"{title}\n\n{description[:200]}",
            "hashtags": [f"#{t}" for t in tags[:5]],
            "max_length": 280,
        },
        "linkedin": {
            "title": title[:200],
            "text": description[:3000],
            "hashtags": [f"#{t}" for t in tags[:5]],
        },
        "instagram": {
            "caption": f"{title}\n\n{description[:2000]}",
            "hashtags": [f"#{t}" for t in tags[:30]],
        },
        "tiktok": {
            "caption": f"{title} {' '.join([f'#{t}' for t in tags[:5]])}",
            "max_length": 150,
        },
    }
    
    return platform_configs.get(platform, {"title": title, "description": description})


def generate_upload_instructions(
    platform: str,
    metadata: Dict[str, Any],
) -> str:
    """
    Generate upload instructions for a platform.
    
    Args:
        platform: Target platform
        metadata: Platform metadata
        
    Returns:
        Markdown instructions
    """
    instructions = {
        "youtube": f"""# YouTube Upload Instructions

1. Go to YouTube Studio: https://studio.youtube.com
2. Click "Create" > "Upload videos"
3. Select your video file
4. Fill in the following:

**Title:** {metadata.get('title', '')}

**Description:**
{metadata.get('description', '')}

**Tags:** {', '.join(metadata.get('tags', [])[:10])}

5. Set visibility to: {metadata.get('privacy', 'public')}
6. Click "Publish"
""",
        "x": f"""# X (Twitter) Post Instructions

1. Go to X: https://x.com/compose/tweet
2. Paste the following text:

{metadata.get('text', '')}

3. Attach your media file
4. Click "Post"
""",
        "linkedin": f"""# LinkedIn Post Instructions

1. Go to LinkedIn: https://www.linkedin.com/feed/
2. Click "Start a post"
3. Paste the following:

{metadata.get('title', '')}

{metadata.get('text', '')}

{' '.join(metadata.get('hashtags', []))}

4. Add your media
5. Click "Post"
""",
    }
    
    return instructions.get(platform, f"# {platform.title()} Upload\n\nUpload your content to {platform}.")


def generate_platform_assets(
    video_path: str,
    platforms: List[str],
    output_dir: str,
) -> Dict[str, Any]:
    """
    Generate platform-optimized video assets.
    
    Args:
        video_path: Source video path
        platforms: Target platforms
        output_dir: Output directory
        
    Returns:
        Dictionary with generated assets
    """
    import subprocess
    
    assets = []
    
    platform_specs = {
        "youtube": {"resolution": "1920x1080", "aspect": "16:9"},
        "instagram": {"resolution": "1080x1080", "aspect": "1:1"},
        "tiktok": {"resolution": "1080x1920", "aspect": "9:16"},
        "x": {"resolution": "1280x720", "aspect": "16:9"},
    }
    
    for platform in platforms:
        spec = platform_specs.get(platform, platform_specs["youtube"])
        output_path = os.path.join(output_dir, f"{platform}_video.mp4")
        
        try:
            cmd = [
                "ffmpeg", "-y",
                "-i", video_path,
                "-vf", f"scale={spec['resolution'].replace('x', ':')}:force_original_aspect_ratio=decrease,pad={spec['resolution'].replace('x', ':')}:(ow-iw)/2:(oh-ih)/2",
                "-c:v", "libx264",
                "-c:a", "aac",
                output_path
            ]
            subprocess.run(cmd, capture_output=True, check=True)
            
            assets.append({
                "platform": platform,
                "path": output_path,
                "spec": spec,
            })
        except Exception as e:
            logger.warning(f"Error creating {platform} asset: {e}")
    
    return {"assets": assets}
