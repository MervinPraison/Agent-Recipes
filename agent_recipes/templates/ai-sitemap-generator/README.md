# Sitemap Generator

Generate XML sitemaps from URLs

## Installation

```bash
pip install agent-recipes
```

## CLI Usage

```bash
# Basic usage
praison recipes run ai-sitemap-generator <input>

# With output directory
praison recipes run ai-sitemap-generator <input> --output ./output/

# Dry run (check dependencies only)
praison recipes run ai-sitemap-generator <input> --dry-run

# Show recipe info
praison recipes info ai-sitemap-generator

# Check dependencies
praison recipes doctor ai-sitemap-generator
```

## Python Usage

```python
from praisonaiagents import Agent
from agent_recipes import load_recipe

# Load and run recipe
recipe = load_recipe("ai-sitemap-generator")
result = recipe.run(input="<your-input>")
print(result)
```

## Requirements

### Packages
- requests

### Environment Variables
- None

### External Tools
- None

## Tags

`web`, `sitemap`, `seo`

## License

Apache-2.0
