# Meta Tag Generator

Generate SEO meta tags for pages

## Installation

```bash
pip install agent-recipes
```

## CLI Usage

```bash
# Basic usage
praison recipes run ai-meta-tag-generator <input>

# With output directory
praison recipes run ai-meta-tag-generator <input> --output ./output/

# Dry run (check dependencies only)
praison recipes run ai-meta-tag-generator <input> --dry-run

# Show recipe info
praison recipes info ai-meta-tag-generator

# Check dependencies
praison recipes doctor ai-meta-tag-generator
```

## Python Usage

```python
from praisonaiagents import Agent
from agent_recipes import load_recipe

# Load and run recipe
recipe = load_recipe("ai-meta-tag-generator")
result = recipe.run(input="<your-input>")
print(result)
```

## Requirements

### Packages
- openai

### Environment Variables
- OPENAI_API_KEY

### External Tools
- None

## Tags

`web`, `seo`, `meta-tags`

## License

Apache-2.0
