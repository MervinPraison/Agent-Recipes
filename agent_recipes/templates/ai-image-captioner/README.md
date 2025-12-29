# Image Captioner

Generate alt-text/captions for images

## Installation

```bash
pip install agent-recipes
```

## CLI Usage

```bash
# Basic usage
praison recipes run ai-image-captioner <input>

# With output directory
praison recipes run ai-image-captioner <input> --output ./output/

# Dry run (check dependencies only)
praison recipes run ai-image-captioner <input> --dry-run

# Show recipe info
praison recipes info ai-image-captioner

# Check dependencies
praison recipes doctor ai-image-captioner
```

## Python Usage

```python
from praisonaiagents import Agent
from agent_recipes import load_recipe

# Load and run recipe
recipe = load_recipe("ai-image-captioner")
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

`image`, `caption`, `accessibility`

## License

Apache-2.0
