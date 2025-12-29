"""
Recipe Runtime - Shared utilities for all Agent-Recipes.

Provides:
- Output directory management
- run.json generation
- Logging setup
- Dry-run support
- Safety defaults
"""

from .core import (
    RecipeRunner,
    RecipeConfig,
    RecipeResult,
    create_output_dir,
    write_run_json,
    setup_logging,
)

__all__ = [
    "RecipeRunner",
    "RecipeConfig",
    "RecipeResult",
    "create_output_dir",
    "write_run_json",
    "setup_logging",
]
