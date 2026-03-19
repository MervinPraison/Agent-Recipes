"""
Tools for ai-image-captioner recipe.
Uses VisionAgent for intelligent image analysis and captioning.
"""

from praisonaiagents import VisionAgent

# Lazy-load the vision agent
_vision_agent = None

def _get_vision_agent():
    global _vision_agent
    if _vision_agent is None:
        _vision_agent = VisionAgent(llm="gpt-4o")
    return _vision_agent


def caption_image(image_path: str) -> str:
    """
    Generate a detailed caption for an image.
    
    Args:
        image_path: Path to the image file or URL
        
    Returns:
        Detailed caption describing the image
    """
    agent = _get_vision_agent()
    return agent.describe(image_path)


def analyze_image(image_path: str, prompt: str = None) -> str:
    """
    Analyze an image with optional custom prompt.
    
    Args:
        image_path: Path to the image file or URL
        prompt: Optional custom analysis prompt
        
    Returns:
        Analysis of the image
    """
    agent = _get_vision_agent()
    return agent.analyze(image_path, prompt=prompt)


def extract_text_from_image(image_path: str) -> str:
    """
    Extract any visible text from an image (OCR-like).
    
    Args:
        image_path: Path to the image file or URL
        
    Returns:
        Extracted text from the image
    """
    agent = _get_vision_agent()
    return agent.extract_text(image_path, detail="high")


# Export tools for recipe
TOOLS = [caption_image, analyze_image, extract_text_from_image]


def get_all_tools():
    """Get all tools defined in this recipe."""
    return TOOLS
