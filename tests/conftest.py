"""
Pytest configuration and fixtures for Agent Recipes tests.
"""

import os
import pytest
from pathlib import Path


def pytest_addoption(parser):
    """Add custom command line options."""
    parser.addoption(
        "--run-smoke",
        action="store_true",
        default=False,
        help="Run smoke tests that require real API keys",
    )


def pytest_configure(config):
    """Configure custom markers."""
    config.addinivalue_line(
        "markers", "smoke: mark test as smoke test (requires real API keys)"
    )
    config.addinivalue_line(
        "markers", "integration: mark test as integration test"
    )


def pytest_collection_modifyitems(config, items):
    """Skip smoke tests unless --run-smoke is specified."""
    if config.getoption("--run-smoke"):
        return
    
    skip_smoke = pytest.mark.skip(reason="need --run-smoke option to run")
    for item in items:
        if "smoke" in item.keywords:
            item.add_marker(skip_smoke)


@pytest.fixture
def has_openai_key():
    """Check if OPENAI_API_KEY is available."""
    return bool(os.environ.get("OPENAI_API_KEY"))


@pytest.fixture
def has_tavily_key():
    """Check if TAVILY_API_KEY is available."""
    return bool(os.environ.get("TAVILY_API_KEY"))


@pytest.fixture
def has_anthropic_key():
    """Check if ANTHROPIC_API_KEY is available."""
    return bool(os.environ.get("ANTHROPIC_API_KEY"))


@pytest.fixture
def templates_dir():
    """Get the templates directory path."""
    return Path(__file__).parent.parent / "agent_recipes" / "templates"


@pytest.fixture
def temp_output_dir(tmp_path):
    """Create a temporary output directory."""
    output_dir = tmp_path / "outputs"
    output_dir.mkdir()
    return output_dir


@pytest.fixture
def sample_news_data():
    """Sample news data for testing."""
    return {
        "articles": [
            {
                "title": "OpenAI Releases GPT-5",
                "url": "https://example.com/gpt5",
                "source": "TechCrunch",
                "published": "2024-12-29T10:00:00Z",
                "content": "OpenAI has announced the release of GPT-5...",
            },
            {
                "title": "Google Announces Gemini 2.0",
                "url": "https://example.com/gemini2",
                "source": "The Verge",
                "published": "2024-12-29T09:00:00Z",
                "content": "Google has unveiled Gemini 2.0...",
            },
        ]
    }


@pytest.fixture
def sample_script_input():
    """Sample input for script generation."""
    return {
        "topic": "AI News: GPT-5 Release",
        "format": "youtube_long",
        "target_length": 600,
        "tone": "educational",
        "key_points": [
            "GPT-5 capabilities",
            "Comparison with GPT-4",
            "Impact on industry",
        ],
    }
