# Image Tagger

Auto-tag images with keywords/categories

## Installation

```bash
pip install agent-recipes
```

## CLI Usage

```bash
# Basic usage
praison recipes run ai-image-tagger <input>

# With output directory
praison recipes run ai-image-tagger <input> --output ./output/

# Dry run (check dependencies only)
praison recipes run ai-image-tagger <input> --dry-run

# Show recipe info
praison recipes info ai-image-tagger

# Check dependencies
praison recipes doctor ai-image-tagger
```

## Python Usage

```python
from praisonaiagents import Agent
from agent_recipes import load_recipe

# Load and run recipe
recipe = load_recipe("ai-image-tagger")
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

`image`, `tagging`, `classification`

## License

Apache-2.0
