"""
Tools for ai-image-cataloger recipe.
Uses VisionAgent for image analysis and file tools for organization.
"""

from praisonaiagents import VisionAgent
from praisonaiagents.tools import read_file, list_files
import os
import json

_vision_agent = None

def _get_vision_agent():
    global _vision_agent
    if _vision_agent is None:
        _vision_agent = VisionAgent(llm="gpt-4o")
    return _vision_agent


def analyze_image_for_catalog(image_path: str) -> str:
    """
    Analyze an image and return structured catalog metadata.
    
    Args:
        image_path: Path to the image file
        
    Returns:
        JSON string with catalog metadata
    """
    agent = _get_vision_agent()
    result = agent.analyze(
        image_path,
        prompt="""Analyze this image and return JSON metadata for cataloging:
{
    "title": "descriptive title",
    "description": "one sentence description",
    "tags": ["tag1", "tag2", "tag3"],
    "category": "Nature|Portrait|Architecture|Food|Product|Art|Technology|Other",
    "dominant_colors": ["color1", "color2"],
    "mood": "happy|sad|calm|energetic|neutral",
    "has_text": true/false,
    "has_people": true/false
}
Return only valid JSON."""
    )
    return result


def list_images_in_directory(directory: str) -> str:
    """
    List all image files in a directory.
    
    Args:
        directory: Path to directory
        
    Returns:
        List of image file paths
    """
    image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.tiff'}
    images = []
    
    for root, _, files in os.walk(directory):
        for file in files:
            if os.path.splitext(file)[1].lower() in image_extensions:
                images.append(os.path.join(root, file))
    
    return json.dumps(images, indent=2)


def compare_images(image1: str, image2: str) -> str:
    """
    Compare two images for similarity.
    
    Args:
        image1: Path to first image
        image2: Path to second image
        
    Returns:
        Comparison analysis
    """
    agent = _get_vision_agent()
    return agent.compare([image1, image2], prompt="Compare these two images. Are they similar? What are the key differences?")


TOOLS = [analyze_image_for_catalog, list_images_in_directory, compare_images]


def get_all_tools():
    return TOOLS
