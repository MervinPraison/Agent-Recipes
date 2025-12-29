# Seo Optimizer

Optimize content for SEO with keywords

## Installation

```bash
pip install agent-recipes
```

## CLI Usage

```bash
# Basic usage
praison recipes run ai-seo-optimizer <input>

# With output directory
praison recipes run ai-seo-optimizer <input> --output ./output/

# Dry run (check dependencies only)
praison recipes run ai-seo-optimizer <input> --dry-run

# Show recipe info
praison recipes info ai-seo-optimizer

# Check dependencies
praison recipes doctor ai-seo-optimizer
```

## Python Usage

```python
from praisonaiagents import Agent
from agent_recipes import load_recipe

# Load and run recipe
recipe = load_recipe("ai-seo-optimizer")
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

`web`, `seo`, `optimization`

## License

Apache-2.0
