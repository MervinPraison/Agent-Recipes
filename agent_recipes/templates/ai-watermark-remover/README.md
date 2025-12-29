# Watermark Remover

Remove watermarks from images (COPYRIGHT WARNING)

## Installation

```bash
pip install agent-recipes
```

## CLI Usage

```bash
# Basic usage
praison recipes run ai-watermark-remover <input>

# With output directory
praison recipes run ai-watermark-remover <input> --output ./output/

# Dry run (check dependencies only)
praison recipes run ai-watermark-remover <input> --dry-run

# Show recipe info
praison recipes info ai-watermark-remover

# Check dependencies
praison recipes doctor ai-watermark-remover
```

## Python Usage

```python
from praisonaiagents import Agent
from agent_recipes import load_recipe

# Load and run recipe
recipe = load_recipe("ai-watermark-remover")
result = recipe.run(input="<your-input>")
print(result)
```

## Requirements

### Packages
- openai
- pillow

### Environment Variables
- OPENAI_API_KEY

### External Tools
- None

## Tags

`image`, `watermark`, `removal`

## License

Apache-2.0
