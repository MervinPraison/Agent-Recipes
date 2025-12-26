"""
Agent Recipes - Real-world AI agent templates for PraisonAI

This package provides ready-to-use templates for common AI agent workflows.
"""

__version__ = "0.1.0"
__all__ = ["get_template_path", "list_templates"]

from pathlib import Path


def get_template_path(template_name: str) -> Path:
    """Get the path to a template directory."""
    templates_dir = Path(__file__).parent / "templates"
    template_path = templates_dir / template_name
    if not template_path.exists():
        raise ValueError(f"Template not found: {template_name}")
    return template_path


def list_templates() -> list:
    """List all available templates."""
    templates_dir = Path(__file__).parent / "templates"
    if not templates_dir.exists():
        return []
    return [d.name for d in templates_dir.iterdir() if d.is_dir() and not d.name.startswith(".")]
