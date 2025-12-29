# Social Media Generator

Generate social media posts from content

## Installation

```bash
pip install agent-recipes
```

## CLI Usage

```bash
# Basic usage
praison recipes run ai-social-media-generator <input>

# With output directory
praison recipes run ai-social-media-generator <input> --output ./output/

# Dry run (check dependencies only)
praison recipes run ai-social-media-generator <input> --dry-run

# Show recipe info
praison recipes info ai-social-media-generator

# Check dependencies
praison recipes doctor ai-social-media-generator
```

## Python Usage

```python
from praisonaiagents import Agent
from agent_recipes import load_recipe

# Load and run recipe
recipe = load_recipe("ai-social-media-generator")
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

`web`, `social-media`, `content`

## License

Apache-2.0
