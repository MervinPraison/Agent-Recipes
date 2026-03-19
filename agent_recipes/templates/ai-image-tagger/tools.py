"""
Tools for ai-image-tagger recipe.
Uses VisionAgent for intelligent image tagging and categorization.
"""

from praisonaiagents import VisionAgent

_vision_agent = None

def _get_vision_agent():
    global _vision_agent
    if _vision_agent is None:
        _vision_agent = VisionAgent(llm="gpt-4o")
    return _vision_agent


def tag_image(image_path: str) -> str:
    """
    Generate relevant tags for an image.
    
    Args:
        image_path: Path to the image file or URL
        
    Returns:
        Comma-separated list of tags
    """
    agent = _get_vision_agent()
    return agent.analyze(
        image_path, 
        prompt="List relevant tags for this image. Return as comma-separated keywords covering: subject, style, colors, mood, objects, setting. Format: tag1, tag2, tag3..."
    )


def categorize_image(image_path: str) -> str:
    """
    Categorize an image into predefined categories.
    
    Args:
        image_path: Path to the image file or URL
        
    Returns:
        Category and confidence
    """
    agent = _get_vision_agent()
    return agent.analyze(
        image_path,
        prompt="Categorize this image. Categories: Nature, Portrait, Architecture, Food, Product, Art, Technology, Sports, Travel, Abstract, Other. Return: category name and confidence (high/medium/low)."
    )


def describe_for_alt_text(image_path: str) -> str:
    """
    Generate accessibility-friendly alt text for an image.
    
    Args:
        image_path: Path to the image file or URL
        
    Returns:
        Concise alt text suitable for screen readers
    """
    agent = _get_vision_agent()
    return agent.analyze(
        image_path,
        prompt="Write concise alt text for this image (max 125 characters) that describes the key content for screen reader users."
    )


TOOLS = [tag_image, categorize_image, describe_for_alt_text]


def get_all_tools():
    return TOOLS
